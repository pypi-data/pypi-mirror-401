from __future__ import annotations

import pytest

from pulka.core.errors import PlanError
from pulka.core.predicate import ColumnRef, LiteralValue, StringPredicate
from pulka.core.predicate_compiler import (
    compile_predicate_to_duckdb_sql,
    compile_predicate_to_polars,
)


def test_compile_predicate_to_polars_rejects_non_string() -> None:
    predicate = StringPredicate("contains", ColumnRef("col"), LiteralValue(123))

    with pytest.raises(PlanError, match="String predicates require string values"):
        compile_predicate_to_polars(predicate)


def test_compile_predicate_to_duckdb_sql_rejects_non_string() -> None:
    predicate = StringPredicate("contains", ColumnRef("col"), LiteralValue(123))

    with pytest.raises(PlanError, match="String predicates require string values"):
        compile_predicate_to_duckdb_sql(predicate)
