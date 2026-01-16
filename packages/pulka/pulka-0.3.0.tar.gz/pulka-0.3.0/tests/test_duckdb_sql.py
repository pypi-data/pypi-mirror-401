from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import duckdb
import pytest

from pulka.api.runtime import Runtime
from pulka.core.engine.duckdb_adapter import (
    DuckDBEngineAdapter,
    DuckDBMaterializer,
    DuckDBPhysicalPlan,
    compile_duckdb_plan,
)
from pulka.core.errors import PlanError
from pulka.core.jobs import JobRunner
from pulka.core.plan import FilterClause, QueryPlan
from pulka.sheets.duckdb_sheet import DuckDBSheet


def test_compile_duckdb_plan_sql() -> None:
    source = DuckDBPhysicalPlan(
        scheme="duckdb",
        connection_uri="duckdb://",
        table="items",
        schema={"id": "INTEGER", "name": "VARCHAR", "age": "INTEGER"},
    )
    plan = QueryPlan(
        filter_clauses=[
            FilterClause("sql", "id > 1"),
            FilterClause("sql", "name IS NOT NULL"),
        ],
        sort=(("name", False), ("id", True)),
        projection=("id", "name"),
        limit=10,
        offset=5,
    )

    compiled = compile_duckdb_plan(plan, source)

    assert (
        compiled.sql == 'SELECT "id", "name" FROM "items" WHERE (id > 1) AND '
        '(name IS NOT NULL) ORDER BY "name" ASC, "id" DESC LIMIT 10 OFFSET 5'
    )
    assert compiled.params == ()


def test_compile_duckdb_plan_supports_safe_expr_filters() -> None:
    source = DuckDBPhysicalPlan(
        scheme="duckdb",
        connection_uri="duckdb://",
        table="items",
        schema={"id": "INTEGER"},
    )
    plan = QueryPlan(filter_clauses=[FilterClause("expr", "c.id > 1")])

    compiled = compile_duckdb_plan(plan, source)

    assert compiled.sql == 'SELECT * FROM "items" WHERE ("id" > ?)'
    assert compiled.params == (1,)


def test_compile_duckdb_plan_rejects_unsupported_expr_filters() -> None:
    source = DuckDBPhysicalPlan(
        scheme="duckdb",
        connection_uri="duckdb://",
        table="items",
        schema={"id": "INTEGER"},
    )
    plan = QueryPlan(filter_clauses=[FilterClause("expr", "pl.col('id') > 1")])

    with pytest.raises(PlanError, match="Expression filters are not supported"):
        compile_duckdb_plan(plan, source)


def test_duckdb_materializer_collect_slice_respects_plan(tmp_path) -> None:
    db_path = tmp_path / "sample.duckdb"
    con = duckdb.connect(database=str(db_path))
    try:
        con.execute("CREATE TABLE items (id INTEGER, name VARCHAR)")
        con.execute("INSERT INTO items VALUES (1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'), (5, 'e')")
    finally:
        con.close()

    source = DuckDBPhysicalPlan(
        scheme="duckdb",
        connection_uri=f"duckdb://{db_path}",
        table="items",
        schema={"id": "INTEGER", "name": "VARCHAR"},
    )
    plan = QueryPlan(
        filter_clauses=[FilterClause("sql", "id >= 2")],
        sort=(("id", True),),
        limit=3,
        offset=0,
    )

    adapter = DuckDBEngineAdapter(source)
    compiled = adapter.compile(plan)
    materializer = DuckDBMaterializer()

    slice_ = materializer.collect_slice(compiled, start=1, length=1, columns=("id",))

    assert slice_.height == 1
    assert slice_.column("id").values == (4,)
    assert materializer.count(compiled) == 3


def test_duckdb_materializer_closes_after_shared_sheets(tmp_path) -> None:
    db_path = tmp_path / "sample.duckdb"
    con = duckdb.connect(database=str(db_path))
    try:
        con.execute("CREATE TABLE items (id INTEGER, name VARCHAR)")
        con.execute("INSERT INTO items VALUES (1, 'a'), (2, 'b')")
    finally:
        con.close()

    source = DuckDBPhysicalPlan(
        scheme="duckdb",
        connection_uri=f"duckdb://{db_path}",
        table="items",
        schema={"id": "INTEGER", "name": "VARCHAR"},
    )

    executor = ThreadPoolExecutor(max_workers=1)
    runner = JobRunner(executor=executor)
    materializer = DuckDBMaterializer()
    try:
        sheet = DuckDBSheet(source, runner=runner, materializer=materializer)
        _ = sheet.row_count()
        assert materializer._connection is not None

        derived = sheet.with_plan(sheet.plan.with_projection(("id",)))
        sheet.close()
        assert materializer._connection is not None

        derived.close()
        assert materializer._connection is None
    finally:
        runner.close()
        executor.shutdown(wait=False)


def test_duckdb_session_close_releases_connection(tmp_path) -> None:
    db_path = tmp_path / "sample.duckdb"
    con = duckdb.connect(database=str(db_path))
    try:
        con.execute("CREATE TABLE items (id INTEGER, name VARCHAR)")
        con.execute("INSERT INTO items VALUES (1, 'a'), (2, 'b')")
    finally:
        con.close()

    runtime = Runtime()
    session = runtime.open(f"duckdb://{db_path}#items")
    try:
        _ = session.render()
        sheet = session.viewer.sheet
        materializer = sheet._materializer
        assert materializer._connection is not None
        session.close()
        assert materializer._connection is None
    finally:
        session.close()
        runtime.close()
