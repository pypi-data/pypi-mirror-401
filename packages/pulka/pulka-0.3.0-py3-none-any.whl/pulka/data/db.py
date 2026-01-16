"""Database URI helpers for parsing and opening tables."""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

import duckdb
import polars as pl

try:  # pragma: no cover - sqlite may be missing in some environments
    import sqlite3
except Exception:  # pragma: no cover - defensive fallback
    sqlite3 = None


@dataclass(frozen=True, slots=True)
class DbSource:
    """Parsed database URI plus table information."""

    scheme: str
    uri: str
    connection_uri: str
    table: str
    path: Path | None = None


DbLoader = Callable[[DbSource], pl.LazyFrame]


_DB_LOADERS: dict[str, DbLoader] = {}
_DB_SCHEMES: set[str] = set()


def register_db_loader(scheme: str, loader: DbLoader) -> None:
    normalized = scheme.strip().lower()
    if not normalized:
        raise ValueError("DB scheme must be non-empty")
    if normalized in _DB_LOADERS:
        raise ValueError(f"DB loader already registered for '{scheme}'")
    _DB_LOADERS[normalized] = loader
    _DB_SCHEMES.add(normalized)


def register_db_scheme(scheme: str) -> None:
    normalized = scheme.strip().lower()
    if not normalized:
        raise ValueError("DB scheme must be non-empty")
    _DB_SCHEMES.add(normalized)


def list_db_schemes() -> tuple[str, ...]:
    return tuple(sorted(_DB_SCHEMES))


def is_db_uri(value: str | None) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme.lower() in _DB_SCHEMES


def parse_db_uri(uri: str) -> DbSource | None:
    """Parse a db://...#table URI into a concrete source."""

    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    if scheme not in _DB_SCHEMES:
        return None

    table = parsed.fragment.strip()
    if not table:
        msg = "Database URI requires a #table fragment"
        raise ValueError(msg)

    connection_uri = uri.split("#", 1)[0]

    if scheme in {"sqlite", "duckdb"}:
        raw_path = ""
        if parsed.netloc and parsed.path:
            raw_path = f"{parsed.netloc}{parsed.path}"
        elif parsed.netloc:
            raw_path = parsed.netloc
        else:
            raw_path = parsed.path

        raw_path = unquote(raw_path)
        if not raw_path:
            msg = f"{scheme} URI is missing a database path"
            raise ValueError(msg)

        path = Path(raw_path).expanduser()
        return DbSource(
            scheme=scheme,
            uri=uri,
            connection_uri=connection_uri,
            table=table,
            path=path,
        )

    return DbSource(
        scheme=scheme,
        uri=uri,
        connection_uri=connection_uri,
        table=table,
    )


def lazyframe_from_db_uri(uri: str) -> pl.LazyFrame:
    """Load a database table and return it as a Polars LazyFrame."""

    source = parse_db_uri(uri)
    if source is None:
        raise ValueError("Not a supported database URI")

    loader = _DB_LOADERS.get(source.scheme)
    if loader is None:  # pragma: no cover - defensive guard
        raise ValueError(f"No loader registered for scheme '{source.scheme}'")

    lf = loader(source)
    _tag_db_metadata(lf, source)
    return lf


def _quote_identifier(value: str) -> str:
    escaped = value.replace('"', '""')
    return f'"{escaped}"'


def _quote_qualified_identifier(value: str) -> str:
    return ".".join(_quote_identifier(part) for part in value.split(".") if part)


def _sqlite_database_path(connection_uri: str) -> str:
    if connection_uri.startswith("sqlite://"):
        return connection_uri.replace("sqlite://", "", 1)
    return connection_uri


def _inspect_sqlite_schema(connection_uri: str, table: str) -> dict[str, str]:
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
    resolved: dict[str, str] = {}
    for row in rows:
        if len(row) < 3:
            continue
        name = row[1]
        dtype = row[2]
        resolved[name] = dtype
    return resolved


def _sqlite_select_list(columns: Sequence[str], schema: dict[str, str]) -> str:
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


def _sqlite_loader(source: DbSource) -> pl.LazyFrame:
    if source.path is None:
        raise ValueError("SQLite loader requires a file path")
    if not source.path.exists():
        raise FileNotFoundError(source.path)

    table_sql = _quote_qualified_identifier(source.table)
    schema = _inspect_sqlite_schema(source.connection_uri, source.table)
    select_list = _sqlite_select_list(list(schema.keys()), schema) if schema else "*"
    query = f"SELECT {select_list} FROM db.{table_sql}"
    con = duckdb.connect()
    try:
        _attach_sqlite_source(con, source.connection_uri)
        cursor = con.execute(query)
        df = pl.from_arrow(cursor.fetch_arrow_table())
    finally:
        con.close()
    return df.lazy()


def _tag_db_metadata(lf: pl.LazyFrame, source: DbSource) -> None:
    lf._pulka_source_kind = source.scheme  # type: ignore[attr-defined]
    lf._pulka_path = source.uri  # type: ignore[attr-defined]
    lf._pulka_table = source.table  # type: ignore[attr-defined]
    lf._pulka_db_scheme = source.scheme  # type: ignore[attr-defined]


register_db_loader("sqlite", _sqlite_loader)
register_db_scheme("duckdb")
register_db_scheme("postgres")


__all__ = [
    "DbSource",
    "DbLoader",
    "is_db_uri",
    "lazyframe_from_db_uri",
    "list_db_schemes",
    "parse_db_uri",
    "register_db_loader",
    "register_db_scheme",
]
