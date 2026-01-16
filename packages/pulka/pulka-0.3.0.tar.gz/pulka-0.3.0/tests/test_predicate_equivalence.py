from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import duckdb

from pulka.core.engine.duckdb_adapter import (
    DuckDBEngineAdapter,
    DuckDBMaterializer,
    DuckDBPhysicalPlan,
    inspect_source_schema,
)
from pulka.core.engine.polars_adapter import Materializer as PolarsMaterializer
from pulka.core.engine.polars_adapter import PlanCompiler as PolarsPlanCompiler
from pulka.core.plan import QueryPlan
from pulka.core.predicate import (
    ColumnRef,
    ComparePredicate,
    InPredicate,
    LiteralValue,
    NullPredicate,
    StringPredicate,
    and_predicates,
    or_predicates,
)
from pulka.testing.data import make_df


def _rows_for_columns(
    table_slice: Any,
    columns: Iterable[str],
) -> list[tuple[Any, ...]]:
    return list(zip(*(table_slice.column(name).values for name in columns), strict=True))


def _build_duckdb_source(tmp_path: Path, table: str, df: Any) -> DuckDBPhysicalPlan:
    parquet_path = tmp_path / "data.parquet"
    df.write_parquet(parquet_path)

    db_path = tmp_path / "data.duckdb"
    con = duckdb.connect(database=str(db_path))
    try:
        con.execute(
            f"CREATE TABLE {table} AS SELECT * FROM read_parquet(?)",
            [str(parquet_path)],
        )
    finally:
        con.close()

    schema = inspect_source_schema(
        scheme="duckdb",
        connection_uri=f"duckdb://{db_path}",
        table=table,
    )
    return DuckDBPhysicalPlan(
        scheme="duckdb",
        connection_uri=f"duckdb://{db_path}",
        table=table,
        schema=schema,
    )


def _collect_polars(plan: QueryPlan, df: Any) -> Any:
    compiler = PolarsPlanCompiler(df.lazy(), df.columns, df.schema)
    compiled = compiler.compile(plan)
    return PolarsMaterializer().collect(compiled)


def _collect_duckdb(plan: QueryPlan, source: DuckDBPhysicalPlan) -> Any:
    adapter = DuckDBEngineAdapter(source)
    compiled = adapter.compile(plan)
    materializer = DuckDBMaterializer()
    try:
        return materializer.collect(compiled)
    finally:
        materializer.close()


def test_predicate_equivalence_for_and_string_contains(tmp_path: Path) -> None:
    df = make_df("mini_nav", rows=40, cols=6, seed=42)
    table = "items"
    source = _build_duckdb_source(tmp_path, table, df)

    predicate = and_predicates(
        ComparePredicate(">", ColumnRef("col_00"), LiteralValue(5)),
        NullPredicate(ColumnRef("col_02"), is_null=False),
        StringPredicate(
            "contains",
            ColumnRef("col_01"),
            LiteralValue("a"),
            case_insensitive=True,
        ),
    )
    projection = ("col_00", "col_01", "col_02")
    plan = QueryPlan(predicates=(predicate,), sort=(("col_00", False),), projection=projection)

    polars_slice = _collect_polars(plan, df)
    duckdb_slice = _collect_duckdb(plan, source)

    assert _rows_for_columns(polars_slice, projection) == _rows_for_columns(
        duckdb_slice, projection
    )


def test_predicate_equivalence_for_or_in(tmp_path: Path) -> None:
    df = make_df("mini_nav", rows=40, cols=6, seed=42)
    table = "items"
    source = _build_duckdb_source(tmp_path, table, df)

    predicate = or_predicates(
        ComparePredicate("==", ColumnRef("col_00"), LiteralValue(1)),
        InPredicate(
            ColumnRef("col_00"),
            (LiteralValue(3), LiteralValue(7)),
        ),
    )
    projection = ("col_00", "col_01")
    plan = QueryPlan(predicates=(predicate,), sort=(("col_00", False),), projection=projection)

    polars_slice = _collect_polars(plan, df)
    duckdb_slice = _collect_duckdb(plan, source)

    assert _rows_for_columns(polars_slice, projection) == _rows_for_columns(
        duckdb_slice, projection
    )
