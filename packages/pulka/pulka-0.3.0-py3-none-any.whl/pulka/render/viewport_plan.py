"""Viewport planning for tabular renders.

This module computes a UI-neutral representation of the visible portion of a
table so renderers (Rich, prompt_toolkit, headless) can share sizing and cell
formatting logic without duplicating width calculations.
"""

from __future__ import annotations

import contextlib
import math
from collections import deque
from collections.abc import Hashable, Sequence
from dataclasses import dataclass, replace
from time import monotonic_ns, perf_counter_ns
from typing import TYPE_CHECKING, Any, Literal

from ..core.engine.contracts import TableSliceLike
from ..core.formatting import _is_numeric_dtype
from ..core.sheet_traits import resolve_sheet_schema, resolve_sheet_traits
from .decimal_alignment import apply_decimal_alignment, compute_decimal_alignment
from .display import (
    display_width,
    pad_left_display,
    pad_right_display,
    truncate_grapheme_safe,
    truncate_middle_grapheme_safe,
)

if TYPE_CHECKING:
    from ..core.viewer import Viewer


@dataclass(slots=True)
class Cell:
    """Rendered cell payload for a viewport column/row intersection."""

    text: str
    truncated: bool
    role: Literal["header", "body"]
    active_row: bool
    active_col: bool
    active_cell: bool
    selected_row: bool
    numeric: bool
    is_null: bool


@dataclass(slots=True)
class _ColumnMeta:
    """Internal helper metadata for planning column layout."""

    name: str
    dtype: Any
    is_numeric: bool
    has_nulls: bool
    min_width: int
    original_width: int
    header_active: bool
    is_sorted: bool
    is_frozen: bool


@dataclass(slots=True)
class ColumnPlan:
    """Metadata for a visible column within the viewport."""

    name: str
    header_label: str
    width: int
    min_width: int
    original_width: int
    is_numeric: bool
    has_nulls: bool
    header_active: bool
    is_sorted: bool


@dataclass(slots=True)
class ViewportPlan:
    """Collection of visible cells and sizing metadata for a table viewport."""

    columns: list[ColumnPlan]
    frozen_boundary_idx: int | None
    rows: int
    row_offset: int
    col_offset: int
    has_left_overflow: bool
    has_right_overflow: bool
    cells: list[list[Cell]]
    active_row_index: int
    row_positions: tuple[int, ...] | None = None
    formatting_skipped: bool = False


@dataclass(slots=True)
class _BodyRowCache:
    key: tuple[Any, ...]
    positions: tuple[int, ...]
    rows: list[list[Cell]]
    active_row: int | None


@dataclass(slots=True)
class _FormattedColumnCache:
    key: tuple[Any, ...]
    columns: dict[tuple[str, int], Sequence[str]]


@dataclass(slots=True)
class _FormattedCellCache:
    key: tuple[Any, ...]
    max_rows: int
    rows: dict[int, dict[tuple[str, int], str]]
    order: deque[int]


@dataclass(slots=True)
class _ViewportLayout:
    columns: list[str]
    column_meta: list[_ColumnMeta]
    column_widths: list[int]
    header_labels: list[str]
    header_label_widths: list[int]
    frozen_boundary_idx: int | None
    fetch_columns: list[str]
    has_left_overflow: bool
    has_right_overflow: bool
    is_file_browser: bool


@dataclass(slots=True)
class _LayoutCache:
    key: tuple[Any, ...]
    layout: _ViewportLayout


def _retag_cached_row(row_cells: list[Cell], *, active: bool) -> list[Cell]:
    if not row_cells:
        return []
    if active:
        return [replace(cell, active_row=True, active_cell=cell.active_col) for cell in row_cells]
    return [replace(cell, active_row=False, active_cell=False) for cell in row_cells]


def _should_defer_selection_fetch(viewer: Viewer, now_ns: int) -> bool:
    try:
        delay_ns = int(getattr(viewer, "_selection_filter_idle_ns", 150_000_000))
    except (TypeError, ValueError):  # pragma: no cover - defensive
        delay_ns = 150_000_000
    delay_ns = max(0, delay_ns)

    last_event = getattr(viewer, "_last_velocity_event_ns", None)
    deadline = getattr(viewer, "_selection_fetch_defer_until_ns", None)

    if last_event is not None and now_ns - last_event < delay_ns:
        viewer._selection_fetch_defer_until_ns = now_ns + delay_ns
        return True
    if deadline is not None and now_ns < deadline:
        return True

    viewer._selection_fetch_defer_until_ns = None
    return False


def fetch_visible_for_viewer(viewer: Viewer) -> TableSliceLike:
    """Return the visible slice for ``viewer`` honouring column visibility."""

    if hasattr(viewer, "visible_cols") and viewer.visible_cols:
        cols = list(viewer.visible_cols)
    else:
        cols = list(viewer.columns)
    return viewer.get_visible_table_slice(cols)


def _compute_fetch_columns(
    viewer: Viewer,
    *,
    visible_column_names: Sequence[str],
    viewer_columns: Sequence[str],
    frozen_names: Sequence[str],
    hidden_names: set[str],
) -> list[str]:
    """Return the column set to fetch for a viewport render.

    Horizontal scrolling tends to shift the visible column list by a single column per tick.
    Fetching exactly the visible columns would churn the row cache (keyed by the column tuple),
    triggering repeated engine slice fetches. To keep scroll smooth, we fetch a stable superset
    window around the visible scrollable columns and only recompute that window when the
    viewport nears its edges (hysteresis).
    """

    try:
        overscan = int(getattr(viewer, "_hscroll_fetch_overscan_cols", 4))
    except Exception:  # pragma: no cover - defensive
        overscan = 4
    if overscan <= 0:
        return list(visible_column_names)

    frozen_set = set(frozen_names)
    scrollable: list[str] = [
        name for name in viewer_columns if name not in hidden_names and name not in frozen_set
    ]
    if not scrollable:
        return list(visible_column_names)

    pos_by_name = {name: idx for idx, name in enumerate(scrollable)}
    visible_positions = [
        pos_by_name[name]
        for name in visible_column_names
        if name not in hidden_names and name not in frozen_set and name in pos_by_name
    ]
    if not visible_positions:
        return list(visible_column_names)

    first_pos = min(visible_positions)
    last_pos = max(visible_positions)

    window = getattr(viewer, "_hscroll_fetch_window", None)
    win_start: int
    win_end: int
    if (
        not isinstance(window, tuple)
        or len(window) != 2
        or not all(isinstance(item, int) for item in window)
    ):
        win_start = max(0, first_pos - overscan)
        win_end = min(len(scrollable) - 1, last_pos + overscan)
    else:
        win_start, win_end = window
        win_start = max(0, min(win_start, len(scrollable) - 1))
        win_end = max(0, min(win_end, len(scrollable) - 1))
        if win_start > win_end:
            win_start, win_end = win_end, win_start

        margin = max(1, overscan // 2)
        if first_pos < win_start + margin or last_pos > win_end - margin:
            win_start = max(0, first_pos - overscan)
            win_end = min(len(scrollable) - 1, last_pos + overscan)

    viewer._hscroll_fetch_window = (win_start, win_end)  # type: ignore[attr-defined]

    requested: list[str] = list(frozen_names)
    requested.extend(scrollable[win_start : win_end + 1])

    # Ensure we always include the visible columns (e.g. if frozen/hidden state shifts).
    seen: set[str] = set()
    final: list[str] = []
    for name in requested:
        if name in seen or name in hidden_names:
            continue
        final.append(name)
        seen.add(name)
    for name in visible_column_names:
        if name in seen:
            continue
        final.append(name)
        seen.add(name)

    return final


def _sort_directions(viewer: Viewer) -> dict[str, bool]:
    """Return a mapping of column name to descending flag."""

    sort_map: dict[str, bool] = {}
    current_plan = None
    with contextlib.suppress(Exception):
        current_plan = viewer._current_plan()

    sort_entries = getattr(current_plan, "sort", None)
    if sort_entries:
        for entry in sort_entries:
            try:
                column, desc = entry
            except Exception:
                continue
            sort_map[str(column)] = bool(desc)
        return sort_map

    sort_col = getattr(viewer, "sort_col", None)
    if sort_col is not None:
        sort_map[str(sort_col)] = not bool(getattr(viewer, "sort_asc", True))
    return sort_map


def _header_label_for_column(column_name: str, sort_map: dict[str, bool]) -> str:
    """Return the header label prefixed with the sort indicator."""

    indicator = " "
    desc = sort_map.get(column_name)
    if desc is not None:
        indicator = "↓" if desc else "↑"
    return f"{indicator}{column_name}"


def _table_border_overhead(column_count: int) -> int:
    """Return the width contribution of table borders and separators."""

    if column_count <= 0:
        return 0
    return column_count + 1


def _compute_horizontal_overflow(
    viewer: Viewer,
    *,
    visible_column_names: Sequence[str],
    frozen_names: set[str],
) -> tuple[bool, bool]:
    """Return whether scrollable columns exist to the left/right of the viewport."""

    hidden = set(getattr(viewer, "_hidden_cols", set()) or ())
    columns = list(getattr(viewer, "columns", ()))
    scrollable_indices = [
        idx for idx, name in enumerate(columns) if name not in hidden and name not in frozen_names
    ]
    if not scrollable_indices:
        return False, False

    visible_set = set(visible_column_names)
    visible_scrollable_indices = [idx for idx in scrollable_indices if columns[idx] in visible_set]

    first_scrollable_idx = (
        viewer._first_scrollable_col_index()
        if hasattr(viewer, "_first_scrollable_col_index")
        else len(frozen_names)
    )
    scroll_start = max(getattr(viewer, "col0", 0), first_scrollable_idx)
    min_visible = visible_scrollable_indices[0] if visible_scrollable_indices else scroll_start
    max_visible = visible_scrollable_indices[-1] if visible_scrollable_indices else scroll_start - 1

    has_left_overflow = any(idx < min_visible for idx in scrollable_indices)
    has_right_overflow = any(idx > max_visible for idx in scrollable_indices)
    if getattr(viewer, "_has_partial_column", False):
        has_right_overflow = True

    return has_left_overflow, has_right_overflow


def _shrink_widths_to_fit(
    widths: list[int],
    minimums: list[int],
    target_total: int,
) -> list[int]:
    """Reduce widths while respecting per-column minimums."""

    if not widths or target_total <= 0:
        return widths

    total = sum(widths)
    if total <= target_total:
        return widths

    overflow = total - target_total
    while overflow > 0:
        slack = [(idx, w - minimums[idx]) for idx, w in enumerate(widths)]
        slack = [item for item in slack if item[1] > 0]
        if not slack:
            break

        share = max(1, overflow // len(slack))
        for idx, available in slack:
            delta = min(available, share, overflow)
            if delta <= 0:
                continue
            widths[idx] -= delta
            overflow -= delta
            if overflow <= 0:
                break

    return widths


def _allocate_widths(
    widths: list[int],
    caps: list[int],
    weights: list[int],
    remaining: int,
) -> int:
    """Grow ``widths`` toward ``caps`` using ``weights`` while columns remain."""

    if remaining <= 0:
        return 0

    size = len(widths)
    while remaining > 0:
        eligible = [idx for idx in range(size) if widths[idx] < caps[idx]]
        if not eligible:
            break

        total_weight = sum(max(0, weights[idx]) for idx in eligible)
        if total_weight <= 0:
            total_weight = len(eligible)
            weight_map = dict.fromkeys(eligible, 1)
        else:
            weight_map = {idx: max(0, weights[idx]) for idx in eligible}

        allocated = 0
        for idx in eligible:
            cap = caps[idx]
            if widths[idx] >= cap:
                continue
            weight = weight_map[idx] or 0
            if weight <= 0:
                continue
            share = int(remaining * weight / total_weight)
            gap = cap - widths[idx]
            if share <= 0:
                share = 1
            share = min(gap, share)
            if share <= 0:
                continue
            widths[idx] += share
            remaining -= share
            allocated += share
            if remaining <= 0:
                break

        if allocated == 0:
            # Fallback: allocate single columns in priority order to avoid stalls.
            eligible.sort(key=lambda idx: (-(weight_map[idx] or 0), idx))
            for idx in eligible:
                if remaining <= 0:
                    break
                if widths[idx] >= caps[idx]:
                    continue
                widths[idx] += 1
                remaining -= 1
            if remaining > 0 and not any(widths[idx] < caps[idx] for idx in eligible):
                break

    return remaining


def _sampled_column_width(column: Any) -> int:
    """Return a padding-aware width based on visible values in ``column``."""

    try:
        values = getattr(column, "values", ())
    except Exception:
        return 0

    max_width = 0
    for value in values:
        try:
            text = "" if value is None else str(value)
        except Exception:
            text = ""
        max_width = max(max_width, display_width(text))

    return max_width + 2 if max_width > 0 else 0


def _layout_cache_key(
    viewer: Viewer,
    *,
    width: int,
    height: int,
    columns: Sequence[str],
    frozen_columns: Sequence[str],
    hidden_columns: set[str],
    sort_map: dict[str, bool],
    traits: Any,
    theme_epoch: int | None,
) -> tuple[Any, ...]:
    header_widths = tuple(getattr(viewer, "_header_widths", ()))
    autosized = getattr(viewer, "_autosized_widths", None)
    autosized_key = tuple(sorted(autosized.items())) if isinstance(autosized, dict) else None
    sticky = getattr(viewer, "_sticky_column_widths", None)
    sticky_key = tuple(sorted(sticky.items())) if isinstance(sticky, dict) else None
    file_browser_samples = getattr(viewer, "_file_browser_sample_widths", None)
    file_browser_key = (
        tuple(sorted(file_browser_samples.items()))
        if isinstance(file_browser_samples, dict)
        else None
    )
    return (
        width,
        height,
        tuple(columns),
        tuple(frozen_columns),
        tuple(sorted(hidden_columns)),
        header_widths,
        autosized_key,
        sticky_key,
        getattr(viewer, "_width_mode", "default"),
        bool(getattr(viewer, "_compact_width_layout", False)),
        getattr(viewer, "_default_col_width_cap", None),
        getattr(viewer, "_last_col_fits_completely", None),
        getattr(viewer, "_stretch_last_for_slack", False),
        bool(getattr(viewer, "all_columns_maximized", False)),
        getattr(viewer, "maximized_column_index", None),
        bool(getattr(viewer, "is_hist_view", False)),
        getattr(viewer, "freq_source_col", None),
        bool(getattr(traits, "is_file_browser", False)),
        getattr(traits, "preferred_fill_column", None),
        tuple(sorted(sort_map.items())),
        getattr(viewer, "_hscroll_fetch_overscan_cols", None),
        getattr(viewer, "_viewport_cols_override", None),
        file_browser_key,
        theme_epoch,
    )


def _compute_viewport_layout(
    viewer: Viewer,
    *,
    width: int,
    height: int,
    columns: list[str],
    viewer_columns: list[str],
    frozen_cols: list[str],
    hidden_cols: set[str],
    sort_map: dict[str, bool],
    traits: Any,
) -> _ViewportLayout:
    fetch_cols = _compute_fetch_columns(
        viewer,
        visible_column_names=columns,
        viewer_columns=viewer_columns,
        frozen_names=frozen_cols,
        hidden_names=hidden_cols,
    )

    header_labels = [_header_label_for_column(name, sort_map) for name in columns]
    header_label_widths = [display_width(label) for label in header_labels]

    frozen_name_set = set(frozen_cols)
    visible_column_index = {name: idx for idx, name in enumerate(columns)}
    layout_focus_index: int | None = None
    if 0 <= viewer.cur_col < len(viewer_columns):
        current_col_name = viewer_columns[viewer.cur_col]
        layout_focus_index = visible_column_index.get(current_col_name)
        if layout_focus_index is None:
            layout_focus_index = 0 if columns else None
    if layout_focus_index is None and columns:
        layout_focus_index = min(viewer.cur_col, len(columns) - 1)
    frozen_boundary_idx: int | None = None
    if frozen_cols:
        boundary_name = frozen_cols[-1]
        if boundary_name in columns:
            frozen_boundary_idx = columns.index(boundary_name)

    header_widths = getattr(viewer, "_header_widths", [])
    autosized = getattr(viewer, "_autosized_widths", None)
    compact_width_layout = bool(getattr(viewer, "_compact_width_layout", False))
    compact_default_layout = (
        compact_width_layout and getattr(viewer, "_width_mode", "default") == "default"
    )
    if compact_default_layout:
        sticky_widths: dict[str, int] = {}
    else:
        sticky_widths = getattr(viewer, "_sticky_column_widths", {})
        if not isinstance(sticky_widths, dict):
            sticky_widths = {}
    width_cap = viewer._default_col_width_cap if compact_default_layout else None
    col_widths: list[int] = []
    seed_widths: list[int] = []
    original_widths: list[int] = []
    viewer_column_index = {name: idx for idx, name in enumerate(viewer_columns)}
    for idx, col_name in enumerate(columns):
        header_label_width = header_label_widths[idx] if idx < len(header_label_widths) else 0
        col_idx = viewer_column_index.get(col_name)
        if col_idx is None:
            base_width = max(4, header_label_width)
        else:
            base_width = (
                header_widths[col_idx]
                if col_idx < len(header_widths)
                else max(4, header_label_width)
            )
            if autosized:
                base_width = autosized.get(col_idx, base_width)
        base_width = max(base_width, header_label_width)
        if width_cap is not None:
            base_width = min(base_width, width_cap)
        original_widths.append(base_width)
        sticky = sticky_widths.get(col_name)
        seed = base_width
        if isinstance(sticky, int) and sticky > 0:
            if frozen_boundary_idx is not None and idx == frozen_boundary_idx:
                seed = max(1, sticky - 1)
            else:
                seed = sticky
        seed = max(seed, header_label_width)
        col_widths.append(seed)
        seed_widths.append(seed)

    if frozen_boundary_idx is not None and 0 <= frozen_boundary_idx < len(col_widths):
        col_widths[frozen_boundary_idx] += 1
        seed_widths[frozen_boundary_idx] += 1
        original_widths[frozen_boundary_idx] += 1

    is_file_browser = traits.is_file_browser
    fill_column_name = traits.preferred_fill_column
    fill_idx = columns.index(fill_column_name) if fill_column_name else None

    all_maximized = getattr(viewer, "all_columns_maximized", False)
    col_maximized = getattr(viewer, "maximized_column_index", None)
    maximized_column_name: str | None = None
    if col_maximized is not None and 0 <= col_maximized < len(viewer_columns):
        maximized_column_name = viewer_columns[col_maximized]

    if (
        columns
        and fill_idx is None
        and not (col_maximized is not None or all_maximized)
        and hasattr(viewer, "_last_col_fits_completely")
        and not getattr(viewer, "_last_col_fits_completely", True)
        and not compact_default_layout
    ):
        border_overhead = _table_border_overhead(len(columns))
        available_width = max(1, width - border_overhead)
        used_width = sum(col_widths[:-1])
        remaining_width = available_width - used_width
        last_header_width = header_label_widths[-1] if header_label_widths else len(columns[-1]) + 2
        min_last_width = max(4, last_header_width)
        extended_width = max(min_last_width, remaining_width)
        col_widths[-1] = extended_width

    if all_maximized and columns:
        border_overhead = _table_border_overhead(len(columns))
        available_inner = max(1, width - border_overhead)
        current_total = sum(col_widths)
        if current_total < available_inner:
            extra = available_inner - current_total
            share, remainder = divmod(extra, len(col_widths))
            if share:
                for idx in range(len(col_widths)):
                    col_widths[idx] += share
            if remainder:
                for idx in range(remainder):
                    col_widths[-(idx + 1)] += 1

    schema = getattr(viewer, "schema", None)
    if not schema:
        schema = resolve_sheet_schema(getattr(viewer, "sheet", None))

    file_browser_samples = getattr(viewer, "_file_browser_sample_widths", {})
    if not isinstance(file_browser_samples, dict):
        file_browser_samples = {}

    column_meta: list[_ColumnMeta] = []
    for idx, column_name in enumerate(columns):
        is_frozen = column_name in frozen_name_set
        dtype = schema.get(column_name)
        is_numeric = bool(dtype and _is_numeric_dtype(dtype))
        header_display = (
            header_label_widths[idx]
            if idx < len(header_label_widths)
            else display_width(column_name)
        )
        min_width = max(4, min(original_widths[idx], header_display))
        if is_numeric:
            min_width = max(min_width, min(original_widths[idx], 8))
        if is_file_browser and column_name in {"type", "size", "modified"}:
            sample_width = file_browser_samples.get(column_name)
            if sample_width:
                cap = getattr(viewer, "_default_col_width_cap", 20)
                min_width = max(min_width, min(sample_width, cap))
        header_active = idx == layout_focus_index
        column_meta.append(
            _ColumnMeta(
                name=column_name,
                dtype=dtype,
                is_numeric=is_numeric,
                has_nulls=False,
                min_width=min_width,
                original_width=original_widths[idx],
                header_active=header_active,
                is_sorted=column_name in sort_map,
                is_frozen=is_frozen,
            )
        )

    border_overhead = _table_border_overhead(len(columns))
    available_inner = max(1, width - border_overhead) if columns else width

    allow_partial_last = (
        columns
        and fill_idx is None
        and not (col_maximized is not None or all_maximized)
        and hasattr(viewer, "_last_col_fits_completely")
        and not getattr(viewer, "_last_col_fits_completely", True)
    )
    min_widths: list[int] = []
    minimum_targets: list[int] = []
    for idx, meta in enumerate(column_meta):
        seed = seed_widths[idx] if idx < len(seed_widths) else meta.original_width
        if compact_default_layout:
            base_min = max(meta.min_width, seed) if meta.is_frozen else seed
            min_widths.append(base_min)
            minimum_targets.append(base_min)
        else:
            base_min = max(meta.min_width, seed) if meta.is_frozen else meta.min_width
            min_widths.append(base_min)
            minimum_targets.append(base_min if meta.is_frozen else meta.min_width)

    if maximized_column_name:
        for idx, meta in enumerate(column_meta):
            if meta.name != maximized_column_name:
                continue
            max_target = max(seed_widths[idx], meta.original_width, min_widths[idx])
            min_widths[idx] = max_target
            seed_widths[idx] = max_target
            minimum_targets[idx] = max_target
            break

    if (
        allow_partial_last
        and min_widths
        and not column_meta[-1].is_frozen
        and not (maximized_column_name and column_meta[-1].name == maximized_column_name)
        and not compact_default_layout
    ):
        min_widths[-1] = 1
        minimum_targets[-1] = 1

    col_widths = list(min_widths)

    total_min = sum(col_widths)
    remaining = 0
    if compact_default_layout:
        remaining = available_inner - total_min
        if allow_partial_last and col_widths:
            fixed_total = sum(col_widths[:-1])
            remaining_for_last = max(0, available_inner - fixed_total)
            desired_last = max(2, min(col_widths[-1], remaining_for_last))
            col_widths[-1] = desired_last
            total_min = sum(col_widths)
            remaining = available_inner - total_min
        if remaining > 0 and getattr(viewer, "_stretch_last_for_slack", False) and col_widths:
            for idx in range(len(col_widths) - 1, -1, -1):
                if not column_meta[idx].is_frozen:
                    col_widths[idx] += remaining
                    remaining = 0
                    break
    else:
        if total_min > available_inner:
            col_widths = _shrink_widths_to_fit(col_widths, minimum_targets, available_inner)
        else:
            remaining = available_inner - total_min
            weights: list[int] = []
            targets: list[int] = []
            for idx, meta in enumerate(column_meta):
                sticky = sticky_widths.get(meta.name)
                seed = seed_widths[idx] if idx < len(seed_widths) else meta.original_width
                if meta.is_frozen:
                    target = col_widths[idx]
                    weights_val = 0
                else:
                    target = max(meta.min_width, seed)
                    if isinstance(sticky, int) and sticky > 0:
                        target = max(target, sticky)
                    weights_val = 1
                if meta.is_numeric:
                    weights_val += 1
                if meta.header_active:
                    weights_val += 2
                if fill_idx is not None and idx == fill_idx:
                    weights_val += 1
                    target = max(target, available_inner)
                if maximized_column_name and meta.name == maximized_column_name:
                    weights_val += 3
                if getattr(viewer, "is_hist_view", False):
                    weights_val += 1
                    if getattr(viewer, "freq_source_col", None) == meta.name:
                        weights_val += 1
                    if all_maximized:
                        weights_val += 1
                    if width_cap is not None:
                        target = min(target, width_cap)
                weights.append(weights_val)
                targets.append(max(target, meta.min_width))

            remaining = _allocate_widths(col_widths, targets, weights, remaining)

        if remaining > 0:
            if (
                fill_idx is not None
                and 0 <= fill_idx < len(col_widths)
                and not column_meta[fill_idx].is_frozen
            ):
                col_widths[fill_idx] += remaining
                remaining = 0
            else:
                expanded_caps = []
                for idx in range(len(targets)):
                    meta = column_meta[idx]
                    if meta.is_frozen:
                        expanded_caps.append(col_widths[idx])
                    else:
                        if maximized_column_name and meta.name == maximized_column_name:
                            expanded_caps.append(targets[idx])
                        else:
                            expanded_caps.append(targets[idx] + remaining)
                remaining = _allocate_widths(col_widths, expanded_caps, weights, remaining)

    has_left_overflow, has_right_overflow = _compute_horizontal_overflow(
        viewer,
        visible_column_names=columns,
        frozen_names=frozen_name_set,
    )

    return _ViewportLayout(
        columns=columns,
        column_meta=column_meta,
        column_widths=col_widths,
        header_labels=header_labels,
        header_label_widths=header_label_widths,
        frozen_boundary_idx=frozen_boundary_idx,
        fetch_columns=fetch_cols,
        has_left_overflow=has_left_overflow,
        has_right_overflow=has_right_overflow,
        is_file_browser=is_file_browser,
    )


def compute_viewport_plan(
    viewer: Viewer, width: int, height: int, *, skip_formatting: bool = False
) -> ViewportPlan:
    """Compute a viewport plan for ``viewer`` constrained to ``width``×``height``."""

    should_record = getattr(viewer, "_perf_callback", None) is not None
    layout_start_ns = perf_counter_ns() if should_record else None

    sheet = getattr(viewer, "sheet", None)
    if sheet is not None and hasattr(sheet, "update_layout_for_view"):
        try:
            sheet.update_layout_for_view(
                view_width=width,
                view_height=height,
                viewer=viewer,
            )
        except TypeError:
            sheet.update_layout_for_view(width)

    viewer_columns = list(getattr(viewer, "columns", ()))
    if hasattr(viewer, "visible_cols") and viewer.visible_cols:
        cols = list(viewer.visible_cols)
    else:
        cols = list(viewer_columns)

    frozen_cols = getattr(viewer, "frozen_columns", []) if hasattr(viewer, "frozen_columns") else []
    hidden = set(getattr(viewer, "_hidden_cols", set()) or ())
    sort_map = _sort_directions(viewer)
    traits = resolve_sheet_traits(getattr(viewer, "sheet", None), columns=cols)
    theme_epoch = getattr(viewer, "_theme_epoch", None)

    layout_key = _layout_cache_key(
        viewer,
        width=width,
        height=height,
        columns=cols,
        frozen_columns=frozen_cols,
        hidden_columns=hidden,
        sort_map=sort_map,
        traits=traits,
        theme_epoch=theme_epoch,
    )

    layout_cache = getattr(viewer, "_viewport_layout_cache", None)
    if isinstance(layout_cache, _LayoutCache) and layout_cache.key == layout_key:
        layout = layout_cache.layout
    else:
        layout = _compute_viewport_layout(
            viewer,
            width=width,
            height=height,
            columns=cols,
            viewer_columns=viewer_columns,
            frozen_cols=frozen_cols,
            hidden_cols=hidden,
            sort_map=sort_map,
            traits=traits,
        )
        viewer._viewport_layout_cache = _LayoutCache(key=layout_key, layout=layout)

    layout_duration_ms = None
    if layout_start_ns is not None:
        layout_duration_ms = (perf_counter_ns() - layout_start_ns) / 1_000_000

    table_slice = viewer.get_visible_table_slice(layout.fetch_columns)
    perf_payload = {
        "width": width,
        "height": height,
        "rows": table_slice.height,
        "cols": len(layout.columns),
    }

    selection_start_ns: int | None
    if should_record and layout_duration_ms is not None:
        viewer._record_perf_event("render.viewport_plan.layout", layout_duration_ms, perf_payload)
        selection_start_ns = perf_counter_ns()
    else:
        selection_start_ns = None

    columns_data = [table_slice.column(name) for name in layout.columns]

    if layout.is_file_browser:
        samples = getattr(viewer, "_file_browser_sample_widths", None)
        if not isinstance(samples, dict):
            samples = {}
        updated = False
        for idx, column_name in enumerate(layout.columns):
            if column_name not in {"type", "size", "modified"}:
                continue
            sample_width = _sampled_column_width(columns_data[idx])
            if not sample_width:
                continue
            cap = getattr(viewer, "_default_col_width_cap", 20)
            sample_width = min(sample_width, cap)
            if sample_width > samples.get(column_name, 0):
                samples[column_name] = sample_width
                updated = True
        viewer._file_browser_sample_widths = samples
        if updated:
            layout_key = _layout_cache_key(
                viewer,
                width=width,
                height=height,
                columns=cols,
                frozen_columns=frozen_cols,
                hidden_columns=hidden,
                sort_map=sort_map,
                traits=traits,
                theme_epoch=theme_epoch,
            )
            layout = _compute_viewport_layout(
                viewer,
                width=width,
                height=height,
                columns=cols,
                viewer_columns=viewer_columns,
                frozen_cols=frozen_cols,
                hidden_cols=hidden,
                sort_map=sort_map,
                traits=traits,
            )
            viewer._viewport_layout_cache = _LayoutCache(key=layout_key, layout=layout)

    frozen_boundary_idx = layout.frozen_boundary_idx

    visible_column_index = {name: idx for idx, name in enumerate(layout.columns)}

    current_visible_col_index: int | None = None
    if 0 <= viewer.cur_col < len(viewer_columns):
        current_col_name = viewer_columns[viewer.cur_col]
        current_visible_col_index = visible_column_index.get(current_col_name)
        if current_visible_col_index is None:
            current_visible_col_index = 0 if layout.columns else None

    if current_visible_col_index is None and layout.columns:
        current_visible_col_index = min(viewer.cur_col, len(layout.columns) - 1)

    for idx, meta in enumerate(layout.column_meta):
        meta.has_nulls = table_slice.height > 0 and columns_data[idx].null_count > 0
        meta.header_active = idx == current_visible_col_index

    column_plans: list[ColumnPlan] = []
    for idx, meta in enumerate(layout.column_meta):
        header_label = (
            layout.header_labels[idx]
            if idx < len(layout.header_labels)
            else _header_label_for_column(meta.name, sort_map)
        )
        column_plans.append(
            ColumnPlan(
                name=meta.name,
                header_label=header_label,
                width=layout.column_widths[idx],
                min_width=meta.min_width,
                original_width=meta.original_width,
                is_numeric=meta.is_numeric,
                has_nulls=meta.has_nulls,
                header_active=meta.header_active,
                is_sorted=meta.is_sorted,
            )
        )

    viewer._sticky_column_widths = {plan.name: plan.width for plan in column_plans}

    header_row: list[Cell] = []
    for column in column_plans:
        cell = Cell(
            text=column.header_label,
            truncated=False,
            role="header",
            active_row=False,
            active_col=column.header_active,
            active_cell=column.header_active,
            selected_row=False,
            numeric=False,
            is_null=False,
        )
        header_row.append(cell)

    row_positions = getattr(viewer, "visible_row_positions", [])
    selection_lookup_obj = getattr(viewer, "_selected_row_ids", None)
    selection_lookup = selection_lookup_obj if isinstance(selection_lookup_obj, set) else set()
    selection_filter_matches: set[Hashable] | None = None
    selection_filter_expr = getattr(viewer, "_selection_filter_expr", None)
    value_filter = getattr(viewer, "_value_selection_filter", None)
    active_row_selected: bool | None = None
    defer_selection_fetch = False
    if not selection_filter_expr:
        value_filter_expr_fn = getattr(viewer, "_value_selection_filter_expr", None)
        if callable(value_filter_expr_fn):
            try:
                selection_filter_expr = value_filter_expr_fn()
            except Exception:
                selection_filter_expr = None
    if selection_filter_expr and not selection_lookup:
        filter_column = value_filter[0] if value_filter else None
        if filter_column and filter_column not in table_slice.column_names:
            defer_selection_fetch = False
        else:
            defer_selection_fetch = _should_defer_selection_fetch(viewer, monotonic_ns())
        resolver = getattr(viewer, "_selection_matches_for_slice", None)
        if callable(resolver):
            original_expr = getattr(viewer, "_selection_filter_expr", None)
            try:
                if original_expr != selection_filter_expr:
                    viewer._selection_filter_expr = selection_filter_expr
                selection_filter_matches = resolver(table_slice, row_positions)
            except Exception:
                selection_filter_matches = None
            finally:
                if original_expr != selection_filter_expr:
                    viewer._selection_filter_expr = original_expr
        if selection_filter_matches is None and not defer_selection_fetch:
            # Attempt to fetch required columns even when they are scrolled out of view.
            fetch_columns = list(table_slice.column_names)
            if selection_filter_expr:
                for name in getattr(viewer, "columns", ()):
                    if name not in fetch_columns:
                        fetch_columns.append(name)
            filter_column = value_filter[0] if value_filter else None
            if filter_column and filter_column not in fetch_columns:
                fetch_columns.append(filter_column)
            row_id_column = getattr(getattr(viewer, "row_provider", None), "_row_id_column", None)
            if row_id_column and row_id_column not in fetch_columns:
                fetch_columns.append(row_id_column)

            start = table_slice.start_offset
            if start is None and row_positions:
                start = min(row_positions)
            if start is None:
                start = getattr(viewer, "row0", None)
            count = max(0, table_slice.height or len(row_positions))
            if fetch_columns and count > 0 and start is not None:
                plan = getattr(viewer, "_current_plan", None)
                row_provider = getattr(viewer, "row_provider", None)
                if callable(plan) and row_provider is not None:
                    try:
                        supplemental_slice, _status = row_provider.get_slice(
                            plan(),
                            fetch_columns,
                            int(start),
                            int(count),
                        )
                    except Exception:
                        supplemental_slice = None
                    if supplemental_slice is not None:
                        resolver = getattr(viewer, "_selection_matches_for_slice", None)
                        if callable(resolver):
                            try:
                                original_expr = getattr(viewer, "_selection_filter_expr", None)
                                if original_expr != selection_filter_expr:
                                    viewer._selection_filter_expr = selection_filter_expr
                                selection_filter_matches = resolver(
                                    supplemental_slice, row_positions
                                )
                            except Exception:
                                selection_filter_matches = None
                            finally:
                                if original_expr != selection_filter_expr:
                                    viewer._selection_filter_expr = original_expr
        if selection_filter_matches is None:
            active_row = getattr(viewer, "cur_row", None)
            if isinstance(active_row, int):
                fetch_columns = list(table_slice.column_names)
                if selection_filter_expr:
                    for name in getattr(viewer, "columns", ()):
                        if name not in fetch_columns:
                            fetch_columns.append(name)
                filter_column = value_filter[0] if value_filter else None
                if filter_column and filter_column not in fetch_columns:
                    fetch_columns.append(filter_column)
                row_id_column = getattr(
                    getattr(viewer, "row_provider", None), "_row_id_column", None
                )
                if row_id_column and row_id_column not in fetch_columns:
                    fetch_columns.append(row_id_column)
                plan = getattr(viewer, "_current_plan", None)
                row_provider = getattr(viewer, "row_provider", None)
                if callable(plan) and row_provider is not None and fetch_columns:
                    try:
                        active_slice, _status = row_provider.get_slice(
                            plan(),
                            fetch_columns,
                            int(active_row),
                            1,
                        )
                    except Exception:
                        active_slice = None
                    if active_slice is not None and callable(resolver):
                        original_expr = getattr(viewer, "_selection_filter_expr", None)
                        try:
                            if original_expr != selection_filter_expr:
                                viewer._selection_filter_expr = selection_filter_expr
                            active_matches = resolver(active_slice, [active_row])
                        except Exception:
                            active_matches = None
                        finally:
                            if original_expr != selection_filter_expr:
                                viewer._selection_filter_expr = original_expr
                        if active_matches is not None:
                            active_row_selected = active_row in active_matches
    resolve_row_id = getattr(viewer, "_row_identifier_for_slice", None)
    visible_frozen_rows = min(getattr(viewer, "visible_frozen_row_count", 0), table_slice.height)
    value_selection_filter = getattr(viewer, "_value_selection_filter", None)
    filter_column_index: int | None = None
    filter_value = None
    filter_is_nan = False
    if value_selection_filter is not None:
        filter_column, filter_value, filter_is_nan = value_selection_filter
        for idx, column in enumerate(column_plans):
            if column.name == filter_column:
                filter_column_index = idx
                break

    plan_hash = None
    plan_hash_fn = getattr(viewer, "plan_hash", None)
    if callable(plan_hash_fn):
        with contextlib.suppress(Exception):
            plan_hash = plan_hash_fn()
    sheet_version = getattr(getattr(viewer, "sheet", None), "cache_version", None)
    selection_epoch = getattr(viewer, "selection_epoch", None)
    cache_key = (
        plan_hash,
        sheet_version,
        tuple(column.name for column in column_plans),
        tuple(column.width for column in column_plans),
        frozen_boundary_idx,
        current_visible_col_index,
        selection_epoch,
        skip_formatting,
    )
    formatted_cell_cache: _FormattedCellCache | None = None
    formatted_cell_cache_key = (
        plan_hash,
        sheet_version,
        tuple(column.name for column in column_plans),
        tuple(column.width for column in column_plans),
        frozen_boundary_idx,
        skip_formatting,
    )
    cache = getattr(viewer, "_viewport_body_cache", None)
    cached_rows: dict[int, list[Cell]] = {}
    cached_active_row: int | None = None
    positions_valid = len(row_positions) == table_slice.height
    if (
        not skip_formatting
        and isinstance(cache, _BodyRowCache)
        and cache.key == cache_key
        and positions_valid
        and cache.positions
    ):
        cached_rows = dict(zip(cache.positions, cache.rows, strict=False))
        cached_active_row = cache.active_row
    row_positions_key = tuple(row_positions) if positions_valid and row_positions else None
    formatted_cache: _FormattedColumnCache | None = None
    if positions_valid and row_positions_key is not None:
        formatted_cache_key = (plan_hash, sheet_version, row_positions_key)
        last_positions_key = getattr(viewer, "_formatted_column_positions_key", None)
        cached = getattr(viewer, "_formatted_column_cache", None)
        if isinstance(cached, _FormattedColumnCache) and cached.key == formatted_cache_key:
            formatted_cache = cached
        elif last_positions_key == row_positions_key:
            formatted_cache = _FormattedColumnCache(key=formatted_cache_key, columns={})
            viewer._formatted_column_cache = formatted_cache
        else:
            viewer._formatted_column_cache = None
        viewer._formatted_column_positions_key = row_positions_key
    else:
        viewer._formatted_column_cache = None
        viewer._formatted_column_positions_key = None

    if positions_valid and row_positions_key is not None and not skip_formatting:
        cell_cache = getattr(viewer, "_formatted_cell_cache", None)
        if (
            isinstance(cell_cache, _FormattedCellCache)
            and cell_cache.key == formatted_cell_cache_key
        ):
            formatted_cell_cache = cell_cache
        else:
            max_rows = max(10, height * 3)
            formatted_cell_cache = _FormattedCellCache(
                key=formatted_cell_cache_key,
                max_rows=max_rows,
                rows={},
                order=deque(),
            )
            viewer._formatted_cell_cache = formatted_cell_cache
    else:
        viewer._formatted_cell_cache = None

    if should_record and selection_start_ns is not None:
        duration_ms = (perf_counter_ns() - selection_start_ns) / 1_000_000
        viewer._record_perf_event("render.viewport_plan.selection", duration_ms, perf_payload)
        cells_start_ns = perf_counter_ns()
    else:
        cells_start_ns = None

    pad = 1
    body_rows: list[list[Cell]] = []
    rows_to_build: list[tuple[int, int]] = []
    for r in range(table_slice.height):
        row_index = row_positions[r] if r < len(row_positions) else viewer.row0 + r
        cached_row = cached_rows.get(row_index) if cached_rows else None
        if cached_row is not None:
            if row_index == viewer.cur_row:
                body_rows.append(_retag_cached_row(cached_row, active=True))
            elif row_index == cached_active_row:
                body_rows.append(_retag_cached_row(cached_row, active=False))
            else:
                body_rows.append(cached_row)
            continue
        body_rows.append([])
        rows_to_build.append((r, row_index))

    if rows_to_build:
        formatted_columns: list[Sequence[str]] = []
        decimal_alignments: list[tuple[int, int] | None] = []
        column_inner_widths: list[int] = []
        column_safe_max_chars: list[int] = []
        formatted_cache_columns = formatted_cache.columns if formatted_cache is not None else None
        if not skip_formatting:
            for idx, column in enumerate(column_plans):
                column_width = max(1, column.width)
                border_offset = (
                    1 if frozen_boundary_idx is not None and idx == frozen_boundary_idx else 0
                )
                content_width = max(0, column_width - border_offset)
                padding = pad if content_width >= (pad * 2 + 1) else 0
                inner_width = max(0, content_width - (padding * 2))
                if column.is_numeric:
                    # Keep full precision for numeric columns; downstream truncation handles width.
                    safe_max_chars = 0
                elif column.name == "hist":
                    safe_max_chars = max(inner_width, 0)
                elif layout.is_file_browser and column.name == "name":
                    safe_max_chars = 0
                else:
                    safe_max_chars = max(inner_width, 1, 20)
                column_safe_max_chars.append(safe_max_chars)
                column_cache_key = (column.name, safe_max_chars)
                if (
                    formatted_cache_columns is not None
                    and column_cache_key in formatted_cache_columns
                ):
                    formatted_columns.append(formatted_cache_columns[column_cache_key])
                else:
                    formatted = columns_data[idx].formatted(safe_max_chars)
                    formatted_columns.append(formatted)
                    if formatted_cache_columns is not None:
                        formatted_cache_columns[column_cache_key] = formatted
                column_inner_widths.append(inner_width)

            decimal_cache = getattr(viewer, "_decimal_alignment_cache", None)
            if decimal_cache is None:
                decimal_cache = {}
                viewer._decimal_alignment_cache = decimal_cache

            for idx, column in enumerate(column_plans):
                if not column.is_numeric:
                    decimal_alignments.append(None)
                    continue
                inner_width = column_inner_widths[idx]
                viewport_alignment = compute_decimal_alignment(formatted_columns[idx], inner_width)
                cached_alignment = decimal_cache.get(column.name)

                merged_alignment: tuple[int, int] | None = None
                if cached_alignment and viewport_alignment:
                    merged_alignment = (
                        max(cached_alignment[0], viewport_alignment[0]),
                        cached_alignment[1],
                    )
                elif cached_alignment:
                    merged_alignment = cached_alignment
                else:
                    merged_alignment = viewport_alignment

                if merged_alignment is not None:
                    required_width = merged_alignment[0] + 1 + merged_alignment[1]
                    if inner_width >= required_width:
                        decimal_cache[column.name] = merged_alignment
                        decimal_alignments.append(merged_alignment)
                        continue

                decimal_alignments.append(None)
        else:
            decimal_cache = getattr(viewer, "_decimal_alignment_cache", None)
            for idx, column in enumerate(column_plans):
                column_width = max(1, column.width)
                border_offset = (
                    1 if frozen_boundary_idx is not None and idx == frozen_boundary_idx else 0
                )
                content_width = max(0, column_width - border_offset)
                padding = pad if content_width >= (pad * 2 + 1) else 0
                inner_width = max(0, content_width - (padding * 2))
                column_inner_widths.append(inner_width)
                alignment = None
                if column.is_numeric and decimal_cache:
                    cached_alignment = decimal_cache.get(column.name)
                    if cached_alignment is not None:
                        required_width = cached_alignment[0] + 1 + cached_alignment[1]
                        if inner_width >= required_width:
                            alignment = cached_alignment
                decimal_alignments.append(alignment)
                if column.is_numeric:
                    safe_max_chars = 0
                elif column.name == "hist":
                    safe_max_chars = max(inner_width, 0)
                elif layout.is_file_browser and column.name == "name":
                    safe_max_chars = 0
                else:
                    safe_max_chars = max(inner_width, 1)
                column_safe_max_chars.append(safe_max_chars)
                column_cache_key = (column.name, safe_max_chars)
                if (
                    formatted_cache_columns is not None
                    and column_cache_key in formatted_cache_columns
                ):
                    formatted_columns.append(formatted_cache_columns[column_cache_key])
                else:
                    formatted = columns_data[idx].formatted(safe_max_chars)
                    formatted_columns.append(formatted)
                    if formatted_cache_columns is not None:
                        formatted_cache_columns[column_cache_key] = formatted

        for r, row_index in rows_to_build:
            row_cells: list[Cell] = []
            row_active = row_index == viewer.cur_row
            need_row_id = bool(selection_lookup or selection_filter_matches)
            row_identifier = None
            if need_row_id and callable(resolve_row_id):
                try:
                    row_identifier = resolve_row_id(
                        table_slice,
                        r,
                        row_positions=row_positions,
                        absolute_row=row_index,
                    )
                except Exception:
                    row_identifier = None
            if need_row_id and row_identifier is None:
                if r < len(row_positions):
                    row_identifier = row_positions[r]
                elif table_slice.start_offset is not None:
                    row_identifier = table_slice.start_offset + r
            row_selected = bool(selection_lookup and row_identifier in selection_lookup)
            if not row_selected and selection_filter_matches:
                row_selected = row_identifier in selection_filter_matches
            if not row_selected and row_active and active_row_selected:
                row_selected = True
            if not row_selected and filter_column_index is not None:
                try:
                    value = columns_data[filter_column_index].values[r]
                except Exception:
                    value = None
                if filter_is_nan:
                    row_selected = isinstance(value, float) and math.isnan(value)
                else:
                    row_selected = value == filter_value
            for ci, column in enumerate(column_plans):
                is_numeric = column.is_numeric
                width_hint = max(1, column.width)
                border_offset = (
                    1 if frozen_boundary_idx is not None and ci == frozen_boundary_idx else 0
                )
                content_width = max(0, width_hint - border_offset)
                padding = pad if content_width >= (pad * 2 + 1) else 0
                inner_width = max(0, content_width - padding * 2)
                raw_value = columns_data[ci].values[r]
                precomputed_txt: str | None = None
                cell_cache_key = None
                row_cache = None
                if formatted_cell_cache is not None:
                    row_cache = formatted_cell_cache.rows.get(row_index)
                    safe_max_chars = (
                        column_safe_max_chars[ci] if ci < len(column_safe_max_chars) else 0
                    )
                    cell_cache_key = (column.name, safe_max_chars)
                    if row_cache is not None:
                        cached_txt = row_cache.get(cell_cache_key)
                        if cached_txt is not None:
                            precomputed_txt = cached_txt
                if precomputed_txt is None:
                    precomputed_txt = formatted_columns[ci][r] if formatted_columns else ""
                    if formatted_cell_cache is not None and cell_cache_key is not None:
                        if row_cache is None:
                            formatted_cell_cache.rows[row_index] = {cell_cache_key: precomputed_txt}
                            formatted_cell_cache.order.append(row_index)
                        else:
                            row_cache[cell_cache_key] = precomputed_txt
                is_null = raw_value is None or precomputed_txt == ""
                if is_null:
                    base_txt = "null"
                elif isinstance(raw_value, float):
                    if math.isnan(raw_value):
                        base_txt = "NaN"
                    elif math.isinf(raw_value):
                        base_txt = "inf" if raw_value > 0 else "-inf"
                    else:
                        base_txt = precomputed_txt
                else:
                    base_txt = precomputed_txt

                cell_truncated = False
                if inner_width > 0:
                    if is_numeric:
                        base_display_width = display_width(base_txt)
                        truncated = base_display_width > inner_width
                        if truncated:
                            # Preserve the fractional part by clipping from the left when tight on
                            # space.
                            suffix = base_txt[-inner_width:]
                            visible_txt = truncate_grapheme_safe(suffix, inner_width)
                        else:
                            visible_txt = base_txt
                        cell_truncated = truncated
                    else:
                        if layout.is_file_browser and column.name == "name":
                            suffix_hint = None
                            if base_txt.endswith("/"):
                                suffix_hint = "/"
                            else:
                                dot_idx = base_txt.rfind(".")
                                if 0 < dot_idx < len(base_txt) - 1:
                                    suffix_hint = base_txt[dot_idx:]
                            visible_txt = truncate_middle_grapheme_safe(
                                base_txt,
                                inner_width,
                                back_preference=suffix_hint,
                            )
                            truncated = visible_txt != base_txt
                            cell_truncated = False
                        else:
                            visible_txt = truncate_grapheme_safe(base_txt, inner_width)
                            truncated = visible_txt != base_txt
                            cell_truncated = truncated
                else:
                    visible_txt = ""
                    truncated = bool(base_txt)
                    if is_numeric:
                        cell_truncated = truncated
                aligned_txt = visible_txt
                if inner_width > 0:
                    alignment = decimal_alignments[ci] if ci < len(decimal_alignments) else None
                    if alignment is not None and not is_null:
                        aligned_candidate = apply_decimal_alignment(
                            base_txt,
                            alignment,
                            inner_width,
                        )
                    else:
                        aligned_candidate = None
                    if aligned_candidate is not None:
                        aligned_txt = aligned_candidate
                    elif is_numeric:
                        aligned_txt = pad_left_display(visible_txt, inner_width)
                    else:
                        aligned_txt = pad_right_display(visible_txt, inner_width)

                cell_text = (
                    "" if content_width == 0 else (" " * padding) + aligned_txt + (" " * padding)
                )

                col_active = ci == current_visible_col_index
                cell = Cell(
                    text=cell_text,
                    truncated=cell_truncated,
                    role="body",
                    active_row=row_active,
                    active_col=col_active,
                    active_cell=row_active and col_active,
                    selected_row=row_selected,
                    numeric=is_numeric,
                    is_null=is_null,
                )
                row_cells.append(cell)
            body_rows[r] = row_cells

        if formatted_cell_cache is not None:
            while len(formatted_cell_cache.rows) > formatted_cell_cache.max_rows:
                stale_row = formatted_cell_cache.order.popleft()
                formatted_cell_cache.rows.pop(stale_row, None)

    if should_record and cells_start_ns is not None:
        duration_ms = (perf_counter_ns() - cells_start_ns) / 1_000_000
        viewer._record_perf_event("render.viewport_plan.cells", duration_ms, perf_payload)

    if positions_valid and not skip_formatting:
        viewer._viewport_body_cache = _BodyRowCache(
            key=cache_key,
            positions=tuple(row_positions),
            rows=body_rows,
            active_row=getattr(viewer, "cur_row", None),
        )
    else:
        viewer._viewport_body_cache = None

    cells: list[list[Cell]] = []
    if header_row:
        cells.append(header_row)
    cells.extend(body_rows)

    row_offset = max(0, viewer.row0)
    if visible_frozen_rows:
        row_offset = max(row_offset, visible_frozen_rows)

    col_offset = max(0, viewer.col0)

    has_left_overflow = layout.has_left_overflow
    has_right_overflow = layout.has_right_overflow
    row_positions_tuple = tuple(row_positions) if positions_valid else None

    return ViewportPlan(
        columns=column_plans,
        frozen_boundary_idx=frozen_boundary_idx,
        rows=table_slice.height,
        row_offset=row_offset,
        col_offset=col_offset,
        has_left_overflow=has_left_overflow,
        has_right_overflow=has_right_overflow,
        cells=cells,
        active_row_index=getattr(viewer, "cur_row", 0),
        row_positions=row_positions_tuple,
        formatting_skipped=skip_formatting,
    )
