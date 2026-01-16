"""Compile predicate IR into engine-specific filter expressions."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

import polars as pl

from .errors import PlanError
from .predicate import (
    AndPredicate,
    ColumnRef,
    ComparePredicate,
    InPredicate,
    IsNaNPredicate,
    LiteralValue,
    NotPredicate,
    NullPredicate,
    OrPredicate,
    Predicate,
    StringPredicate,
)


def compile_predicate_to_polars(
    predicate: Predicate,
    schema: Mapping[str, pl.DataType] | None = None,
) -> pl.Expr:
    if isinstance(predicate, AndPredicate):
        return _reduce_polars(predicate.items, op="and", schema=schema)
    if isinstance(predicate, OrPredicate):
        return _reduce_polars(predicate.items, op="or", schema=schema)
    if isinstance(predicate, NotPredicate):
        return ~compile_predicate_to_polars(predicate.predicate, schema=schema)
    if isinstance(predicate, ComparePredicate):
        left = _compile_value_to_polars(predicate.left)
        right = _compile_value_to_polars(predicate.right)
        if predicate.op == "==":
            return left == right
        if predicate.op == "!=":
            return left != right
        if predicate.op == "<":
            return left < right
        if predicate.op == "<=":
            return left <= right
        if predicate.op == ">":
            return left > right
        if predicate.op == ">=":
            return left >= right
        raise PlanError(f"Unsupported comparison operator: {predicate.op}")
    if isinstance(predicate, InPredicate):
        values = [value.value for value in predicate.values]
        return pl.col(predicate.item.name).is_in(values)
    if isinstance(predicate, NullPredicate):
        expr = pl.col(predicate.column.name).is_null()
        return expr if predicate.is_null else ~expr
    if isinstance(predicate, IsNaNPredicate):
        return pl.col(predicate.column.name).is_nan()
    if isinstance(predicate, StringPredicate):
        return _compile_string_predicate(predicate)
    raise PlanError(f"Unsupported predicate: {type(predicate)!r}")


def compile_predicate_to_duckdb_sql(predicate: Predicate) -> tuple[str, tuple[Any, ...]]:
    sql, params = _compile_predicate_sql(predicate)
    return sql, tuple(params)


def _compile_value_to_polars(value: ColumnRef | LiteralValue) -> pl.Expr:
    if isinstance(value, ColumnRef):
        return pl.col(value.name)
    if isinstance(value, LiteralValue):
        return pl.lit(value.value)
    raise PlanError(f"Unsupported value expression: {type(value)!r}")


def _compile_value_to_sql(value: ColumnRef | LiteralValue) -> tuple[str, list[Any]]:
    if isinstance(value, ColumnRef):
        return _quote_identifier(value.name), []
    if isinstance(value, LiteralValue):
        return "?", [value.value]
    raise PlanError(f"Unsupported value expression: {type(value)!r}")


def _reduce_polars(
    items: Sequence[Predicate],
    *,
    op: str,
    schema: Mapping[str, Any] | None,
) -> pl.Expr:
    if not items:
        return pl.lit(True)
    expr = compile_predicate_to_polars(items[0], schema=schema)
    for item in items[1:]:
        compiled = compile_predicate_to_polars(item, schema=schema)
        expr = (expr & compiled) if op == "and" else (expr | compiled)
    return expr


def _compile_predicate_sql(predicate: Predicate) -> tuple[str, list[Any]]:
    if isinstance(predicate, AndPredicate):
        return _reduce_sql(predicate.items, op="and")
    if isinstance(predicate, OrPredicate):
        return _reduce_sql(predicate.items, op="or")
    if isinstance(predicate, NotPredicate):
        inner_sql, inner_params = _compile_predicate_sql(predicate.predicate)
        return f"NOT ({inner_sql})", inner_params
    if isinstance(predicate, ComparePredicate):
        left_sql, left_params = _compile_value_to_sql(predicate.left)
        right_sql, right_params = _compile_value_to_sql(predicate.right)
        return f"{left_sql} {predicate.op} {right_sql}", [*left_params, *right_params]
    if isinstance(predicate, InPredicate):
        if not predicate.values:
            return "FALSE", []
        rendered: list[str] = []
        params: list[Any] = []
        for value in predicate.values:
            value_sql, value_params = _compile_value_to_sql(value)
            rendered.append(value_sql)
            params.extend(value_params)
        values_sql = ", ".join(rendered)
        return f"{_quote_identifier(predicate.item.name)} IN ({values_sql})", params
    if isinstance(predicate, NullPredicate):
        op = "IS NULL" if predicate.is_null else "IS NOT NULL"
        return f"{_quote_identifier(predicate.column.name)} {op}", []
    if isinstance(predicate, IsNaNPredicate):
        return f"isnan({_quote_identifier(predicate.column.name)})", []
    if isinstance(predicate, StringPredicate):
        return _compile_string_predicate_sql(predicate)
    raise PlanError(f"Unsupported predicate: {type(predicate)!r}")


def _reduce_sql(items: Sequence[Predicate], *, op: str) -> tuple[str, list[Any]]:
    if not items:
        return "TRUE", []
    parts: list[str] = []
    params: list[Any] = []
    for item in items:
        item_sql, item_params = _compile_predicate_sql(item)
        parts.append(f"({item_sql})")
        params.extend(item_params)
    joined = f" {op.upper()} ".join(parts)
    return joined, params


def _compile_string_predicate(predicate: StringPredicate) -> pl.Expr:
    if not isinstance(predicate.value, LiteralValue):
        raise PlanError("String predicates require literal values")
    raw = predicate.value.value
    if not isinstance(raw, str):
        raise PlanError("String predicates require string values")
    base = pl.col(predicate.column.name).cast(pl.Utf8, strict=False).fill_null("")

    if predicate.op == "contains":
        pattern = re.escape(raw)
        if predicate.case_insensitive:
            expr = base.str.contains(f"(?i){pattern}", literal=False)
        else:
            expr = base.str.contains(pattern, literal=True)
    elif predicate.op == "starts_with":
        expr = base.str.starts_with(raw)
        if predicate.case_insensitive:
            expr = base.str.to_lowercase().str.starts_with(raw.lower())
    elif predicate.op == "ends_with":
        expr = base.str.ends_with(raw)
        if predicate.case_insensitive:
            expr = base.str.to_lowercase().str.ends_with(raw.lower())
    else:
        raise PlanError(f"Unsupported string predicate: {predicate.op}")

    if predicate.match_nulls:
        expr = expr | pl.col(predicate.column.name).is_null()
    return expr


def _compile_string_predicate_sql(predicate: StringPredicate) -> tuple[str, list[Any]]:
    if not isinstance(predicate.value, LiteralValue):
        raise PlanError("String predicates require literal values")
    raw = predicate.value.value
    if not isinstance(raw, str):
        raise PlanError("String predicates require string values")

    column = _quote_identifier(predicate.column.name)
    escaped = _escape_like(raw)
    if predicate.op == "contains":
        pattern = f"%{escaped}%"
    elif predicate.op == "starts_with":
        pattern = f"{escaped}%"
    elif predicate.op == "ends_with":
        pattern = f"%{escaped}"
    else:
        raise PlanError(f"Unsupported string predicate: {predicate.op}")

    op = "ILIKE" if predicate.case_insensitive else "LIKE"
    expr = f"CAST({column} AS VARCHAR) {op} ? ESCAPE '\\'"
    if predicate.match_nulls:
        expr = f"({expr} OR {column} IS NULL)"
    return expr, [pattern]


def _quote_identifier(value: str) -> str:
    escaped = value.replace('"', '""')
    return f'"{escaped}"'


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


__all__ = ["compile_predicate_to_duckdb_sql", "compile_predicate_to_polars"]
