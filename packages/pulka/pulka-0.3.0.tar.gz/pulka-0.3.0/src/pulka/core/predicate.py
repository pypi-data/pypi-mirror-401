"""Engine-neutral predicate IR used by query plans."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True, slots=True)
class ColumnRef:
    name: str


@dataclass(frozen=True, slots=True)
class LiteralValue:
    value: Any


ValueExpr = ColumnRef | LiteralValue


@dataclass(frozen=True, slots=True)
class ComparePredicate:
    op: Literal["==", "!=", "<", "<=", ">", ">="]
    left: ValueExpr
    right: ValueExpr


@dataclass(frozen=True, slots=True)
class InPredicate:
    item: ColumnRef
    values: tuple[LiteralValue, ...]


@dataclass(frozen=True, slots=True)
class NullPredicate:
    column: ColumnRef
    is_null: bool = True


@dataclass(frozen=True, slots=True)
class IsNaNPredicate:
    column: ColumnRef


@dataclass(frozen=True, slots=True)
class StringPredicate:
    op: Literal["contains", "starts_with", "ends_with"]
    column: ColumnRef
    value: LiteralValue
    case_insensitive: bool = False
    match_nulls: bool = False


@dataclass(frozen=True, slots=True)
class NotPredicate:
    predicate: Predicate


@dataclass(frozen=True, slots=True)
class AndPredicate:
    items: tuple[Predicate, ...]


@dataclass(frozen=True, slots=True)
class OrPredicate:
    items: tuple[Predicate, ...]


Predicate = (
    ComparePredicate
    | InPredicate
    | NullPredicate
    | IsNaNPredicate
    | StringPredicate
    | NotPredicate
    | AndPredicate
    | OrPredicate
)


def and_predicates(*items: Predicate) -> Predicate:
    flattened: list[Predicate] = []
    for item in items:
        if isinstance(item, AndPredicate):
            flattened.extend(item.items)
        else:
            flattened.append(item)
    if len(flattened) == 1:
        return flattened[0]
    return AndPredicate(tuple(flattened))


def or_predicates(*items: Predicate) -> Predicate:
    flattened: list[Predicate] = []
    for item in items:
        if isinstance(item, OrPredicate):
            flattened.extend(item.items)
        else:
            flattened.append(item)
    if len(flattened) == 1:
        return flattened[0]
    return OrPredicate(tuple(flattened))


def render_predicate_text(predicate: Predicate) -> str:
    if isinstance(predicate, ComparePredicate):
        left = _render_value_text(predicate.left)
        right = _render_value_text(predicate.right)
        return f"{left} {predicate.op} {right}"
    if isinstance(predicate, InPredicate):
        values = ", ".join(_render_value_text(value) for value in predicate.values)
        return f"{predicate.item.name} in ({values})"
    if isinstance(predicate, NullPredicate):
        suffix = "is null" if predicate.is_null else "is not null"
        return f"{predicate.column.name} {suffix}"
    if isinstance(predicate, IsNaNPredicate):
        return f"{predicate.column.name} is NaN"
    if isinstance(predicate, StringPredicate):
        op = predicate.op.replace("_", " ")
        value = _render_value_text(predicate.value)
        base = f"{predicate.column.name} {op} {value}"
        if predicate.case_insensitive:
            base = f"{base} (ci)"
        if predicate.match_nulls:
            base = f"{base} or null"
        return base
    if isinstance(predicate, NotPredicate):
        return f"not ({render_predicate_text(predicate.predicate)})"
    if isinstance(predicate, AndPredicate):
        return " and ".join(_wrap_child_text(child, "and") for child in predicate.items)
    if isinstance(predicate, OrPredicate):
        return " or ".join(_wrap_child_text(child, "or") for child in predicate.items)
    raise TypeError(f"Unsupported predicate: {type(predicate)!r}")


def predicate_to_payload(predicate: Predicate) -> dict[str, Any]:
    if isinstance(predicate, ComparePredicate):
        return {
            "type": "compare",
            "op": predicate.op,
            "left": _value_to_payload(predicate.left),
            "right": _value_to_payload(predicate.right),
        }
    if isinstance(predicate, InPredicate):
        return {
            "type": "in",
            "item": _value_to_payload(predicate.item),
            "values": [_value_to_payload(value) for value in predicate.values],
        }
    if isinstance(predicate, NullPredicate):
        return {
            "type": "null",
            "column": _value_to_payload(predicate.column),
            "is_null": predicate.is_null,
        }
    if isinstance(predicate, IsNaNPredicate):
        return {
            "type": "nan",
            "column": _value_to_payload(predicate.column),
        }
    if isinstance(predicate, StringPredicate):
        return {
            "type": "string",
            "op": predicate.op,
            "column": _value_to_payload(predicate.column),
            "value": _value_to_payload(predicate.value),
            "case_insensitive": predicate.case_insensitive,
            "match_nulls": predicate.match_nulls,
        }
    if isinstance(predicate, NotPredicate):
        return {
            "type": "not",
            "predicate": predicate_to_payload(predicate.predicate),
        }
    if isinstance(predicate, AndPredicate):
        return {"type": "and", "items": [predicate_to_payload(item) for item in predicate.items]}
    if isinstance(predicate, OrPredicate):
        return {"type": "or", "items": [predicate_to_payload(item) for item in predicate.items]}
    raise TypeError(f"Unsupported predicate: {type(predicate)!r}")


def predicate_payload_to_text(payload: dict[str, Any]) -> str:
    try:
        rendered = json.dumps(payload, sort_keys=True)
    except Exception:
        return "<predicate>"
    return rendered


def _value_to_payload(value: ValueExpr) -> dict[str, Any]:
    if isinstance(value, ColumnRef):
        return {"type": "column", "name": value.name}
    if isinstance(value, LiteralValue):
        return {"type": "literal", "value": _serialize_literal(value.value)}
    raise TypeError(f"Unsupported value expression: {type(value)!r}")


def _serialize_literal(value: Any) -> Any:
    if isinstance(value, float) and math.isnan(value):
        return {"__type__": "nan"}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    try:
        json.dumps(value)
    except Exception:
        return {"__repr__": repr(value)}
    return value


def _render_value_text(value: ValueExpr) -> str:
    if isinstance(value, ColumnRef):
        return value.name
    if isinstance(value, LiteralValue):
        return repr(value.value)
    raise TypeError(f"Unsupported value expression: {type(value)!r}")


def _wrap_child_text(child: Predicate, operator: str) -> str:
    text = render_predicate_text(child)
    if isinstance(child, (AndPredicate, OrPredicate)):
        if operator == "and" and isinstance(child, AndPredicate):
            return text
        if operator == "or" and isinstance(child, OrPredicate):
            return text
        return f"({text})"
    return text


__all__ = [
    "AndPredicate",
    "ColumnRef",
    "ComparePredicate",
    "InPredicate",
    "IsNaNPredicate",
    "LiteralValue",
    "NotPredicate",
    "NullPredicate",
    "OrPredicate",
    "Predicate",
    "StringPredicate",
    "and_predicates",
    "or_predicates",
    "predicate_payload_to_text",
    "predicate_to_payload",
    "render_predicate_text",
]
