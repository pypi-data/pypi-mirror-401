"""prompt_toolkit-native table control that renders from a viewport plan."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Sequence
from contextlib import nullcontext, suppress
from dataclasses import dataclass, replace
from time import perf_counter, perf_counter_ns
from types import MethodType
from typing import TYPE_CHECKING, Any
from weakref import ReferenceType, ref

from prompt_toolkit.data_structures import Point
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.layout.controls import UIContent, UIControl
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType, MouseModifier

from ...logging import Recorder, frame_hash, viewer_state_snapshot
from ...render.status_bar import render_status_line
from ...render.style_resolver import get_active_style_resolver
from ...render.table import (
    RenderedLine,
    apply_overflow_indicators,
    build_blank_line,
    build_row_line,
    build_separator_line,
    compute_column_overflows,
    determine_blank_line_highlights,
)
from ...render.viewport_plan import Cell, ViewportPlan, compute_viewport_plan
from ...theme import theme_epoch

PlanCacheKey = tuple[Any, int, int, int, int, Any, Any, int]
LineCacheKey = tuple[Any, ...]

if TYPE_CHECKING:  # pragma: no cover - import cycles in typing context only
    from prompt_toolkit.key_binding.key_bindings import NotImplementedOrNone

    from ...core.viewer import Viewer
else:  # pragma: no cover - fallback for runtime typing introspection
    Viewer = Any


@dataclass(slots=True)
class _LineRender:
    """Container for rendered line fragments and plain text."""

    fragments: StyleAndTextTuples
    plain_text: str
    cursor_x: int | None = None
    source: RenderedLine | None = None


@dataclass(slots=True)
class _RowLineCache:
    key: tuple[Any, ...]
    positions: tuple[int, ...]
    lines: deque[_LineRender]
    active_row: int | None


@dataclass(slots=True)
class _RegionCell:
    base: Cell
    region_selected: bool

    def __getattr__(self, name: str) -> Any:  # pragma: no cover - simple proxy
        return getattr(self.base, name)


@dataclass(slots=True)
class _StatusWidthProxy:
    base: Any
    status_width_chars: int

    def __getattr__(self, name: str) -> Any:  # pragma: no cover - simple proxy
        return getattr(self.base, name)


@dataclass(frozen=True, slots=True)
class _BudgetPlan:
    """Per-frame rendering adjustments when the budget guard triggers."""

    overscan_hint: int | None = None
    minimal_styles: bool = False
    drop_borders: bool = False
    coalesce_multiplier: float = 1.0

    def is_default(self) -> bool:
        return (
            self.overscan_hint is None
            and not self.minimal_styles
            and not self.drop_borders
            and self.coalesce_multiplier == 1.0
        )


class RenderBudgetGuard:
    """Track frame timings and request temporary render degradations."""

    def __init__(self, *, budget_ms: float = 18.0, alpha: float = 0.25) -> None:
        self._budget_ms = budget_ms
        self._alpha = alpha
        self._avg_ms: float | None = None
        self._degrade_next = False
        self._sample_count = 0

    def plan_frame(self, viewer: Viewer) -> _BudgetPlan:
        if not self._degrade_next:
            return _BudgetPlan()

        self._degrade_next = False
        overscan = max(1, int(getattr(viewer, "view_height", 1) or 1))
        return _BudgetPlan(
            overscan_hint=overscan,
            minimal_styles=True,
            drop_borders=True,
            coalesce_multiplier=2.0,
        )

    def record_frame(self, render_ms: float, paint_ms: float) -> None:
        total = render_ms + paint_ms
        self._sample_count += 1
        if self._avg_ms is None:
            self._avg_ms = total
        else:
            self._avg_ms = (1 - self._alpha) * self._avg_ms + self._alpha * total

        if self._sample_count >= 2 and (
            total > self._budget_ms or (self._avg_ms or 0.0) > self._budget_ms
        ):
            self._degrade_next = True

    @property
    def average_ms(self) -> float | None:
        return self._avg_ms


class TableControl(UIControl):
    """A prompt_toolkit ``UIControl`` that draws table cells from a viewport plan."""

    def __init__(
        self,
        viewer: Viewer,
        *,
        apply_pending_moves: Callable[[], None],
        poll_background_jobs: Callable[[], None],
        set_status: Callable[[StyleAndTextTuples], None],
        apply_budget_plan: Callable[[_BudgetPlan], None] | None = None,
        on_cell_click: Callable[[int, str], None] | None = None,
        recorder: Recorder | None = None,
    ) -> None:
        self._viewer = viewer
        self._apply_pending_moves = apply_pending_moves
        self._poll_background_jobs = poll_background_jobs
        self._set_status = set_status
        self._apply_budget_plan = apply_budget_plan
        self._on_cell_click = on_cell_click
        self._recorder = recorder
        self._cached_plan: ViewportPlan | None = None
        self._plan_cache_key: PlanCacheKey | None = None
        self._line_cache: dict[LineCacheKey, _LineRender] = {}
        self._row_line_cache: _RowLineCache | None = None
        self._wrapped_ui_hooks: set[Any] = set()
        self._wrapped_ui_hook_refs: list[ReferenceType[Any]] = []
        self._wrapped_ui_hook_ids: set[int] = set()
        self._budget_guard = RenderBudgetGuard()
        self._current_budget_plan = _BudgetPlan()
        self._current_theme_epoch = theme_epoch()
        self._style_cache: dict[tuple[str, ...], str] = {}
        self._recorded_style_epoch: int | None = None
        self._style_resolve_ns = 0
        self._style_resolve_calls = 0
        self._style_resolve_enabled = False
        self._last_plan_cache_hit = False
        self._last_frame_finished_at: float | None = None
        self._last_move_direction: int = 0
        self._last_move_time: float | None = None
        self._last_coalesced_steps: int = 0
        self._last_overscan_rows: int = 0
        self._last_content_line_count: int | None = None
        self._last_content_height: int | None = None
        self._last_render_width: int | None = None
        self._last_render_height: int | None = None
        self._fast_scroll_active = False
        self._status_initialized = False
        self._coalesce_hot_window = 0.25
        self._overscan_ratio = 0.25

    def update_viewer(self, viewer: Viewer) -> None:
        """Point the control at the active viewer."""

        self._viewer = viewer
        self._invalidate_cache()

    def attach_ui_hooks(self, ui_hooks: Any) -> Any:
        """Wrap ``ui_hooks.invalidate`` to clear cached render state."""

        invalidate = getattr(ui_hooks, "invalidate", None)
        if invalidate is None:
            return ui_hooks

        hook_id = id(ui_hooks)

        try:
            if ui_hooks in self._wrapped_ui_hooks:
                return ui_hooks
        except TypeError:
            pass

        for hook_ref in list(self._wrapped_ui_hook_refs):
            hook = hook_ref()
            if hook is None:
                self._wrapped_ui_hook_refs.remove(hook_ref)
                continue
            if hook is ui_hooks:
                return ui_hooks

        if hook_id in self._wrapped_ui_hook_ids:
            return ui_hooks

        bound_self = getattr(invalidate, "__self__", None)
        bound_func = getattr(invalidate, "__func__", None)

        def _wrapped_invalidate(*args: Any, **kwargs: Any) -> Any:
            self._invalidate_cache()
            if bound_self is not None and bound_func is not None:
                return bound_func(bound_self, *args[1:], **kwargs)
            return invalidate(*args[1:], **kwargs) if args else invalidate(**kwargs)

        ui_hooks.invalidate = MethodType(_wrapped_invalidate, ui_hooks)
        try:
            self._wrapped_ui_hooks.add(ui_hooks)
        except TypeError:
            try:
                self._wrapped_ui_hook_refs.append(ref(ui_hooks))
            except TypeError:
                self._wrapped_ui_hook_ids.add(hook_id)
        return ui_hooks

    def preferred_width(self, max_available_width: int) -> int | None:  # noqa: D401
        _ = max_available_width
        return None

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix: Callable[[int], str] | None,
    ) -> int | None:  # noqa: D401
        _ = (width, max_available_height, wrap_lines, get_line_prefix)
        return None

    def is_focusable(self) -> bool:  # noqa: D401
        return True

    def create_content(self, width: int, height: int) -> UIContent:  # noqa: D401
        viewer = self._viewer
        recorder = self._recorder if self._recorder and self._recorder.enabled else None
        self._last_render_width = width
        self._last_render_height = height

        move_controller = getattr(self._apply_pending_moves, "__self__", None)
        base_steps = (
            max(1, int(getattr(move_controller, "_max_steps_per_frame", 1)))
            if move_controller is not None
            else 1
        )
        pending_before = (
            abs(int(getattr(move_controller, "_pending_row_delta", 0)))
            if move_controller is not None
            else 0
        )
        previous_direction = self._last_move_direction
        burst_multiplier = self._compute_burst_multiplier(
            pending_before, base_steps, previous_direction
        )

        budget_plan = self._budget_guard.plan_frame(viewer)
        if burst_multiplier > getattr(budget_plan, "coalesce_multiplier", 1.0):
            budget_plan = replace(budget_plan, coalesce_multiplier=burst_multiplier)
        fast_scroll = self._should_skip_formatting(
            viewer,
            pending_before=pending_before,
            base_steps=base_steps,
            budget_plan=budget_plan,
            previous_direction=previous_direction,
        )
        if fast_scroll and not budget_plan.minimal_styles:
            budget_plan = replace(budget_plan, minimal_styles=True, drop_borders=True)
        self._current_budget_plan = budget_plan
        previous_theme_epoch = self._current_theme_epoch
        self._current_theme_epoch = theme_epoch()
        if previous_theme_epoch != self._current_theme_epoch:
            self._recorded_style_epoch = None
            self._style_cache = {}
        if self._apply_budget_plan is not None:
            self._apply_budget_plan(budget_plan)
        if budget_plan.overscan_hint is not None:
            with suppress(Exception):
                viewer.request_frame_budget_overscan(budget_plan.overscan_hint)

        direction, _total_steps, coalesced_steps = self._apply_pending_moves_with_coalesce(
            budget_plan,
            previous_direction,
            base_steps,
            move_controller,
        )
        self._poll_background_jobs()
        overscan_rows = self._maybe_prime_overscan(
            viewer,
            height,
            budget_plan,
            direction,
            previous_direction,
            move_controller,
        )

        perf_ctx = (
            recorder.perf_timer(
                "render.table",
                payload={"context": "tui", "trigger": "refresh"},
            )
            if recorder
            else nullcontext()
        )

        render_start = perf_counter()
        with perf_ctx:
            plan_start = perf_counter()
            if fast_scroll:
                plan = compute_viewport_plan(viewer, width, height, skip_formatting=True)
                plan_cache_hit = False
            else:
                plan, plan_cache_hit = self._get_plan(viewer, width, height)
            plan_end = perf_counter()
            if recorder:
                recorder.record_perf(
                    phase="render.table.plan",
                    duration_ms=(plan_end - plan_start) * 1000,
                    payload={
                        "context": "tui",
                        "plan_cache": "format_skip"
                        if fast_scroll
                        else ("hit" if plan_cache_hit else "miss"),
                    },
                )

            row_positions = viewer.visible_row_positions
            frozen_rows = viewer.visible_frozen_row_count
            self._style_resolve_ns = 0
            self._style_resolve_calls = 0
            self._style_resolve_enabled = recorder is not None
            try:
                line_start = perf_counter()
                rendered, line_stats = self._render_lines(
                    plan,
                    height,
                    row_positions=row_positions,
                    frozen_rows=frozen_rows,
                )
                line_end = perf_counter()
            finally:
                self._style_resolve_enabled = False

            if recorder:
                recorder.record_perf(
                    phase="render.table.lines",
                    duration_ms=(line_end - line_start) * 1000,
                    payload={
                        "context": "tui",
                        "rendered_lines": line_stats["rendered"],
                        "reused_lines": line_stats["reused"],
                    },
                )
                recorder.record_perf(
                    phase="render.table.styles",
                    duration_ms=self._style_resolve_ns / 1_000_000,
                    payload={
                        "context": "tui",
                        "calls": self._style_resolve_calls,
                    },
                )
        render_end = perf_counter()

        status_text = ""
        status_dirty = True
        status_dirty_fn = getattr(viewer, "is_status_dirty", None)
        if callable(status_dirty_fn):
            with suppress(Exception):
                status_dirty = bool(status_dirty_fn())
        if recorder is not None or status_dirty or not self._status_initialized:
            status_ctx = (
                recorder.perf_timer(
                    "render.status",
                    payload={"context": "tui", "trigger": "refresh"},
                )
                if recorder
                else nullcontext()
            )
            status_fragments: StyleAndTextTuples = []
            with status_ctx:
                status_fragments = render_status_line(viewer)
            self._set_status(status_fragments)
            viewer.acknowledge_status_rendered()
            self._status_initialized = True
            status_text = "".join(fragment for _, fragment in status_fragments)

        if recorder:
            state_snapshot = viewer_state_snapshot(viewer)
            recorder.record_state(state_snapshot)
            if status_text:
                recorder.record_status(status_text)

        if recorder:
            self._maybe_record_line_styles(rendered, recorder)

        cursor_position = self._locate_cursor(rendered)

        fragments: list[StyleAndTextTuples] = [line.fragments for line in rendered]
        line_count = len(rendered)
        self._last_content_line_count = line_count
        self._last_content_height = height

        content = UIContent(
            get_line=lambda line_index: fragments[line_index],
            line_count=line_count,
            cursor_position=cursor_position,
            show_cursor=True,
        )

        paint_end = perf_counter()

        if recorder and not budget_plan.is_default():
            recorder.record(
                "render_budget",
                {
                    "avg_ms": self._budget_guard.average_ms,
                    "render_ms": (render_end - render_start) * 1000,
                    "paint_ms": (paint_end - render_end) * 1000,
                },
            )

        self._budget_guard.record_frame(
            (render_end - render_start) * 1000,
            (paint_end - render_end) * 1000,
        )

        if recorder:
            plain_lines: list[str] = []
            plain_bytes = 0
            fragment_count = 0
            for line in rendered:
                plain_lines.append(line.plain_text)
                plain_bytes += len(line.plain_text)
                fragment_count += len(line.fragments)

            frame_lines = plain_lines[:]
            frame_width = max((len(line) for line in frame_lines), default=0)
            frame_status = status_text
            if frame_width:
                frame_lines = [line.ljust(frame_width) for line in frame_lines]
                if frame_status:
                    if len(frame_status) != frame_width:
                        frame_status = "".join(
                            fragment
                            for _, fragment in render_status_line(
                                _StatusWidthProxy(viewer, frame_width)
                            )
                        )
                    frame_status = frame_status[:frame_width].ljust(frame_width)
            if frame_status:
                frame_lines.append(frame_status)
            frame_capture = "\n".join(frame_lines)
            recorder.record_frame(
                frame_text=frame_capture,
                frame_hash=frame_hash(frame_capture),
            )
            recorder.record(
                "render_stats",
                {
                    "component": "table_control",
                    "lines": len(rendered),
                    "rendered_lines": line_stats["rendered"],
                    "reused_lines": line_stats["reused"],
                    "row_shift": line_stats.get("row_shift"),
                    "plan_cache": "format_skip"
                    if fast_scroll
                    else ("hit" if plan_cache_hit else "miss"),
                    "plain_bytes": plain_bytes,
                    "fragment_count": fragment_count,
                    "coalesced_steps": coalesced_steps,
                    "overscan_rows": overscan_rows,
                    "format_skip": fast_scroll,
                },
            )

        self._last_plan_cache_hit = plan_cache_hit
        self._last_frame_finished_at = paint_end
        self._last_coalesced_steps = coalesced_steps
        self._last_overscan_rows = overscan_rows
        self._fast_scroll_active = fast_scroll

        try:
            return content
        finally:
            self._current_budget_plan = _BudgetPlan()
            if self._apply_budget_plan is not None:
                self._apply_budget_plan(_BudgetPlan())

    def mouse_handler(self, mouse_event: MouseEvent) -> NotImplementedOrNone:  # noqa: D401
        """Translate mouse wheel events into queued viewer moves."""

        controller = getattr(self._apply_pending_moves, "__self__", None)
        refresh = getattr(controller, "refresh", None) if controller is not None else None

        if mouse_event.event_type in {
            MouseEventType.SCROLL_DOWN,
            MouseEventType.SCROLL_UP,
        }:
            if controller is None:
                return NotImplemented
            queue_move = getattr(controller, "_queue_move", None)
            if queue_move is None or refresh is None:
                return NotImplemented

            direction = 1 if mouse_event.event_type == MouseEventType.SCROLL_DOWN else -1
            if MouseModifier.CONTROL in mouse_event.modifiers:
                queue_move(dc=direction)
            else:
                queue_move(dr=direction)

            refresh()
            return None

        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            if refresh is None:
                return NotImplemented
            if not self._apply_mouse_click(mouse_event):
                return NotImplemented
            refresh()
            return None

        return NotImplemented

    def _apply_mouse_click(self, mouse_event: MouseEvent) -> bool:
        plan = self._cached_plan
        width = self._last_render_width
        height = self._last_render_height
        if width is None or height is None:
            return False
        if plan is None:
            plan = compute_viewport_plan(self._viewer, width, height, skip_formatting=True)

        x = mouse_event.position.x
        y = mouse_event.position.y
        if x < 0 or y < 0:
            return False

        column_widths = [max(1, column.width) for column in plan.columns] or []
        if not column_widths:
            return False

        col_idx = self._column_index_for_x(column_widths, x)
        if col_idx is None:
            return False

        row_id, header_only = self._row_id_for_y(plan, y, height)
        if col_idx >= len(plan.columns):
            return False
        col_name = plan.columns[col_idx].name
        if header_only:
            self._jump_to_column(plan, col_idx)
            return True
        if row_id is None:
            return False
        self._jump_to_cell(plan, row_id, col_idx)
        if self._on_cell_click is not None:
            self._on_cell_click(row_id, col_name)
        return True

    def _column_index_for_x(self, column_widths: Sequence[int], x: int) -> int | None:
        cursor = 1  # skip row marker
        for idx, width in enumerate(column_widths):
            span = max(1, width) + 1
            if cursor <= x < cursor + span:
                return idx
            cursor += span
        return None

    def _row_id_for_y(self, plan: ViewportPlan, y: int, height: int) -> tuple[int | None, bool]:
        table_height = max(0, height - 1)
        line = y
        if table_height > 0:
            if line == 0:
                return None, False
            line -= 1

        has_header = bool(plan.cells and plan.cells[0] and plan.cells[0][0].role == "header")
        body_rows = plan.cells[1:] if has_header else plan.cells
        if has_header:
            if line == 0:
                return None, True
            line -= 1
            if body_rows:
                if line == 0:
                    return None, False
                line -= 1

        if line < 0 or line >= len(body_rows):
            return None, False

        row_positions = plan.row_positions
        if row_positions and line < len(row_positions):
            return row_positions[line], False
        return plan.row_offset + line, False

    def _jump_to_column(self, plan: ViewportPlan, visible_idx: int) -> bool:
        viewer = self._viewer
        if visible_idx < 0 or visible_idx >= len(plan.columns):
            return False
        col_name = plan.columns[visible_idx].name
        viewer_columns = list(getattr(viewer, "columns", ()))
        try:
            col_idx = viewer_columns.index(col_name)
        except ValueError:
            return False
        before = (viewer.cur_row, viewer.cur_col)
        viewer.cur_col = col_idx
        viewer.clamp()
        return (viewer.cur_row, viewer.cur_col) != before

    def _jump_to_cell(self, plan: ViewportPlan, row_id: int, visible_idx: int) -> bool:
        viewer = self._viewer
        if visible_idx < 0 or visible_idx >= len(plan.columns):
            return False
        col_name = plan.columns[visible_idx].name
        viewer_columns = list(getattr(viewer, "columns", ()))
        try:
            col_idx = viewer_columns.index(col_name)
        except ValueError:
            return False
        before = (viewer.cur_row, viewer.cur_col)
        if isinstance(row_id, int):
            viewer.cur_row = row_id
        viewer.cur_col = col_idx
        viewer.clamp()
        return (viewer.cur_row, viewer.cur_col) != before

    def _render_lines(
        self,
        plan: ViewportPlan,
        height: int,
        *,
        row_positions: Sequence[int] | None = None,
        frozen_rows: int = 0,
    ) -> tuple[list[_LineRender], dict[str, int]]:
        column_widths = [max(1, column.width) for column in plan.columns] or [1]
        frozen_boundary = plan.frozen_boundary_idx
        column_overflows = compute_column_overflows(plan.columns, plan.rows > 0)
        column_widths_key = tuple(column_widths)
        column_overflows_key = tuple(column_overflows)
        cache_hits = 0
        cache_misses = 0
        row_cache_hits = 0
        row_cache_misses = 0
        used_keys: set[LineCacheKey] = set()
        highlight_top_blank, highlight_bottom_blank = determine_blank_line_highlights(plan)

        def _cache_lookup(key: LineCacheKey, builder: Callable[[], _LineRender]) -> _LineRender:
            nonlocal cache_hits, cache_misses
            cached = self._line_cache.get(key)
            if cached is not None:
                cache_hits += 1
                used_keys.add(key)
                return cached
            cache_misses += 1
            line = builder()
            self._line_cache[key] = line
            used_keys.add(key)
            return line

        def _blank_line(
            *, header: bool = False, row_active: bool = False, include_boundary: bool = True
        ) -> _LineRender:
            key = self._blank_line_key(
                column_widths_key,
                frozen_boundary,
                column_overflows_key,
                header=header,
                row_active=row_active,
                include_boundary=include_boundary,
            )
            return _cache_lookup(
                key,
                lambda: self._to_line_render(
                    build_blank_line(
                        column_widths,
                        frozen_boundary,
                        column_overflows,
                        header=header,
                        column_plans=plan.columns,
                        row_active=row_active,
                        include_boundary=include_boundary,
                    )
                ),
            )

        lines: list[_LineRender] = []

        table_height = max(0, height - 1)
        has_header = bool(plan.cells and plan.cells[0] and plan.cells[0][0].role == "header")
        body_rows = plan.cells[1:] if has_header else plan.cells
        drop_borders = self._current_budget_plan.drop_borders
        include_boundary = not drop_borders or plan.frozen_boundary_idx is not None

        row_positions_list: list[int] = []
        if row_positions:
            row_positions_list = list(row_positions)
            if len(row_positions_list) != len(body_rows):
                row_positions_list = []

        def _clipboard_region_bounds() -> tuple[int, int, int, int] | None:
            ui_state = getattr(self._viewer, "_ui_state", None)
            if not isinstance(ui_state, dict):
                return None
            anchor = ui_state.get("clipboard_region_anchor")
            if not isinstance(anchor, tuple) or len(anchor) != 2:
                return None
            anchor_row_id, anchor_col_idx = anchor
            if not isinstance(anchor_row_id, int) or not isinstance(anchor_col_idx, int):
                return None

            cur_row_id = getattr(self._viewer, "cur_row", None)
            cur_col_idx = getattr(self._viewer, "cur_col", None)
            if not isinstance(cur_row_id, int) or not isinstance(cur_col_idx, int):
                return None

            row_lo_id = min(anchor_row_id, cur_row_id)
            row_hi_id = max(anchor_row_id, cur_row_id)
            col_lo = min(anchor_col_idx, cur_col_idx)
            col_hi = max(anchor_col_idx, cur_col_idx)
            return row_lo_id, row_hi_id, col_lo, col_hi

        region_bounds = _clipboard_region_bounds()
        region_sig = region_bounds
        visible_column_index: dict[str, int] = {}
        for idx, name in enumerate(getattr(self._viewer, "columns", ())):
            if name not in visible_column_index:
                visible_column_index[name] = idx
        visible_col_indices = [visible_column_index.get(column.name) for column in plan.columns]

        if table_height > 0:
            lines.append(
                _blank_line(
                    header=has_header,
                    row_active=highlight_top_blank,
                    include_boundary=False,
                )
            )

        if has_header:
            header_cells = plan.cells[0]
            if region_bounds is not None:
                _row_lo_id, _row_hi_id, col_lo, col_hi = region_bounds
                header_cells = [
                    _RegionCell(cell, True)
                    if (
                        (col_idx := visible_col_indices[idx]) is not None
                        and col_lo <= col_idx <= col_hi
                    )
                    else cell
                    for idx, cell in enumerate(header_cells)
                ]
            header_key = self._row_line_key(
                header_cells,
                column_widths_key,
                column_overflows_key,
                frozen_boundary,
                is_header=True,
                include_boundary=include_boundary,
                overflow_left=plan.has_left_overflow,
                overflow_right=plan.has_right_overflow,
            )
            lines.append(
                _cache_lookup(
                    header_key,
                    lambda cells=header_cells: self._to_line_render(
                        apply_overflow_indicators(
                            build_row_line(
                                cells,
                                column_widths,
                                frozen_boundary,
                                column_overflows,
                                is_header=True,
                                row_active=False,
                                column_plans=plan.columns,
                                include_boundary=include_boundary,
                            ),
                            show_left=plan.has_left_overflow,
                            show_right=plan.has_right_overflow,
                            is_header=True,
                        )
                    ),
                )
            )
            if body_rows:
                sep_key = self._separator_line_key(
                    column_widths_key,
                    frozen_boundary=frozen_boundary if include_boundary else None,
                )
                lines.append(
                    _cache_lookup(
                        sep_key,
                        lambda: self._to_line_render(
                            build_separator_line(
                                column_widths,
                                frozen_boundary=frozen_boundary if include_boundary else None,
                            )
                        ),
                    )
                )

        def _render_body_line(row: list[Cell], *, body_index: int) -> _LineRender:
            if region_bounds is not None and row_positions_list:
                row_lo_id, row_hi_id, col_lo, col_hi = region_bounds
                if body_index < len(row_positions_list):
                    row_id = row_positions_list[body_index]
                    if row_lo_id <= row_id <= row_hi_id:
                        row = [
                            _RegionCell(cell, True)
                            if (
                                visible_col_indices[idx] is not None
                                and col_lo <= visible_col_indices[idx] <= col_hi
                            )
                            else cell
                            for idx, cell in enumerate(row)
                        ]
            return self._to_line_render(
                build_row_line(
                    row,
                    column_widths,
                    frozen_boundary,
                    column_overflows,
                    is_header=False,
                    column_plans=plan.columns,
                    include_boundary=include_boundary,
                )
            )

        frozen_count = 0
        if row_positions_list:
            frozen_count = min(max(0, frozen_rows), len(body_rows), len(row_positions_list))

        frozen_rows_cells = body_rows[:frozen_count]
        scroll_rows_cells = body_rows[frozen_count:]
        scroll_positions = row_positions_list[frozen_count:] if row_positions_list else []

        row_shift: int | None = None
        for idx, row in enumerate(frozen_rows_cells):
            lines.append(_render_body_line(row, body_index=idx))
            row_cache_misses += 1

        scroll_lines: list[_LineRender] = []
        if scroll_rows_cells:
            active_col_index = None
            for idx, column in enumerate(plan.columns):
                if column.header_active:
                    active_col_index = idx
                    break
            plan_hash = None
            plan_hash_fn = getattr(self._viewer, "plan_hash", None)
            if callable(plan_hash_fn):
                with suppress(Exception):
                    plan_hash = plan_hash_fn()
            epoch = self._current_epoch(self._viewer)

            row_cache_key = (
                plan_hash,
                epoch,
                tuple(column.name for column in plan.columns),
                column_widths_key,
                column_overflows_key,
                frozen_boundary,
                include_boundary,
                frozen_count,
                active_col_index,
                region_sig,
                getattr(self._viewer, "selection_epoch", None),
                self._current_theme_epoch,
                self._current_budget_plan.minimal_styles,
                self._current_budget_plan.drop_borders,
            )

            cache = self._row_line_cache
            if (
                cache is not None
                and cache.key == row_cache_key
                and scroll_positions
                and len(scroll_positions) == len(scroll_rows_cells)
                and len(scroll_positions) == len(cache.positions)
                and len(cache.lines) == len(scroll_rows_cells)
            ):
                shift = self._infer_row_shift(cache.positions, scroll_positions)
            else:
                shift = None

            rendered_indices: set[int] = set()
            if shift is not None:
                row_shift = shift
                lines_deque = cache.lines
                if shift > 0:
                    for _ in range(min(shift, len(lines_deque))):
                        lines_deque.popleft()
                    start_idx = max(0, len(scroll_rows_cells) - shift)
                    for idx in range(start_idx, len(scroll_rows_cells)):
                        lines_deque.append(
                            _render_body_line(
                                scroll_rows_cells[idx],
                                body_index=frozen_count + idx,
                            )
                        )
                        rendered_indices.add(idx)
                elif shift < 0:
                    shift_up = -shift
                    for _ in range(min(shift_up, len(lines_deque))):
                        lines_deque.pop()
                    for idx in range(shift_up - 1, -1, -1):
                        lines_deque.appendleft(
                            _render_body_line(
                                scroll_rows_cells[idx],
                                body_index=frozen_count + idx,
                            )
                        )
                        rendered_indices.add(idx)

                active_row = getattr(self._viewer, "cur_row", None)
                if active_row != cache.active_row and scroll_positions:
                    pos_to_index = {pos: idx for idx, pos in enumerate(scroll_positions)}
                    for row_id in (cache.active_row, active_row):
                        idx = pos_to_index.get(row_id)
                        if idx is None or idx in rendered_indices:
                            continue
                        lines_deque[idx] = _render_body_line(
                            scroll_rows_cells[idx],
                            body_index=frozen_count + idx,
                        )
                        rendered_indices.add(idx)

                scroll_lines = list(lines_deque)
                row_cache_hits += len(scroll_rows_cells) - len(rendered_indices)
                row_cache_misses += len(rendered_indices)
                self._row_line_cache = _RowLineCache(
                    key=row_cache_key,
                    positions=tuple(scroll_positions),
                    lines=lines_deque,
                    active_row=active_row,
                )
            else:
                scroll_lines = [
                    _render_body_line(row, body_index=frozen_count + idx)
                    for idx, row in enumerate(scroll_rows_cells)
                ]
                row_cache_misses += len(scroll_lines)
                if scroll_positions:
                    self._row_line_cache = _RowLineCache(
                        key=row_cache_key,
                        positions=tuple(scroll_positions),
                        lines=deque(scroll_lines),
                        active_row=getattr(self._viewer, "cur_row", None),
                    )
                else:
                    self._row_line_cache = None
        else:
            self._row_line_cache = None

        lines.extend(scroll_lines)

        if height > 0:
            lines.append(_blank_line(row_active=highlight_bottom_blank, include_boundary=False))

        stats = {
            "reused": cache_hits + row_cache_hits,
            "rendered": cache_misses + row_cache_misses,
            "row_shift": row_shift,
        }
        current_cache = self._line_cache
        self._line_cache = {key: current_cache[key] for key in used_keys if key in current_cache}
        return lines, stats

    def _should_skip_formatting(
        self,
        viewer: Viewer,
        *,
        pending_before: int,
        base_steps: int,
        budget_plan: _BudgetPlan,
        previous_direction: int,
    ) -> bool:
        if not self._strategy_allows_fast_scroll(viewer):
            return False
        backlog = max(0, pending_before)
        fast_backlog = max(2, base_steps * 2)
        if backlog >= fast_backlog:
            return True
        if not budget_plan.is_default():
            return True
        return self._fast_scroll_active and (
            backlog > 0 or self._is_previous_frame_hot(previous_direction)
        )

    def _strategy_allows_fast_scroll(self, viewer: Viewer) -> bool:
        row_provider = getattr(viewer, "row_provider", None)
        if row_provider is None:
            return True
        strategy = None
        strategy_getter = getattr(row_provider, "current_strategy", None)
        if callable(strategy_getter):
            with suppress(Exception):
                strategy = strategy_getter()
        if strategy is None:
            strategy = getattr(row_provider, "_strategy", None)
        if strategy is None:
            return True
        return bool(getattr(strategy, "downgrade_formatting_on_fast_scroll", True))

    def _locate_cursor(self, lines: list[_LineRender]) -> Point:
        line_index = 0
        cursor_x = 0
        for idx, line in enumerate(lines):
            cx = getattr(line, "cursor_x", None)
            if cx is not None:
                line_index = idx
                cursor_x = cx
                break
        return Point(x=cursor_x, y=line_index)

    def _to_line_render(self, line: RenderedLine) -> _LineRender:
        fragments: StyleAndTextTuples = []
        last_style: str | None = None
        for segment in line.segments:
            style = self._style_from_classes(segment.classes)
            if style == last_style and fragments:
                prev_style, prev_text = fragments[-1]
                fragments[-1] = (prev_style, prev_text + segment.text)
            else:
                fragments.append((style, segment.text))
            last_style = style
        return _LineRender(fragments, line.plain_text, line.cursor_x, line)

    def _style_from_classes(self, classes: Sequence[str]) -> str:
        filtered = self._filter_classes(classes)
        if not filtered:
            return ""
        cached = self._style_cache.get(filtered)
        if cached is not None:
            return cached
        resolver = get_active_style_resolver()
        if self._style_resolve_enabled:
            start_ns = perf_counter_ns()
            style = resolver.prompt_toolkit_style_for_classes(filtered)
            self._style_resolve_ns += perf_counter_ns() - start_ns
            self._style_resolve_calls += 1
        else:
            style = resolver.prompt_toolkit_style_for_classes(filtered)
        resolved = style or ""
        self._style_cache[filtered] = resolved
        return resolved

    def _filter_classes(self, classes: Sequence[str]) -> tuple[str, ...]:
        if not self._current_budget_plan.minimal_styles:
            return classes if isinstance(classes, tuple) else tuple(classes)

        essential = {
            "table",
            "table.header",
            "table.header.region",
            "table.cell",
            "table.cell.null",
            "table.cell.region",
            "table.row.active",
            "table.row.selected",
            "table.row.selected.active",
            "table.cell.active",
            "table.cell.active.selected",
            "table.col.active",
            "table.header.active",
            "table.header.sorted",
            "table.separator",
            "table.separator.active",
            "table.overflow_indicator",
        }
        return tuple(cls for cls in classes if cls in essential)

    def _maybe_record_line_styles(self, lines: Sequence[_LineRender], recorder: Recorder) -> None:
        if self._recorded_style_epoch == self._current_theme_epoch:
            return

        resolver = get_active_style_resolver()
        captured: list[dict[str, Any]] = []

        for index, line in enumerate(lines):
            source = line.source
            if source is None:
                continue
            if not any("table.header" in segment.classes for segment in source.segments):
                continue

            segments_payload: list[dict[str, Any]] = []
            for segment in source.segments:
                components = resolver.resolve(segment.classes)
                segments_payload.append(
                    {
                        "text": segment.text,
                        "classes": list(segment.classes),
                        "foreground": components.foreground,
                        "background": components.background,
                        "extras": list(components.extras),
                    }
                )

            if segments_payload:
                captured.append(
                    {
                        "line_index": index,
                        "plain_text": source.plain_text,
                        "segments": segments_payload,
                    }
                )
            break

        if not captured:
            return

        recorder.record_render_line_styles(
            component="table_control",
            lines=captured,
            metadata={"theme_epoch": self._current_theme_epoch},
        )
        self._recorded_style_epoch = self._current_theme_epoch

    def _get_plan(self, viewer: Viewer, width: int, height: int) -> tuple[ViewportPlan, bool]:
        selection_fetch_deadline = getattr(viewer, "_selection_fetch_defer_until_ns", None)
        if selection_fetch_deadline is not None and perf_counter_ns() >= selection_fetch_deadline:
            self._cached_plan = None
            self._plan_cache_key = None
            self._row_line_cache = None

        key_hint = self._make_plan_key(viewer, width, height)
        if self._cached_plan is not None and self._plan_cache_key == key_hint:
            if self._refresh_plan_active_state(self._cached_plan, viewer):
                with suppress(Exception):
                    viewer.mark_status_dirty()
            return self._cached_plan, True

        viewer._theme_epoch = self._current_theme_epoch
        plan = compute_viewport_plan(viewer, width, height)
        epoch = self._current_epoch(viewer)
        selection_epoch = getattr(viewer, "selection_epoch", None)
        view_id = self._view_identity(viewer)
        self._cached_plan = plan
        self._plan_cache_key = (
            view_id,
            plan.row_offset,
            plan.col_offset,
            width,
            height,
            epoch,
            selection_epoch,
            self._current_theme_epoch,
        )
        # Column level cache must be invalidated when plan changes.
        self._line_cache = {}
        return plan, False

    def _make_plan_key(self, viewer: Viewer, width: int, height: int) -> PlanCacheKey:
        view_id = self._view_identity(viewer)
        row_offset = self._estimate_row_offset(viewer)
        col_offset = max(0, getattr(viewer, "col0", 0))
        epoch = self._current_epoch(viewer)
        theme_ep = getattr(self, "_current_theme_epoch", theme_epoch())
        selection_epoch = getattr(viewer, "selection_epoch", None)
        return (
            view_id,
            row_offset,
            col_offset,
            width,
            height,
            epoch,
            selection_epoch,
            theme_ep,
        )

    def _refresh_plan_active_state(self, plan: ViewportPlan, viewer: Viewer) -> bool:
        cur_row = getattr(viewer, "cur_row", None)
        cur_col = getattr(viewer, "cur_col", None)
        visible_names = [column.name for column in plan.columns]
        current_visible_col_index: int | None = None
        viewer_columns = list(getattr(viewer, "columns", ()))
        if isinstance(cur_col, int) and 0 <= cur_col < len(viewer_columns):
            current_col_name = viewer_columns[cur_col]
            if current_col_name in visible_names:
                current_visible_col_index = visible_names.index(current_col_name)
            elif visible_names:
                current_visible_col_index = 0
        if current_visible_col_index is None and visible_names and isinstance(cur_col, int):
            current_visible_col_index = min(cur_col, len(visible_names) - 1)

        old_active_col_index: int | None = None
        for idx, column in enumerate(plan.columns):
            if column.header_active:
                old_active_col_index = idx
                break

        old_active_row = getattr(plan, "active_row_index", None)
        active_row_changed = cur_row != old_active_row
        active_col_changed = current_visible_col_index != old_active_col_index
        if not active_row_changed and not active_col_changed:
            return False

        if active_col_changed:
            for idx, column in enumerate(plan.columns):
                column.header_active = idx == current_visible_col_index

        if isinstance(cur_row, int):
            plan.active_row_index = cur_row

        if not plan.cells:
            return True

        header_offset = (
            1
            if plan.cells and plan.cells[0] and getattr(plan.cells[0][0], "role", None) == "header"
            else 0
        )
        body_rows = plan.cells[header_offset:]

        row_positions = list(getattr(viewer, "visible_row_positions", []) or [])
        positions_valid = len(row_positions) == plan.rows and len(body_rows) == plan.rows
        positions_map = (
            {pos: idx for idx, pos in enumerate(row_positions)} if positions_valid else {}
        )

        def _row_is_active(body_index: int) -> bool:
            if not isinstance(cur_row, int):
                return False
            if positions_valid:
                return row_positions[body_index] == cur_row
            return plan.row_offset + body_index == cur_row

        def _body_index_for(row_id: int | None) -> int | None:
            if not isinstance(row_id, int):
                return None
            if positions_valid:
                return positions_map.get(row_id)
            return row_id - plan.row_offset

        if active_col_changed and header_offset:
            header_row = plan.cells[0]
            for ci, cell in enumerate(header_row):
                col_active = (
                    current_visible_col_index is not None and ci == current_visible_col_index
                )
                cell.active_row = False
                cell.active_col = col_active
                cell.active_cell = col_active

        if active_col_changed:
            for body_index, row in enumerate(body_rows):
                row_active = _row_is_active(body_index)
                for ci, cell in enumerate(row):
                    col_active = (
                        current_visible_col_index is not None and ci == current_visible_col_index
                    )
                    cell.active_row = row_active
                    cell.active_col = col_active
                    cell.active_cell = row_active and col_active
            return True

        if not active_row_changed:
            return False

        for row_id in (old_active_row, cur_row):
            body_index = _body_index_for(row_id)
            if body_index is None:
                continue
            if body_index < 0 or body_index >= len(body_rows):
                continue
            row_active = _row_is_active(body_index)
            row = body_rows[body_index]
            for ci, cell in enumerate(row):
                col_active = (
                    current_visible_col_index is not None and ci == current_visible_col_index
                )
                cell.active_row = row_active
                cell.active_col = col_active
                cell.active_cell = row_active and col_active

        return True

    def _estimate_row_offset(self, viewer: Viewer) -> int:
        row0 = max(0, getattr(viewer, "row0", 0))
        frozen_rows = getattr(viewer, "visible_frozen_row_count", 0)
        if isinstance(frozen_rows, int) and frozen_rows > 0:
            row0 = max(row0, frozen_rows)
        return row0

    def _current_epoch(self, viewer: Viewer) -> Any:
        sheet = getattr(viewer, "sheet", None)
        if sheet is not None:
            version = getattr(sheet, "cache_version", None)
            if version is not None:
                return version
        generation_getter = getattr(viewer, "job_generation", None)
        if callable(generation_getter):
            try:
                return generation_getter()
            except Exception:  # pragma: no cover - defensive
                return None
        return None

    def _view_identity(self, viewer: Viewer) -> Any:
        sheet_id = getattr(viewer, "sheet_id", None)
        if sheet_id is not None:
            return sheet_id
        return id(viewer)

    def _invalidate_cache(self) -> None:
        self._cached_plan = None
        self._plan_cache_key = None
        self._line_cache = {}
        self._row_line_cache = None
        self._style_cache = {}

    def _infer_row_shift(self, previous: Sequence[int], current: Sequence[int]) -> int | None:
        previous_list = list(previous)
        current_list = list(current)
        if len(previous_list) != len(current_list) or not previous_list:
            return None
        if previous_list == current_list:
            return 0

        down_shift = None
        with suppress(ValueError):
            down_shift = previous_list.index(current_list[0])
        if (
            down_shift
            and 0 < down_shift < len(previous_list)
            and previous_list[down_shift:] == current_list[:-down_shift]
        ):
            return down_shift

        up_shift = None
        with suppress(ValueError):
            up_shift = current_list.index(previous_list[0])
        if (
            up_shift
            and 0 < up_shift < len(previous_list)
            and current_list[up_shift:] == previous_list[:-up_shift]
        ):
            return -up_shift

        return None

    def _row_line_key(
        self,
        cells: list[Cell],
        column_widths: tuple[int, ...],
        column_overflows: tuple[bool, ...],
        frozen_boundary: int | None,
        *,
        is_header: bool,
        include_boundary: bool,
        overflow_left: bool = False,
        overflow_right: bool = False,
    ) -> LineCacheKey:
        cell_key: tuple[Any, ...] = tuple(
            (
                cell.text,
                cell.active_row,
                cell.active_col,
                cell.active_cell,
                getattr(cell, "selected_row", False),
                getattr(cell, "region_selected", False),
                cell.role,
            )
            for cell in cells
        )
        return (
            "row",
            is_header,
            include_boundary,
            column_widths,
            frozen_boundary,
            column_overflows,
            cell_key,
            overflow_left,
            overflow_right,
            self._current_theme_epoch,
            self._current_budget_plan.minimal_styles,
            self._current_budget_plan.drop_borders,
        )

    def _blank_line_key(
        self,
        column_widths: tuple[int, ...],
        frozen_boundary: int | None,
        column_overflows: tuple[bool, ...],
        *,
        header: bool,
        row_active: bool,
        include_boundary: bool,
    ) -> LineCacheKey:
        return (
            "blank",
            header,
            row_active,
            column_widths,
            frozen_boundary,
            column_overflows,
            include_boundary,
            self._current_theme_epoch,
            self._current_budget_plan.minimal_styles,
            self._current_budget_plan.drop_borders,
        )

    def _separator_line_key(
        self, column_widths: tuple[int, ...], *, frozen_boundary: int | None
    ) -> LineCacheKey:
        return (
            "separator",
            column_widths,
            frozen_boundary,
            self._current_theme_epoch,
            self._current_budget_plan.drop_borders,
        )

    def _apply_pending_moves_with_coalesce(
        self,
        budget_plan: _BudgetPlan,
        previous_direction: int,
        base_steps: int,
        controller: Any | None,
    ) -> tuple[int, int, int]:
        viewer = self._viewer
        before_row = getattr(viewer, "cur_row", 0)

        self._apply_pending_moves()

        after_row = getattr(viewer, "cur_row", before_row)
        delta = after_row - before_row
        direction = 0
        if delta > 0:
            direction = 1
        elif delta < 0:
            direction = -1
        consumed = abs(delta)
        total_moved = consumed
        coalesced = 0

        if (
            direction != 0
            and controller is not None
            and self._is_previous_frame_hot(previous_direction)
        ):
            pending_remaining = getattr(controller, "_pending_row_delta", 0)
            pending_same_dir = (
                max(0, int(pending_remaining)) if direction > 0 else max(0, -int(pending_remaining))
            )
            if pending_same_dir > 0:
                multiplier = float(getattr(budget_plan, "coalesce_multiplier", 1.0) or 1.0)
                multiplier = min(4.0, max(1.0, multiplier))
                max_allowed = max(base_steps, int(round(base_steps * multiplier)))
                remaining_budget = max(0, max_allowed - consumed)
                if remaining_budget > 0:
                    move_fn = getattr(viewer, "move_down" if direction > 0 else "move_up", None)
                    if callable(move_fn):
                        before_extra_row = after_row
                        move_fn(min(pending_same_dir, remaining_budget))
                        new_row = getattr(viewer, "cur_row", before_extra_row)
                        actual_extra = new_row - after_row if direction > 0 else after_row - new_row
                        actual_extra = max(0, actual_extra)
                        if actual_extra > 0:
                            total_moved += actual_extra
                            coalesced = actual_extra
                            if direction > 0:
                                with suppress(Exception):
                                    controller._pending_row_delta = max(
                                        0,
                                        int(getattr(controller, "_pending_row_delta", 0))
                                        - actual_extra,
                                    )
                            else:
                                with suppress(Exception):
                                    controller._pending_row_delta = min(
                                        0,
                                        int(getattr(controller, "_pending_row_delta", 0))
                                        + actual_extra,
                                    )

        if total_moved > 0:
            self._last_move_direction = direction
            self._last_move_time = perf_counter()
        else:
            self._last_move_direction = 0
        self._last_coalesced_steps = coalesced
        return direction, total_moved, coalesced

    def _compute_burst_multiplier(
        self, pending_rows: int, base_steps: int, previous_direction: int
    ) -> float:
        if base_steps <= 0:
            return 1.0
        if pending_rows <= base_steps:
            return 1.0
        if not self._is_previous_frame_hot(previous_direction):
            return 1.0
        blocks = (pending_rows + base_steps - 1) // base_steps
        extra = max(0, min(3, blocks - 1))
        if extra <= 0:
            return 1.0
        return 1.0 + float(extra)

    def _is_previous_frame_hot(self, previous_direction: int) -> bool:
        if previous_direction == 0:
            return False
        last_finish = self._last_frame_finished_at
        if last_finish is None:
            return False
        return (perf_counter() - last_finish) <= self._coalesce_hot_window

    def _maybe_prime_overscan(
        self,
        viewer: Viewer,
        height: int,
        budget_plan: _BudgetPlan,
        direction: int,
        previous_direction: int,
        controller: Any | None,
    ) -> int:
        max_extra_from_budget: int | None = None
        if budget_plan.overscan_hint is not None:
            try:
                hint_value = int(budget_plan.overscan_hint)
            except (TypeError, ValueError):  # pragma: no cover - defensive
                hint_value = 0
            body_height = max(0, height - 1)
            max_extra_from_budget = max(0, hint_value - body_height)
        hot_motion = self._is_previous_frame_hot(previous_direction)
        if not hot_motion:
            # Allow immediate same-direction scrolls even if the previous frame fell
            # outside the hot window (e.g. under CI load) so overscan still primes.
            same_direction = direction != 0 and direction == previous_direction
            if not same_direction:
                return 0
        if direction == 0:
            pending = (
                abs(int(getattr(controller, "_pending_row_delta", 0)))
                if controller is not None
                else 0
            )
            if pending <= 0:
                return 0
        body_height = max(0, height - 1)
        if body_height <= 0:
            return 0
        overscan_rows = int(body_height * self._overscan_ratio)
        if overscan_rows <= 0 and body_height > 0:
            overscan_rows = 1
        overscan_rows = min(overscan_rows, body_height * 3)
        if max_extra_from_budget is not None:
            overscan_rows = min(overscan_rows, max_extra_from_budget)
        if overscan_rows <= 0:
            return 0
        columns = self._visible_column_names(viewer)
        if not columns:
            return 0
        try:
            viewer.request_frame_overscan_hint(body_height + overscan_rows)
        except Exception:  # pragma: no cover - defensive
            return 0
        return overscan_rows

    def _visible_column_names(self, viewer: Viewer) -> list[str]:
        columns = getattr(viewer, "visible_cols", None)
        if columns:
            return list(columns)
        columns = getattr(viewer, "columns", None)
        if columns:
            return list(columns)
        return []
