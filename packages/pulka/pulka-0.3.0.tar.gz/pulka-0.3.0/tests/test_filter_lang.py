from __future__ import annotations

from pulka.core.predicate import (
    AndPredicate,
    ColumnRef,
    ComparePredicate,
    InPredicate,
    IsNaNPredicate,
    LiteralValue,
    NotPredicate,
    NullPredicate,
    StringPredicate,
)
from pulka.data.filter_lang import (
    clear_filter_cache,
    compile_filter_expression,
    compile_filter_predicate,
)


def test_cache_hits_for_identical_text_and_schema() -> None:
    clear_filter_cache()
    columns = ["a", "b"]

    expr1 = compile_filter_expression("c.a > 1", columns)
    expr2 = compile_filter_expression("c.a > 1", columns)

    assert expr1 is expr2


def test_cache_miss_for_different_schema() -> None:
    clear_filter_cache()

    expr1 = compile_filter_expression("c.a > 1", ["a"])
    expr2 = compile_filter_expression("c.a > 1", ["a", "b"])

    assert expr1 is not expr2


def test_compile_filter_predicate_basic_compare() -> None:
    predicate = compile_filter_predicate("c.a > 1", ["a"])

    assert predicate == ComparePredicate(">", ColumnRef("a"), LiteralValue(1))


def test_compile_filter_predicate_bool_ops() -> None:
    predicate = compile_filter_predicate("c.a > 1 and c.b == 2", ["a", "b"])

    assert predicate == AndPredicate(
        (
            ComparePredicate(">", ColumnRef("a"), LiteralValue(1)),
            ComparePredicate("==", ColumnRef("b"), LiteralValue(2)),
        )
    )


def test_compile_filter_predicate_null_predicates() -> None:
    predicate = compile_filter_predicate("c.a.is_null()", ["a"])

    assert predicate == NullPredicate(ColumnRef("a"), is_null=True)

    predicate = compile_filter_predicate("c.a.is_not_null()", ["a"])

    assert predicate == NullPredicate(ColumnRef("a"), is_null=False)


def test_compile_filter_predicate_is_in() -> None:
    predicate = compile_filter_predicate("c.a.is_in([1, 2])", ["a"])

    assert predicate == InPredicate(
        ColumnRef("a"),
        (LiteralValue(1), LiteralValue(2)),
    )


def test_compile_filter_predicate_compare_methods() -> None:
    predicate = compile_filter_predicate("c.a.gt(10)", ["a"])

    assert predicate == ComparePredicate(">", ColumnRef("a"), LiteralValue(10))


def test_compile_filter_predicate_is_nan() -> None:
    predicate = compile_filter_predicate("c.a.is_nan()", ["a"])

    assert predicate == IsNaNPredicate(ColumnRef("a"))

    predicate = compile_filter_predicate("c.a.is_not_nan()", ["a"])

    assert predicate == NotPredicate(IsNaNPredicate(ColumnRef("a")))


def test_compile_filter_predicate_is_between() -> None:
    predicate = compile_filter_predicate("c.a.is_between(1, 3)", ["a"])

    assert predicate == AndPredicate(
        (
            ComparePredicate(">=", ColumnRef("a"), LiteralValue(1)),
            ComparePredicate("<=", ColumnRef("a"), LiteralValue(3)),
        )
    )


def test_compile_filter_predicate_string_contains_literal() -> None:
    predicate = compile_filter_predicate("c.a.str.contains('x', literal=True)", ["a"])

    assert predicate == StringPredicate(
        "contains",
        ColumnRef("a"),
        LiteralValue("x"),
        case_insensitive=False,
    )


def test_compile_filter_predicate_rejects_regex_contains() -> None:
    predicate = compile_filter_predicate("c.a.str.contains('x')", ["a"])

    assert predicate is None


def test_compile_filter_predicate_ignores_polars_namespace() -> None:
    predicate = compile_filter_predicate("pl.col('a') > 1", ["a"])

    assert predicate is None
