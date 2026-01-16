"""
Filter language compiler for Pulka.

This module handles the parsing and compilation of filter expressions to Polars
expressions, including AST validation and namespace resolution.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Sequence

import polars as pl

from ..core.predicate import (
    ColumnRef,
    ComparePredicate,
    InPredicate,
    IsNaNPredicate,
    LiteralValue,
    NotPredicate,
    NullPredicate,
    Predicate,
    StringPredicate,
    and_predicates,
    or_predicates,
)
from ..sheets.query_plan import normalized_columns_key


class FilterError(ValueError):
    """Raised when a filter expression cannot be parsed or evaluated."""


class ColumnNamespace:
    """Attribute/Item access helper that maps column names to Polars expressions."""

    def __init__(self, columns: Sequence[str]):
        self._columns = list(columns)
        self._column_set = set(columns)

    def __getattr__(self, name: str) -> pl.Expr:
        if name.startswith("_") or name not in self._column_set or not name.isidentifier():
            raise AttributeError(f"No column named '{name}'")
        return pl.col(name)

    def __getitem__(self, key: str) -> pl.Expr:
        if key not in self._column_set:
            raise KeyError(f"No column named '{key}'")
        return pl.col(key)

    def __dir__(self) -> list[str]:
        return sorted([c for c in self._columns if c.isidentifier()])

    @property
    def columns(self) -> Sequence[str]:
        return tuple(self._columns)


_FILTER_CACHE: dict[tuple[str, str], pl.Expr] = {}
_PREDICATE_CACHE: dict[tuple[str, str], Predicate | None] = {}
_PREDICATE_MISSING: object = object()


def compile_filter_expression(text: str, columns: Sequence[str]) -> pl.Expr:
    """Return a cached Polars expression for ``text`` and ``columns``."""

    normalized = text.strip()
    key = (normalized, normalized_columns_key(columns))
    expr = _FILTER_CACHE.get(key)
    if expr is None:
        expr = _compile_filter_expression(normalized, columns)
        _FILTER_CACHE[key] = expr
    return expr


def clear_filter_cache() -> None:
    """Clear the cached filter expressions."""

    _FILTER_CACHE.clear()
    _PREDICATE_CACHE.clear()


def compile_filter_predicate(text: str, columns: Sequence[str]) -> Predicate | None:
    """Return a cached predicate IR for ``text`` when supported."""

    normalized = text.strip()
    key = (normalized, normalized_columns_key(columns))
    cached = _PREDICATE_CACHE.get(key, _PREDICATE_MISSING)
    if cached is not _PREDICATE_MISSING:
        return cached  # type: ignore[return-value]
    predicate = _compile_filter_predicate(normalized, columns)
    _PREDICATE_CACHE[key] = predicate
    return predicate


_INDEX_NODE = getattr(ast, "Index", None)
_ALLOWED_FILTER_NODE_TYPES = (
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Call,
    ast.Attribute,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Subscript,
    ast.Slice,
    ast.keyword,
) + ((_INDEX_NODE,) if _INDEX_NODE is not None else ())


def _detect_precedence_issues(text: str) -> None:
    """Detect common operator precedence issues and provide helpful error messages."""
    # Pattern: comparison == literal & other_expr (without parentheses)
    # This will be parsed as: comparison == (literal & other_expr)
    pattern1 = re.compile(r"\b\w+(?:\.\w+)*\s*==\s*(?:True|False|\w+)\s*&\s*\w+")
    if pattern1.search(text):
        raise FilterError(
            f"Operator precedence issue detected in '{text}'. "
            "Use parentheses to clarify: (a == b) & (c op d)"
        )

    # Pattern: comparison == literal | other_expr (without parentheses)
    pattern2 = re.compile(r"\b\w+(?:\.\w+)*\s*==\s*(?:True|False|\w+)\s*\|\s*\w+")
    if pattern2.search(text):
        raise FilterError(
            f"Operator precedence issue detected in '{text}'. "
            "Use parentheses to clarify: (a == b) | (c op d)"
        )

    # Pattern: comparison != literal & other_expr (without parentheses)
    pattern3 = re.compile(r"\b\w+(?:\.\w+)*\s*!=\s*(?:True|False|\w+)\s*&\s*\w+")
    if pattern3.search(text):
        raise FilterError(
            f"Operator precedence issue detected in '{text}'. "
            "Use parentheses to clarify: (a != b) & (c op d)"
        )


def _validate_filter_ast(node: ast.AST, allowed_names: set[str]) -> None:
    extra_allowed = (ast.operator, ast.boolop, ast.unaryop, ast.cmpop)
    for child in ast.walk(node):
        if not isinstance(child, _ALLOWED_FILTER_NODE_TYPES + extra_allowed):
            raise FilterError("Unsupported syntax in filter expression")
        if isinstance(child, ast.Attribute):
            if child.attr.startswith("_"):
                raise FilterError("Attribute access starting with '_' is not allowed")
        elif isinstance(child, ast.Name) and child.id not in allowed_names:
            raise FilterError(f"Unknown name '{child.id}' in filter expression")


def _compile_filter_expression(text: str, columns: Sequence[str]) -> pl.Expr:
    namespace = ColumnNamespace(columns)

    # Check for common precedence issues before parsing
    _detect_precedence_issues(text)

    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise FilterError(f"Invalid filter syntax: {exc.msg}") from exc

    _validate_filter_ast(tree, {"c", "pl", "lit", "col", "True", "False", "None"})

    env = {
        "c": namespace,
        "pl": pl,
        "lit": pl.lit,
        "col": pl.col,
        "True": True,
        "False": False,
        "None": None,
    }

    try:
        compiled = eval(compile(tree, "<filter>", "eval"), {"__builtins__": {}}, env)
    except FilterError:
        raise
    except Exception as exc:
        raise FilterError(str(exc)) from exc

    if not isinstance(compiled, pl.Expr):
        raise FilterError("Filter expression must produce a Polars expression")
    return compiled


def _compile_filter_predicate(text: str, columns: Sequence[str]) -> Predicate | None:
    if not text:
        return None

    _detect_precedence_issues(text)

    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise FilterError(f"Invalid filter syntax: {exc.msg}") from exc

    _validate_filter_ast(tree, {"c", "pl", "lit", "col", "True", "False", "None"})

    if _uses_pl_namespace(tree):
        return None

    compiler = _PredicateCompiler(columns)
    return compiler.compile(tree.body)


def _uses_pl_namespace(node: ast.AST) -> bool:
    return any(isinstance(child, ast.Name) and child.id == "pl" for child in ast.walk(node))


class _PredicateCompiler:
    def __init__(self, columns: Sequence[str]) -> None:
        self._columns = set(columns)

    def compile(self, node: ast.AST) -> Predicate | None:
        if isinstance(node, ast.Expression):
            return self.compile(node.body)
        if isinstance(node, ast.BoolOp):
            return self._compile_boolop(node)
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.BitAnd, ast.BitOr)):
            return self._compile_binop(node)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.Not, ast.Invert)):
            return self._compile_unary(node)
        if isinstance(node, ast.Compare):
            return self._compile_compare(node)
        if isinstance(node, ast.Call):
            return self._compile_call(node)
        return None

    def _compile_boolop(self, node: ast.BoolOp) -> Predicate | None:
        items: list[Predicate] = []
        for value in node.values:
            compiled = self.compile(value)
            if compiled is None:
                return None
            items.append(compiled)
        if isinstance(node.op, ast.And):
            return and_predicates(*items)
        if isinstance(node.op, ast.Or):
            return or_predicates(*items)
        return None

    def _compile_binop(self, node: ast.BinOp) -> Predicate | None:
        left = self.compile(node.left)
        right = self.compile(node.right)
        if left is None or right is None:
            return None
        if isinstance(node.op, ast.BitAnd):
            return and_predicates(left, right)
        if isinstance(node.op, ast.BitOr):
            return or_predicates(left, right)
        return None

    def _compile_unary(self, node: ast.UnaryOp) -> Predicate | None:
        operand = self.compile(node.operand)
        if operand is None:
            return None
        return NotPredicate(operand)

    def _compile_compare(self, node: ast.Compare) -> Predicate | None:
        if len(node.ops) != 1 or len(node.comparators) != 1:
            return None
        left = self._compile_value(node.left)
        right = self._compile_value(node.comparators[0])
        if left is None or right is None:
            return None
        if isinstance(left, LiteralValue) and left.value is None:
            return None
        if isinstance(right, LiteralValue) and right.value is None:
            return None

        op = node.ops[0]
        if isinstance(op, ast.Eq):
            return ComparePredicate("==", left, right)
        if isinstance(op, ast.NotEq):
            return ComparePredicate("!=", left, right)
        if isinstance(op, ast.Lt):
            return ComparePredicate("<", left, right)
        if isinstance(op, ast.LtE):
            return ComparePredicate("<=", left, right)
        if isinstance(op, ast.Gt):
            return ComparePredicate(">", left, right)
        if isinstance(op, ast.GtE):
            return ComparePredicate(">=", left, right)
        return None

    def _compile_call(self, node: ast.Call) -> Predicate | None:
        if not isinstance(node.func, ast.Attribute):
            return None

        method = node.func.attr
        target = node.func.value

        compare_ops = {
            "eq": "==",
            "ne": "!=",
            "gt": ">",
            "ge": ">=",
            "lt": "<",
            "le": "<=",
        }
        if method in compare_ops:
            if len(node.args) != 1 or node.keywords:
                return None
            column = self._compile_column(target)
            if column is None:
                return None
            value = self._compile_value(node.args[0])
            if value is None:
                return None
            if isinstance(value, LiteralValue) and value.value is None:
                return None
            return ComparePredicate(compare_ops[method], column, value)

        if method in {"is_true", "is_false"}:
            if node.args or node.keywords:
                return None
            column = self._compile_column(target)
            if column is None:
                return None
            return ComparePredicate(
                "==",
                column,
                LiteralValue(method == "is_true"),
            )

        if method in {"is_nan", "is_not_nan"}:
            if node.args or node.keywords:
                return None
            column = self._compile_column(target)
            if column is None:
                return None
            predicate: Predicate = IsNaNPredicate(column)
            if method == "is_not_nan":
                return NotPredicate(predicate)
            return predicate

        if method == "is_between":
            if len(node.args) != 2:
                return None
            closed = "both"
            for keyword in node.keywords:
                if keyword.arg != "closed":
                    return None
                if not isinstance(keyword.value, ast.Constant):
                    return None
                if not isinstance(keyword.value.value, str):
                    return None
                closed = keyword.value.value
            if closed not in {"both", "left", "right", "none"}:
                return None
            column = self._compile_column(target)
            if column is None:
                return None
            lower = self._compile_value(node.args[0])
            upper = self._compile_value(node.args[1])
            if lower is None or upper is None:
                return None
            if isinstance(lower, LiteralValue) and lower.value is None:
                return None
            if isinstance(upper, LiteralValue) and upper.value is None:
                return None
            lower_op = ">=" if closed in {"both", "left"} else ">"
            upper_op = "<=" if closed in {"both", "right"} else "<"
            return and_predicates(
                ComparePredicate(lower_op, column, lower),
                ComparePredicate(upper_op, column, upper),
            )

        if method in {"is_null", "is_not_null"}:
            if node.args or node.keywords:
                return None
            column = self._compile_column(target)
            if column is None:
                return None
            return NullPredicate(column, is_null=method == "is_null")

        if method == "is_in":
            if len(node.args) != 1 or node.keywords:
                return None
            column = self._compile_column(target)
            if column is None:
                return None
            values = _compile_literal_sequence(node.args[0])
            if values is None:
                return None
            return InPredicate(column, tuple(values))

        string_method = _normalize_string_method(method)
        if string_method and isinstance(target, ast.Attribute) and target.attr == "str":
            column = self._compile_column(target.value)
            if column is None:
                return None
            return self._compile_string_predicate(node, column, string_method)

        return None

    def _compile_string_predicate(
        self,
        node: ast.Call,
        column: ColumnRef,
        method: str,
    ) -> Predicate | None:
        pattern_node = _extract_pattern_node(node)
        if pattern_node is None:
            return None
        literal = _compile_literal_value(pattern_node)
        if literal is None or not isinstance(literal.value, str):
            return None

        case_sensitive: bool | None = None
        literal_flag: bool | None = None
        for keyword in node.keywords:
            if keyword.arg is None:
                return None
            if keyword.arg in {"case_sensitive", "case"}:
                value = _compile_literal_bool(keyword.value)
                if value is None:
                    return None
                case_sensitive = value
                continue
            if keyword.arg == "literal":
                value = _compile_literal_bool(keyword.value)
                if value is None:
                    return None
                literal_flag = value
                continue
            if keyword.arg == "pattern":
                continue
            return None

        if method == "contains":
            if literal_flag is not True:
                return None
        else:
            if literal_flag is not None:
                return None

        case_insensitive = False if case_sensitive is None else not case_sensitive
        return StringPredicate(
            method,
            column,
            literal,
            case_insensitive=case_insensitive,
        )

    def _compile_column(self, node: ast.AST) -> ColumnRef | None:
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id != "c":
                return None
            name = node.attr
            if name.startswith("_") or not name.isidentifier() or name not in self._columns:
                raise FilterError(f"No column named '{name}'")
            return ColumnRef(name)

        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
            if node.value.id != "c":
                return None
            key = _extract_subscript_key(node.slice)
            if not isinstance(key, str):
                return None
            if key not in self._columns:
                raise FilterError(f"No column named '{key}'")
            return ColumnRef(key)

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id != "col":
                return None
            if len(node.args) != 1 or node.keywords:
                return None
            arg = node.args[0]
            if not isinstance(arg, ast.Constant) or not isinstance(arg.value, str):
                return None
            if arg.value not in self._columns:
                raise FilterError(f"No column named '{arg.value}'")
            return ColumnRef(arg.value)

        return None

    def _compile_value(self, node: ast.AST) -> ColumnRef | LiteralValue | None:
        column = self._compile_column(node)
        if column is not None:
            return column
        return _compile_literal_value(node)


def _extract_subscript_key(node: ast.AST) -> object | None:
    if _INDEX_NODE is not None and isinstance(node, _INDEX_NODE):
        return _extract_subscript_key(node.value)
    if isinstance(node, ast.Constant):
        return node.value
    return None


def _compile_literal_value(node: ast.AST) -> LiteralValue | None:
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, (str, int, float, bool)) or value is None:
            return LiteralValue(value)
        return None
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, (ast.UAdd, ast.USub))
        and isinstance(node.operand, ast.Constant)
        and isinstance(node.operand.value, (int, float))
    ):
        value = node.operand.value
        if isinstance(node.op, ast.USub):
            value = -value
        return LiteralValue(value)
    return None


def _compile_literal_bool(node: ast.AST) -> bool | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return node.value
    return None


def _compile_literal_sequence(node: ast.AST) -> tuple[LiteralValue, ...] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    values: list[LiteralValue] = []
    for item in node.elts:
        literal = _compile_literal_value(item)
        if literal is None:
            return None
        values.append(literal)
    return tuple(values)


def _normalize_string_method(method: str) -> str | None:
    if method == "contains":
        return "contains"
    if method in {"starts_with", "startswith"}:
        return "starts_with"
    if method in {"ends_with", "endswith"}:
        return "ends_with"
    return None


def _extract_pattern_node(node: ast.Call) -> ast.AST | None:
    if node.args:
        if len(node.args) != 1:
            return None
        return node.args[0]
    for keyword in node.keywords:
        if keyword.arg == "pattern":
            return keyword.value
    return None
