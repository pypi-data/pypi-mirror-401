# mypy: ignore-errors

"""DuckDB-backed implementation of the core engine contracts."""

from __future__ import annotations

import contextlib
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

import duckdb

try:  # pragma: no cover - sqlite may be missing in some environments
    import sqlite3
except Exception:  # pragma: no cover - defensive fallback
    sqlite3 = None

from ...data.filter_lang import FilterError, compile_filter_predicate
from ...utils import _boot_trace
from ..errors import MaterializeError, PlanError
from ..plan import Predicate, QueryPlan
from ..predicate import AndPredicate, NotPredicate, OrPredicate, StringPredicate
from ..predicate_compiler import compile_predicate_to_duckdb_sql
from .contracts import EnginePayloadHandle, PhysicalPlan, TableColumn, TableSlice

DUCKDB_ENGINE = "duckdb"
"""Identifier used for handles backed by the DuckDB engine."""

_KIND_PHYSICAL_PLAN = "physical_plan"
_KIND_COMPILED_PLAN = "compiled_plan"

_BOOT_TRACE_FIRST_CONNECT = True
_BOOT_TRACE_FIRST_QUERY = True
_BOOT_TRACE_FIRST_SCHEMA = True


def _quote_identifier(value: str) -> str:
    escaped = value.replace('"', '""')
    return f'"{escaped}"'


def _quote_qualified_identifier(value: str) -> str:
    return ".".join(_quote_identifier(part) for part in value.split(".") if part)


def quote_duckdb_identifier(value: str) -> str:
    """Public wrapper for quoting DuckDB identifiers."""

    return _quote_identifier(value)


@dataclass(slots=True)
class DuckDBPhysicalPlan:
    """Wrapper around a DuckDB source with cached schema."""

    scheme: str
    connection_uri: str
    table: str
    schema: dict[str, Any]

    def table_ref(self) -> str:
        quoted = _quote_qualified_identifier(self.table)
        if self.scheme in {"postgres", "sqlite"}:
            return f"db.{quoted}"
        return quoted


@dataclass(slots=True)
class DuckDBCompiledPlan:
    """Compiled DuckDB query parts plus the rendered SQL."""

    source: DuckDBPhysicalPlan
    sql: str
    params: tuple[Any, ...]
    projection: tuple[str, ...]
    filters: tuple[str, ...]
    sort: tuple[tuple[str, bool], ...]
    limit: int | None
    offset: int


class DuckDBEngineAdapter:
    """Minimal adapter that exposes a stable DuckDB physical plan."""

    supports_predicates: bool = True
    supports_case_insensitive_contains: bool = True

    def __init__(self, source: DuckDBPhysicalPlan) -> None:
        self._source = source

    def compile(self, plan: QueryPlan) -> PhysicalPlan:
        compiled = compile_duckdb_plan(plan, self._source)
        return make_compiled_plan_handle(compiled)

    def validate_filter(self, clause: str) -> None:
        try:
            predicate = compile_filter_predicate(clause, self._source.schema.keys())
        except FilterError as exc:
            raise PlanError(str(exc)) from exc
        if predicate is None:
            msg = "Expression filters are not supported for DuckDB sources"
            raise PlanError(msg)
        _validate_predicate_capabilities([predicate], self)
        compile_predicate_to_duckdb_sql(predicate)

    def validate_predicates(self, predicates: Sequence[Predicate]) -> None:
        _validate_predicate_capabilities(predicates, self)
        for predicate in predicates:
            compile_predicate_to_duckdb_sql(predicate)

    def validate_sql_where(self, clause: str) -> None:
        _validate_sql_where_clause(self._source, clause)


@dataclass(slots=True)
class DuckDBMaterializer:
    """Collect DuckDB queries into :class:`TableSlice` objects."""

    _connection: duckdb.DuckDBPyConnection | None = None
    _connection_key: tuple[str, str] | None = None
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)
    _ref_count: int = field(default=1, init=False, repr=False)

    def collect(self, plan: PhysicalPlan) -> TableSlice:
        global _BOOT_TRACE_FIRST_QUERY
        compiled = unwrap_compiled_plan(plan)
        if _BOOT_TRACE_FIRST_QUERY:
            _BOOT_TRACE_FIRST_QUERY = False
            _boot_trace("duckdb:collect first query")
        return self._execute_query(compiled.source, compiled.sql, params=compiled.params)

    def share(self) -> DuckDBMaterializer:
        """Return this materializer while incrementing the shared ref count."""

        with self._lock:
            self._ref_count += 1
        return self

    def close(self) -> None:
        """Release any shared DuckDB connection held by this materializer."""

        with self._lock:
            if self._ref_count <= 0:
                return
            self._ref_count -= 1
            if self._ref_count > 0:
                return
            if self._connection is not None:
                with contextlib.suppress(Exception):
                    self._connection.close()
            self._connection = None
            self._connection_key = None

    def collect_slice(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
    ) -> TableSlice:
        global _BOOT_TRACE_FIRST_QUERY
        compiled = unwrap_compiled_plan(plan)
        if _BOOT_TRACE_FIRST_QUERY:
            _BOOT_TRACE_FIRST_QUERY = False
            _boot_trace("duckdb:collect_slice first query")
        query, params = _build_select_query(compiled, columns, start, length)
        return self._execute_query(
            compiled.source,
            query,
            params=params,
            start_offset=start,
        )

    def collect_slice_stream(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
        batch_rows: int | None = None,
    ) -> Iterator[TableSlice]:
        if batch_rows is None or batch_rows <= 0:
            yield self.collect_slice(plan, start=start, length=length, columns=columns)
            return
        remaining = length
        cursor = start
        while remaining is None or remaining > 0:
            chunk = batch_rows if remaining is None else min(batch_rows, remaining)
            slice_ = self.collect_slice(plan, start=cursor, length=chunk, columns=columns)
            if slice_.height == 0:
                break
            yield slice_
            cursor += slice_.height
            if remaining is not None:
                remaining -= slice_.height
            if slice_.height < chunk:
                break

    def count(self, plan: PhysicalPlan) -> int | None:
        compiled = unwrap_compiled_plan(plan)
        query = f"SELECT COUNT(*) FROM ({compiled.sql}) AS pulka_count"
        try:
            rows, _schema = self._execute_rows(compiled.source, query, params=compiled.params)
        except Exception:
            return None
        if not rows:
            return 0
        return int(rows[0][0])

    def _get_connection(self, source: DuckDBPhysicalPlan) -> duckdb.DuckDBPyConnection:
        key = (source.scheme, source.connection_uri)
        if self._connection is None or self._connection_key != key:
            if self._connection is not None:
                with contextlib.suppress(Exception):
                    self._connection.close()
            self._connection = _open_connection(source)
            self._connection_key = key
        return self._connection

    def _execute_query(
        self,
        source: DuckDBPhysicalPlan,
        query: str,
        *,
        params: Sequence[Any] | None = None,
        start_offset: int | None = None,
    ) -> TableSlice:
        with self._lock:
            con = self._get_connection(source)
            try:
                rows, schema = _execute_rows(source, query, con=con, params=params)
            except Exception as exc:
                msg = f"Failed to materialise DuckDB query: {exc}"
                raise MaterializeError(msg) from exc
        return _slice_from_rows(rows, schema, start_offset=start_offset)

    def _execute_rows(
        self,
        source: DuckDBPhysicalPlan,
        query: str,
        *,
        params: Sequence[Any] | None = None,
    ) -> tuple[list[tuple[Any, ...]], dict[str, Any]]:
        with self._lock:
            con = self._get_connection(source)
            return _execute_rows(source, query, con=con, params=params)


def make_physical_plan_handle(plan: DuckDBPhysicalPlan) -> PhysicalPlan:
    return EnginePayloadHandle(DUCKDB_ENGINE, _KIND_PHYSICAL_PLAN, plan)


def unwrap_physical_plan(plan: PhysicalPlan) -> DuckDBPhysicalPlan:
    if not isinstance(plan, EnginePayloadHandle):
        msg = "DuckDB plan must be wrapped in an EnginePayloadHandle"
        raise TypeError(msg)
    return plan.unwrap(expected_engine=DUCKDB_ENGINE, expected_kind=_KIND_PHYSICAL_PLAN)


def make_compiled_plan_handle(plan: DuckDBCompiledPlan) -> PhysicalPlan:
    return EnginePayloadHandle(DUCKDB_ENGINE, _KIND_COMPILED_PLAN, plan)


def unwrap_compiled_plan(plan: PhysicalPlan) -> DuckDBCompiledPlan:
    if not isinstance(plan, EnginePayloadHandle):
        msg = "DuckDB plan must be wrapped in an EnginePayloadHandle"
        raise TypeError(msg)
    return plan.unwrap(expected_engine=DUCKDB_ENGINE, expected_kind=_KIND_COMPILED_PLAN)


def inspect_source_schema(
    *,
    scheme: str,
    connection_uri: str,
    table: str,
) -> dict[str, Any]:
    global _BOOT_TRACE_FIRST_SCHEMA
    if _BOOT_TRACE_FIRST_SCHEMA:
        _BOOT_TRACE_FIRST_SCHEMA = False
        _boot_trace("duckdb:schema inspect start")
    if scheme == "sqlite":
        schema = _inspect_sqlite_schema(connection_uri, table)
    else:
        query = f"SELECT * FROM {_table_ref_for_scheme(scheme, table)} LIMIT 0"
        rows, schema = _execute_rows(
            DuckDBPhysicalPlan(scheme, connection_uri, table, {}),
            query,
        )
        _ = rows
    _boot_trace("duckdb:schema inspect done")
    return schema


def compile_duckdb_plan(plan: QueryPlan, source: DuckDBPhysicalPlan) -> DuckDBCompiledPlan:
    projection = _compile_projection(plan, source)
    filters, params = _compile_filters(plan, source)
    if plan.predicates:
        predicate_filters, predicate_params = _compile_predicates(plan.predicates)
        filters = (*filters, *predicate_filters)
        params = (*params, *predicate_params)
    sort = _compile_sort(plan, source)
    sql = _render_query(
        source,
        projection=projection,
        filters=filters,
        sort=sort,
        limit=plan.limit,
        offset=plan.offset,
    )
    return DuckDBCompiledPlan(
        source=source,
        sql=sql,
        params=params,
        projection=projection,
        filters=filters,
        sort=sort,
        limit=plan.limit,
        offset=plan.offset,
    )


def compile_duckdb_plan_sql(
    plan: QueryPlan, source: DuckDBPhysicalPlan
) -> tuple[str, tuple[Any, ...]]:
    """Compile ``plan`` to SQL text plus positional parameters."""

    compiled = compile_duckdb_plan(plan, source)
    return compiled.sql, compiled.params


def _compile_projection(plan: QueryPlan, source: DuckDBPhysicalPlan) -> tuple[str, ...]:
    if not plan.projection:
        return ()
    available = tuple(source.schema.keys())
    if not available:
        return tuple(plan.projection)
    return tuple(_valid_projection(plan.projection, available))


def _compile_filters(
    plan: QueryPlan,
    source: DuckDBPhysicalPlan,
) -> tuple[tuple[str, ...], tuple[Any, ...]]:
    filters: list[str] = []
    params: list[Any] = []
    for clause in plan.filter_clauses:
        if clause.kind == "expr":
            try:
                predicate = compile_filter_predicate(clause.text, source.schema.keys())
            except FilterError as exc:
                raise PlanError(str(exc)) from exc
            if predicate is None:
                msg = "Expression filters are not supported for DuckDB sources"
                raise PlanError(msg)
            _validate_predicate_capabilities([predicate], DuckDBEngineAdapter)
            predicate_sql, predicate_params = compile_predicate_to_duckdb_sql(predicate)
            filters.append(predicate_sql)
            params.extend(predicate_params)
        if clause.kind == "sql":
            filters.append(clause.text)
    return tuple(filters), tuple(params)


def _compile_predicates(
    predicates: Sequence[Predicate],
) -> tuple[tuple[str, ...], tuple[Any, ...]]:
    filters: list[str] = []
    params: list[Any] = []
    for predicate in predicates:
        _validate_predicate_capabilities([predicate], DuckDBEngineAdapter)
        predicate_sql, predicate_params = compile_predicate_to_duckdb_sql(predicate)
        filters.append(predicate_sql)
        params.extend(predicate_params)
    return tuple(filters), tuple(params)


def _compile_sort(plan: QueryPlan, source: DuckDBPhysicalPlan) -> tuple[tuple[str, bool], ...]:
    if not plan.sort:
        return ()
    available = set(source.schema.keys())
    if not available:
        return tuple(plan.sort)
    return tuple((name, desc) for name, desc in plan.sort if name in available)


def _build_select_query(
    plan: DuckDBCompiledPlan,
    columns: Sequence[str] | None,
    start: int,
    length: int | None,
) -> tuple[str, tuple[Any, ...]]:
    projection = _projection_for_slice(plan, columns)
    limit, offset = _apply_slice(plan.limit, plan.offset, start, length)
    query = _render_query(
        plan.source,
        projection=projection,
        filters=plan.filters,
        sort=plan.sort,
        limit=limit,
        offset=offset,
    )
    return query, plan.params


def _validate_predicate_capabilities(
    predicates: Sequence[Predicate],
    features: object,
) -> None:
    if not getattr(features, "supports_predicates", True):
        msg = "Predicate filtering is not supported"
        raise PlanError(msg)
    if not getattr(features, "supports_case_insensitive_contains", True) and (
        _requires_case_insensitive_contains(predicates)
    ):
        msg = "Case-insensitive contains is not supported"
        raise PlanError(msg)


def _requires_case_insensitive_contains(predicates: Sequence[Predicate]) -> bool:
    return any(_predicate_requires_case_insensitive_contains(predicate) for predicate in predicates)


def _predicate_requires_case_insensitive_contains(predicate: Predicate) -> bool:
    if isinstance(predicate, StringPredicate):
        return predicate.case_insensitive
    if isinstance(predicate, AndPredicate):
        return any(_predicate_requires_case_insensitive_contains(item) for item in predicate.items)
    if isinstance(predicate, OrPredicate):
        return any(_predicate_requires_case_insensitive_contains(item) for item in predicate.items)
    if isinstance(predicate, NotPredicate):
        return _predicate_requires_case_insensitive_contains(predicate.predicate)
    return False


def _projection_for_slice(
    plan: DuckDBCompiledPlan, columns: Sequence[str] | None
) -> tuple[str, ...]:
    if columns is None:
        return plan.projection
    seen: set[str] = set()
    projected = []
    available = set(plan.projection) if plan.projection else None
    for name in columns:
        if name in seen:
            continue
        if available is not None and name not in available:
            continue
        projected.append(name)
        seen.add(name)
    return tuple(projected)


def _apply_slice(
    limit: int | None, offset: int, start: int, length: int | None
) -> tuple[int | None, int]:
    base_offset = max(0, int(offset))
    start = max(0, int(start))
    combined_offset = base_offset + start
    if limit is None:
        return (None if length is None else max(0, int(length))), combined_offset
    remaining = max(0, int(limit) - start)
    if length is None:
        return remaining, combined_offset
    return min(max(0, int(length)), remaining), combined_offset


def _valid_projection(names: Sequence[str], available: Sequence[str]) -> list[str]:
    available_set = set(available)
    projection: list[str] = []
    for name in names:
        if name in available_set and name not in projection:
            projection.append(name)
    return projection


def _render_query(
    source: DuckDBPhysicalPlan,
    *,
    projection: Sequence[str],
    filters: Sequence[str],
    sort: Sequence[tuple[str, bool]],
    limit: int | None,
    offset: int,
) -> str:
    if source.scheme == "sqlite":
        base_columns = list(projection) if projection else list(source.schema.keys())
        select_list = _sqlite_select_list(base_columns, source.schema)
        query = f"SELECT {select_list} FROM {source.table_ref()}"
    else:
        select_list = (
            ", ".join(_quote_identifier(name) for name in projection) if projection else "*"
        )
        query = f"SELECT {select_list} FROM {source.table_ref()}"
    if filters:
        conditions = " AND ".join(f"({clause})" for clause in filters)
        query += f" WHERE {conditions}"
    if sort:
        ordering = ", ".join(
            f"{_quote_identifier(name)} {'DESC' if desc else 'ASC'}" for name, desc in sort
        )
        query += f" ORDER BY {ordering}"
    if limit is not None:
        query += f" LIMIT {max(0, int(limit))}"
    if offset > 0:
        query += f" OFFSET {max(0, int(offset))}"
    return query


def _slice_from_rows(
    rows: Sequence[Sequence[Any]],
    schema: dict[str, Any],
    *,
    start_offset: int | None = None,
) -> TableSlice:
    if not schema:
        return TableSlice.empty(schema.keys(), schema)

    column_names = list(schema.keys())
    columns: list[TableColumn] = []
    values_by_column = {name: [] for name in column_names}
    null_counts = dict.fromkeys(column_names, 0)

    for row in rows:
        for index, name in enumerate(column_names):
            value = row[index] if index < len(row) else None
            if value is None:
                null_counts[name] += 1
            values_by_column[name].append(value)

    for name in column_names:
        values = tuple(values_by_column[name])
        columns.append(TableColumn(name, values, schema.get(name), null_counts[name]))

    return TableSlice(tuple(columns), schema, start_offset=start_offset)


def _execute_rows(
    source: DuckDBPhysicalPlan,
    query: str,
    *,
    con: duckdb.DuckDBPyConnection | None = None,
    params: Sequence[Any] | None = None,
) -> tuple[list[tuple[Any, ...]], dict[str, Any]]:
    close_after = False
    if con is None:
        con = _open_connection(source)
        close_after = True
    try:
        cursor = con.execute(query) if params is None else con.execute(query, params)
        rows = cursor.fetchall()
        schema = _schema_from_cursor(cursor)
        return rows, schema
    finally:
        if close_after:
            con.close()


def _schema_from_cursor(cursor: duckdb.DuckDBPyConnection) -> dict[str, Any]:
    description = getattr(cursor, "description", None)
    if not description:
        return {}
    schema: dict[str, Any] = {}
    for entry in description:
        name = entry[0]
        dtype = entry[1] if len(entry) > 1 else None
        schema[name] = dtype
    return schema


def execute_duckdb_query(
    source: DuckDBPhysicalPlan,
    query: str,
    *,
    params: Sequence[Any] | None = None,
) -> tuple[list[tuple[Any, ...]], dict[str, Any]]:
    """Run a query against ``source`` and return rows plus a schema mapping."""

    return _execute_rows(source, query, params=params)


def _normalize_duckdb_dtype_text(dtype: Any) -> str:
    if dtype is None:
        return ""
    text = str(dtype).strip().lower()
    for delimiter in ("(", "[", "<"):
        if delimiter in text:
            text = text.split(delimiter, 1)[0]
    return text.strip()


def duckdb_dtype_label(dtype: Any) -> str | None:
    """Return a short, panel-friendly dtype label for DuckDB types."""

    text = _normalize_duckdb_dtype_text(dtype)
    if not text:
        return None
    if text.startswith("timestamp") or text in {"datetime"}:
        return "datetime"
    if text.startswith("date"):
        return "date"
    if text.startswith("time"):
        return "time"
    if text.startswith("interval") or text.startswith("duration"):
        return "duration"
    if text in {"varchar", "text", "string", "uuid", "enum"} or "char" in text:
        return "string"
    if text in {"bool", "boolean"}:
        return "bool"
    if text.startswith("uint") or (text.startswith("u") and "int" in text):
        return "uint"
    if text.startswith("int") or text in {"integer", "bigint", "smallint", "tinyint"}:
        return "int"
    if text in {"double", "float", "real"}:
        return "float"
    if text.startswith("decimal") or text.startswith("numeric"):
        return "decimal"
    return text


def duckdb_dtype_category(dtype: Any) -> str | None:
    """Return ``numeric``, ``temporal``, ``string``, or ``boolean`` for DuckDB dtypes."""

    label = duckdb_dtype_label(dtype)
    if label is None:
        return None
    if label.startswith(("int", "uint", "float", "decimal")):
        return "numeric"
    if label.startswith(("date", "datetime", "time", "duration")):
        return "temporal"
    if label.startswith(("string", "str", "utf", "categorical", "enum")):
        return "string"
    if label.startswith("bool"):
        return "boolean"
    return None


def _open_connection(source: DuckDBPhysicalPlan) -> duckdb.DuckDBPyConnection:
    global _BOOT_TRACE_FIRST_CONNECT
    if _BOOT_TRACE_FIRST_CONNECT:
        _BOOT_TRACE_FIRST_CONNECT = False
        _boot_trace(f"duckdb:open connection (scheme={source.scheme})")
    if source.scheme == "duckdb":
        database = _duckdb_database_path(source.connection_uri)
        return duckdb.connect(database=database)
    if source.scheme == "postgres":
        con = duckdb.connect()
        _attach_postgres_source(con, source.connection_uri)
        return con
    if source.scheme == "sqlite":
        con = duckdb.connect()
        _attach_sqlite_source(con, source.connection_uri)
        return con
    msg = f"Unsupported DuckDB scheme: {source.scheme}"
    raise ValueError(msg)


def _duckdb_database_path(connection_uri: str) -> str:
    if connection_uri.startswith("duckdb://"):
        return connection_uri.replace("duckdb://", "", 1) or ":memory:"
    return connection_uri


def _sqlite_database_path(connection_uri: str) -> str:
    if connection_uri.startswith("sqlite://"):
        return connection_uri.replace("sqlite://", "", 1)
    return connection_uri


def _attach_postgres_source(con: duckdb.DuckDBPyConnection, connection_uri: str) -> None:
    for statement in ("INSTALL postgres", "LOAD postgres"):
        with contextlib.suppress(Exception):
            con.execute(statement)
    attempts = [
        f"ATTACH '{connection_uri}' AS db (TYPE POSTGRES)",
        f"ATTACH '{connection_uri}' AS db",
    ]
    last_exc: Exception | None = None
    for statement in attempts:
        try:
            con.execute(statement)
            return
        except Exception as exc:  # pragma: no cover - depends on environment
            last_exc = exc
    msg = "Failed to attach Postgres source to DuckDB"
    raise RuntimeError(msg) from last_exc


def _table_ref_for_scheme(scheme: str, table: str) -> str:
    quoted = _quote_qualified_identifier(table)
    if scheme in {"postgres", "sqlite"}:
        return f"db.{quoted}"
    return quoted


def _validate_sql_where_clause(source: DuckDBPhysicalPlan, clause: str) -> None:
    query = f"SELECT * FROM {source.table_ref()} WHERE {clause} LIMIT 0"
    con = _open_connection(source)
    try:
        con.execute(query)
    finally:
        con.close()


def _attach_sqlite_source(con: duckdb.DuckDBPyConnection, connection_uri: str) -> None:
    for statement in ("INSTALL sqlite_scanner", "LOAD sqlite_scanner"):
        with contextlib.suppress(Exception):
            con.execute(statement)
    with contextlib.suppress(Exception):
        con.execute("SET sqlite_all_varchar=true")
    database = _sqlite_database_path(connection_uri)
    attempts = [
        f"ATTACH '{database}' AS db (TYPE SQLITE)",
        f"ATTACH '{database}' AS db",
    ]
    last_exc: Exception | None = None
    for statement in attempts:
        try:
            con.execute(statement)
            return
        except Exception as exc:  # pragma: no cover - depends on environment
            last_exc = exc
    msg = "Failed to attach SQLite source to DuckDB"
    raise RuntimeError(msg) from last_exc


def _inspect_sqlite_schema(connection_uri: str, table: str) -> dict[str, Any]:
    if sqlite3 is None:  # pragma: no cover - import guard
        msg = "sqlite3 is unavailable in this environment"
        raise RuntimeError(msg)
    database = _sqlite_database_path(connection_uri)
    schema = ""
    table_name = table
    if "." in table:
        schema, _, table_name = table.partition(".")
    pragma_target = (
        f"{schema}.table_info('{table_name}')" if schema else f"table_info('{table_name}')"
    )
    with sqlite3.connect(database) as conn:
        rows = conn.execute(f"PRAGMA {pragma_target}").fetchall()
    schema: dict[str, Any] = {}
    for row in rows:
        if len(row) < 3:
            continue
        name = row[1]
        dtype = row[2]
        schema[name] = dtype
    return schema


def _sqlite_select_list(columns: Sequence[str], schema: dict[str, Any]) -> str:
    parts: list[str] = []
    for name in columns:
        quoted = _quote_identifier(name)
        dtype = schema.get(name)
        type_text = str(dtype).upper() if dtype is not None else ""
        if "BLOB" in type_text or "BINARY" in type_text:
            expr = f"NULL AS {quoted}"
        elif "INT" in type_text or any(
            token in type_text for token in ("REAL", "FLOA", "DOUB", "DEC", "NUM")
        ):
            expr = f"TRY_CAST({quoted} AS DOUBLE) AS {quoted}"
        else:
            expr = quoted
        parts.append(expr)
    return ", ".join(parts) if parts else "*"


__all__ = [
    "DUCKDB_ENGINE",
    "DuckDBCompiledPlan",
    "DuckDBEngineAdapter",
    "DuckDBMaterializer",
    "DuckDBPhysicalPlan",
    "compile_duckdb_plan",
    "compile_duckdb_plan_sql",
    "duckdb_dtype_category",
    "duckdb_dtype_label",
    "execute_duckdb_query",
    "inspect_source_schema",
    "make_compiled_plan_handle",
    "make_physical_plan_handle",
    "quote_duckdb_identifier",
    "unwrap_compiled_plan",
    "unwrap_physical_plan",
]
