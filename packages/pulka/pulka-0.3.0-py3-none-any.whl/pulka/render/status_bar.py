# mypy: ignore-errors

"""
Status bar rendering for Pulka.

This module provides functions for rendering the status bar that displays
metadata about the current view including filename, row position, column info,
filters, sort, and memory usage.
"""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from ..utils import lazy_imports

if TYPE_CHECKING:
    StyleAndTextTuples = list[tuple[str, str]]  # type: ignore[assignment]
else:  # pragma: no cover - runtime import helper
    StyleAndTextTuples = lazy_imports.prompt_toolkit_style_and_text_tuples()

from ..core.formatting import (
    _format_large_number_compact,
    _format_number_with_thousands_separator,
    _simplify_dtype_text,
)
from ..core.sheet_traits import (
    resolve_display_path,
    resolve_sheet_schema,
    resolve_sheet_traits,
)
from ..testing import is_test_mode
from .style_resolver import get_active_style_resolver
from .styles import apply_style

# Constants for formatting and truncation
_LARGE_NUMBER_THRESHOLD = 999999  # Threshold for compact number formatting
_MEMORY_THRESHOLD = 1000000  # Threshold for memory usage interpretation


def sample_memory_usage(*, test_mode: bool) -> int | None:
    """Return current memory usage in MB with the same semantics as the status bar."""

    if test_mode:
        return 120

    try:
        import resource
    except Exception:  # pragma: no cover - resource module unavailable
        return None

    try:
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:  # pragma: no cover - getrusage failures are best-effort
        return None

    if usage > _MEMORY_THRESHOLD:
        return max(1, int(usage / 1024 / 1024))
    return max(1, int(usage / 1024))


def _truncate_middle(text: str, max_length: int) -> str:
    """Return ``text`` truncated around the middle to fit ``max_length``."""

    if max_length <= 0:
        return ""
    if len(text) <= max_length:
        return text

    ellipsis = "…"
    if max_length <= len(ellipsis):
        return ellipsis[:max_length]

    slice_length = max_length - len(ellipsis)
    front = (slice_length + 1) // 2
    back = slice_length // 2
    return f"{text[:front]}{ellipsis}{text[-back:] if back else ''}"


def _segments_length(segments: Sequence[tuple[str, str]]) -> int:
    return sum(len(text) for _, text in segments)


def _merge_segments(segments: Sequence[tuple[str, str]]) -> list[tuple[str, str]]:
    merged: list[tuple[str, str]] = []
    for style, text in segments:
        if not text:
            continue
        if merged and merged[-1][0] == style:
            merged[-1] = (style, merged[-1][1] + text)
        else:
            merged.append((style, text))
    return merged


def _slice_segments(
    segments: Sequence[tuple[str, str]],
    start: int,
    end: int,
) -> list[tuple[str, str]]:
    if start >= end:
        return []
    result: list[tuple[str, str]] = []
    pos = 0
    for style, text in segments:
        if pos >= end:
            break
        next_pos = pos + len(text)
        if next_pos <= start:
            pos = next_pos
            continue
        slice_start = max(0, start - pos)
        slice_end = min(len(text), end - pos)
        chunk = text[slice_start:slice_end]
        if chunk:
            if result and result[-1][0] == style:
                result[-1] = (style, result[-1][1] + chunk)
            else:
                result.append((style, chunk))
        pos = next_pos
    return result


def _truncate_segments_middle(
    segments: Sequence[tuple[str, str]],
    max_length: int,
    *,
    ellipsis_style: str,
) -> list[tuple[str, str]]:
    if max_length <= 0:
        return []
    total = _segments_length(segments)
    if total <= max_length:
        return list(segments)

    ellipsis = "…"
    if max_length <= len(ellipsis):
        return [(ellipsis_style, ellipsis[:max_length])]

    slice_length = max_length - len(ellipsis)
    front = (slice_length + 1) // 2
    back = slice_length // 2
    front_segments = _slice_segments(segments, 0, front)
    back_segments = _slice_segments(segments, total - back, total)
    return _merge_segments([*front_segments, (ellipsis_style, ellipsis), *back_segments])


def render_status_line(
    v: Any,
    *,
    test_mode: bool | None = None,
    resource_sample: int | None = None,
) -> StyleAndTextTuples:
    """Render a ``prompt_toolkit`` fragment representing the status bar."""

    if test_mode is None:
        test_mode = is_test_mode()

    if not hasattr(v, "columns") or not hasattr(v, "cur_col"):
        raise TypeError(
            f"Expected Viewer-like object with columns and cur_col attributes, got {type(v)}"
        )

    sheet = getattr(v, "sheet", None)
    traits = resolve_sheet_traits(sheet)
    columns = list(getattr(v, "columns", []) or [])
    if columns:
        cur_index = min(max(int(getattr(v, "cur_col", 0)), 0), len(columns) - 1)
        current_col = str(columns[cur_index])
        sheet_schema = resolve_sheet_schema(sheet)
        schema = getattr(v, "schema", None) or sheet_schema
        col_dtype = schema.get(columns[cur_index], "unknown")
    else:
        current_col = "no columns"
        col_dtype = "N/A"

    total_rows = getattr(v, "_total_rows", None)
    row_count_stale = bool(getattr(v, "_row_count_stale", False))
    if row_count_stale or total_rows is None:
        ensure_total_rows = getattr(v, "_ensure_total_rows", None)
        if callable(ensure_total_rows):
            total_rows = ensure_total_rows()
        elif hasattr(v, "sheet") and hasattr(v.sheet, "__len__"):
            with contextlib.suppress(Exception):
                total_rows = len(v.sheet)
        row_count_stale = bool(getattr(v, "_row_count_stale", False))

    current_row_formatted = _format_number_with_thousands_separator(
        int(getattr(v, "cur_row", 0)) + 1
    )
    pending_row_count = getattr(v, "_row_count_future", None)
    display_pending = bool(getattr(v, "_row_count_display_pending", False))
    pending = row_count_stale or display_pending or pending_row_count is not None
    if total_rows is not None:
        sheet_id = getattr(getattr(v, "sheet", None), "sheet_id", None)
        if not (pending and sheet_id is not None):
            threshold = getattr(v, "_status_large_number_threshold", _LARGE_NUMBER_THRESHOLD)
            if total_rows > threshold:
                rows_total_text = _format_large_number_compact(total_rows)
            else:
                rows_total_text = _format_number_with_thousands_separator(total_rows)
        else:
            rows_total_text = "≈"
    else:
        rows_total_text = "≈" if pending else "?"

    if resource_sample is None:
        mem_mb = sample_memory_usage(test_mode=test_mode)
    else:
        mem_mb = resource_sample

    browser_path: str | None = None
    if traits.is_file_browser:
        fallback = getattr(sheet, "sheet_id", None) or getattr(v, "_source_path", None)
        fallback_text = str(fallback) if fallback is not None else None
        browser_path = resolve_display_path(sheet, fallback=fallback_text)

    simple_dtype = _simplify_dtype_text(col_dtype)
    status_message = getattr(v, "status_message", None)
    status_segment: str | None = None
    if status_message:
        normalised_status = status_message.strip().lower()
        if "error" in normalised_status or not normalised_status.startswith(
            ("filter", "filters", "sql filter", "sort")
        ):
            status_segment = status_message

    left_parts: list[str] = []
    if browser_path:
        left_parts.append(browser_path)
    else:
        left_parts.append(f"row {current_row_formatted} / col {current_col}[{simple_dtype}]")

    left_segments: list[tuple[str, str]] = []
    if test_mode:
        base_style = ""
        status_style = ""
    else:
        resolver = get_active_style_resolver()
        base_style = resolver.prompt_toolkit_style_for_classes(("status",))
        severity = getattr(v, "status_severity", None)
        status_classes = ("status", f"status.{severity}") if severity else ("status",)
        status_style = resolver.prompt_toolkit_style_for_classes(status_classes)

    for idx, part in enumerate(left_parts):
        if idx:
            left_segments.append((base_style, " • "))
        left_segments.append((base_style, part))
    if status_segment:
        if left_segments:
            left_segments.append((base_style, " • "))
        left_segments.append((status_style or base_style, status_segment))

    total_columns = len(columns)
    hidden_column_count = 0
    hidden_columns = getattr(v, "hidden_columns", None)
    if hidden_columns:
        hidden_column_count = len(tuple(hidden_columns))
    else:
        hidden_names = getattr(v, "_hidden_cols", None)
        if hidden_names and columns:
            hidden_set = set(hidden_names)
            hidden_column_count = sum(1 for name in columns if name in hidden_set)

    non_hidden_columns = total_columns - hidden_column_count
    if non_hidden_columns <= 0:
        visible_columns = list(getattr(v, "visible_cols", []) or [])
        visible_count = len(visible_columns)
        non_hidden_columns = visible_count or total_columns or visible_count

    right_parts = [f"depth {getattr(v, 'stack_depth', 0)}"]
    right_parts.append(f"{rows_total_text}×{max(0, non_hidden_columns)}")
    if mem_mb is not None:
        right_parts.append(f"mem {mem_mb}MB")
    right_text = " • ".join(right_parts)

    width_hint = getattr(v, "status_width_chars", None)
    if width_hint is None:
        width_hint = getattr(v, "view_width_chars", 80)
    width = max(20, int(width_hint or 0))
    right_text = _truncate_middle(right_text, width)
    available_left = max(0, width - len(right_text))
    if right_text and available_left > 0:
        available_left -= 1
    left_segments = (
        _truncate_segments_middle(left_segments, available_left, ellipsis_style=base_style)
        if available_left > 0
        else []
    )
    left_len = _segments_length(left_segments)

    if right_text:
        if left_len:
            gap = max(1, width - left_len - len(right_text))
            segments = [*left_segments, (base_style, " " * gap), (base_style, right_text)]
        else:
            pad = max(0, width - len(right_text))
            segments = [(base_style, " " * pad), (base_style, right_text)]
    else:
        segments = list(left_segments)

    total_len = _segments_length(segments)
    if total_len < width:
        segments.append((base_style, " " * (width - total_len)))
    elif total_len > width:
        segments = _slice_segments(segments, 0, width)
    return _merge_segments(segments)


def render_status_line_text(v: Any, *, test_mode: bool | None = None) -> str:
    """Return an ANSI string fallback for tests and non-PTK paths."""

    fragments = render_status_line(v, test_mode=test_mode)
    if not fragments:
        return ""

    test_mode_flag = is_test_mode() if test_mode is None else test_mode
    parts: list[str] = []
    for style, part in fragments:
        parts.append(apply_style(part, style or None, test_mode=test_mode_flag))
    return "".join(parts)
