"""Helpers for deriving sheet-specific UI traits."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SheetTraits:
    """Structured hints derived from optional sheet attributes."""

    is_file_browser: bool = False
    is_summary_view: bool = False
    is_transpose_view: bool = False
    insight_soft_disabled: bool = False
    preferred_fill_column: str | None = None
    display_path: str | None = None


def resolve_sheet_traits(
    sheet: object | None,
    *,
    columns: Sequence[str] | None = None,
    path_fallback: str | None = None,
) -> SheetTraits:
    if sheet is None:
        return SheetTraits()

    is_file_browser = bool(getattr(sheet, "is_file_browser", False))
    preferred_fill_column = resolve_preferred_fill_column(sheet, columns)
    display_path = None
    if is_file_browser:
        display_path = resolve_display_path(sheet, fallback=path_fallback)

    return SheetTraits(
        is_file_browser=is_file_browser,
        is_summary_view=bool(getattr(sheet, "is_summary_view", False)),
        is_transpose_view=bool(getattr(sheet, "is_transpose_view", False)),
        insight_soft_disabled=bool(getattr(sheet, "is_insight_soft_disabled", False)),
        preferred_fill_column=preferred_fill_column,
        display_path=display_path,
    )


def resolve_sheet_schema(sheet: object | None) -> Mapping[str, Any]:
    if sheet is None:
        return {}
    schema = getattr(sheet, "schema", None)
    if isinstance(schema, Mapping):
        return dict(schema)
    schema_dict = getattr(sheet, "schema_dict", None)
    if callable(schema_dict):
        try:
            resolved = schema_dict()
        except Exception:
            return {}
        if isinstance(resolved, Mapping):
            return dict(resolved)
    return {}


def resolve_preferred_fill_column(
    sheet: object | None,
    columns: Sequence[str] | None = None,
) -> str | None:
    if sheet is None:
        return None
    preferred = None
    preferred_attr = getattr(sheet, "preferred_fill_column", None)
    if callable(preferred_attr):
        try:
            preferred = preferred_attr()
        except Exception:
            preferred = None
    elif preferred_attr is not None:
        preferred = preferred_attr
    if preferred is None:
        preferred = getattr(sheet, "fill_column_name", None)
    if isinstance(preferred, str) and (columns is None or preferred in columns):
        return preferred
    return None


def resolve_display_path(sheet: object | None, *, fallback: str | None = None) -> str | None:
    if sheet is None:
        return fallback
    display_path = getattr(sheet, "display_path", None)
    if not display_path:
        directory = getattr(sheet, "directory", None)
        if directory is not None:
            display_path = str(directory)
    if not display_path and fallback is not None:
        display_path = fallback
    if display_path is None:
        return None
    return str(display_path)


def resolve_insight_flags(sheet: object | None) -> tuple[bool, bool]:
    traits = resolve_sheet_traits(sheet)
    allowed = not traits.is_file_browser
    soft_disabled = (
        traits.is_summary_view or traits.is_transpose_view or traits.insight_soft_disabled
    )
    return allowed, soft_disabled


def is_row_selectable(sheet: object | None, row_index: int) -> bool:
    if sheet is None:
        return True
    selectable_fn = getattr(sheet, "is_row_selectable", None)
    if callable(selectable_fn):
        try:
            return bool(selectable_fn(row_index))
        except Exception:
            return True
    reason_fn = getattr(sheet, "selection_block_reason", None)
    if callable(reason_fn):
        try:
            reason = reason_fn(row_index)
        except Exception:
            return True
        if isinstance(reason, str) and reason:
            return False
    return True


def selection_block_reason(sheet: object | None, row_index: int) -> str | None:
    if sheet is None:
        return None
    reason_fn = getattr(sheet, "selection_block_reason", None)
    if callable(reason_fn):
        try:
            reason = reason_fn(row_index)
        except Exception:
            return None
        if isinstance(reason, str) and reason:
            return reason
        return None
    selectable_fn = getattr(sheet, "is_row_selectable", None)
    if callable(selectable_fn):
        try:
            selectable = selectable_fn(row_index)
        except Exception:
            return None
        if not selectable:
            return "row is not selectable"
    return None


__all__ = [
    "SheetTraits",
    "resolve_display_path",
    "resolve_insight_flags",
    "resolve_preferred_fill_column",
    "resolve_sheet_schema",
    "resolve_sheet_traits",
    "is_row_selectable",
    "selection_block_reason",
]
