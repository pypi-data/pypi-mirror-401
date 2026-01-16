from __future__ import annotations

import contextlib
import math
import threading
import weakref
from collections import OrderedDict, deque
from collections.abc import Callable, Sequence
from concurrent.futures import Future
from dataclasses import dataclass, field
from time import monotonic_ns
from typing import TYPE_CHECKING, Any, ClassVar

from ...config.settings import CACHE_DEFAULTS, STREAMING_DEFAULTS
from ...utils import _boot_trace
from ..engine.contracts import TableSlice, TableSliceComposite, TableSliceLike, TableSliceView
from ..formatting import _format_float_two_decimals, _is_float_like
from ..plan import QueryPlan, normalized_columns_key
from ..row_provider import SliceStatus, SliceStreamRequest, TableSliceChunk

if TYPE_CHECKING:
    from .viewer import Viewer


_BOOT_TRACE_FIRST_VIEWPORT = True


@dataclass(slots=True)
class FreezePaneController:
    """Manage frozen row/column state for a :class:`Viewer`."""

    viewer: Viewer
    column_count: int = 0
    row_count: int = 0
    _columns_cache_valid: bool = False
    _column_indices_cache: tuple[int, ...] = field(default_factory=tuple)
    _column_names_cache: tuple[str, ...] = field(default_factory=tuple)
    _column_index_set_cache: frozenset[int] = frozenset()
    _column_name_set_cache: frozenset[str] = frozenset()

    def invalidate_cache(self) -> None:
        self._columns_cache_valid = False

    def ensure_cache(self) -> None:
        if self._columns_cache_valid:
            return

        viewer = self.viewer
        if self.column_count <= 0:
            self._column_indices_cache = ()
            self._column_names_cache = ()
            self._column_index_set_cache = frozenset()
            self._column_name_set_cache = frozenset()
            self._columns_cache_valid = True
            return

        indices: list[int] = []
        names: list[str] = []
        for idx, name in enumerate(viewer.columns):
            if name in viewer._hidden_cols:
                continue
            indices.append(idx)
            names.append(name)
            if len(indices) >= self.column_count:
                break

        self._column_indices_cache = tuple(indices)
        self._column_names_cache = tuple(names)
        self._column_index_set_cache = frozenset(indices)
        self._column_name_set_cache = frozenset(names)
        self._columns_cache_valid = True

    def column_indices(self) -> list[int]:
        self.ensure_cache()
        return list(self._column_indices_cache)

    def first_scrollable_col_index(self) -> int:
        indices = self.column_indices()
        if not indices:
            return 0
        last = indices[-1]
        return min(len(self.viewer.columns), last + 1)

    def is_column_frozen(self, idx: int) -> bool:
        self.ensure_cache()
        return idx in self._column_index_set_cache

    def effective_row_count(self) -> int:
        return max(0, self.row_count)

    def reserved_view_rows(self) -> int:
        viewer = self.viewer

        if viewer.view_height <= 1:
            return 0

        visible = viewer.visible_frozen_row_count
        if visible <= 0:
            visible = self.effective_row_count()
        return max(0, min(visible, viewer.view_height - 1))

    def body_view_height(self) -> int:
        viewer = self.viewer
        reserved = self.reserved_view_rows()
        margin = 1 if reserved and (viewer.view_height - reserved) >= 2 else 0
        return max(1, viewer.view_height - reserved - margin)

    def frozen_column_names(self) -> list[str]:
        self.ensure_cache()
        return list(self._column_names_cache)

    def column_index_set(self) -> frozenset[int]:
        self.ensure_cache()
        return self._column_index_set_cache

    def column_name_set(self) -> frozenset[str]:
        self.ensure_cache()
        return self._column_name_set_cache

    def set_frozen_columns(self, count: int) -> None:
        viewer = self.viewer
        new_count = max(0, count)
        if new_count == self.column_count:
            return

        self.column_count = new_count
        viewer._visible_key = None
        viewer._max_visible_col = None
        self.invalidate_cache()
        viewer.clamp()

    def set_frozen_rows(self, count: int) -> None:
        viewer = self.viewer
        new_count = max(0, count)
        if new_count == self.row_count:
            return

        self.row_count = new_count
        if self.row_count:
            viewer.row0 = max(viewer.row0, self.row_count)
        viewer.invalidate_row_cache()
        viewer.clamp()

    def clear(self) -> None:
        viewer = self.viewer
        if not (self.column_count or self.row_count):
            return

        self.column_count = 0
        self.row_count = 0
        viewer._visible_key = None
        viewer._max_visible_col = None
        self.invalidate_cache()
        viewer.invalidate_row_cache()
        viewer.clamp()


@dataclass(slots=True)
class _StreamContext:
    sheet_id: str | None
    generation: int | None
    plan_hash: str | None
    plan: Any
    columns: tuple[str, ...]
    column_count: int
    fetch_start: int
    fetch_count: int
    target_start: int
    target_end: int
    body_start: int
    body_end_needed: int
    direction: int
    backward_extra: int
    forward_extra: int
    window_cells_cap: int
    prefetch_span: int
    cache_status: str
    start_ns: int
    first_chunk_ns: int
    status: SliceStatus = SliceStatus.OK
    fetched_cells: int = 0
    batches: int = 0
    mode: str | None = None
    reason: str | None = None
    evicted_rows: int = 0
    prefetch_dir: str = "none"
    prefetch_rows: int = 0
    first_chunk_rows: int = 0
    first_chunk_cells: int = 0
    first_chunk_duration_ns: int = 0
    first_chunk_seen: bool = False
    final_rows: int = 0
    final_cells: int = 0
    final_duration_ns: int = 0
    cancelled: bool = False


@dataclass(slots=True)
class _PageCacheEntry:
    slice: TableSlice
    status: SliceStatus


@dataclass(slots=True)
class RowCacheTelemetry:
    rows_per_second: float = 0.0
    speed_tier: str = "slow"
    cache_hit_rate: float = 1.0
    bytes_copied_per_second: float = 0.0
    p50_row_cache_ms: float = 0.0
    p95_row_cache_ms: float = 0.0
    last_duration_ms: float = 0.0
    last_bytes_copied: int = 0
    last_cache_status: str = "hit"
    last_prefetch_pages: int = 0
    last_prefetch_dir: str = "none"


@dataclass(slots=True)
class RowCacheController:
    """Cache viewport slices to accelerate vertical scrolling."""

    DEFAULT_MAX_CELLS: ClassVar[int] = CACHE_DEFAULTS.viewer_row_cache_max_cells
    STREAM_JOB_PRIORITY: ClassVar[int] = 50
    APPROX_BYTES_PER_CELL: ClassVar[int] = 16
    SPEED_TIER_SLOW_UP: ClassVar[float] = 40.0
    SPEED_TIER_MEDIUM_DOWN: ClassVar[float] = 25.0
    SPEED_TIER_FAST_UP: ClassVar[float] = 140.0
    SPEED_TIER_FAST_DOWN: ClassVar[float] = 100.0
    SPEED_IDLE_RESET_NS: ClassVar[int] = 120_000_000
    OVERSCAN_FACTORS: ClassVar[dict[str, float]] = {
        "slow": 0.25,
        "medium": 0.5,
        "fast": 1.0,
    }
    PREFETCH_PAGES: ClassVar[dict[str, int]] = {
        "slow": 1,
        "medium": 2,
        "fast": 3,
    }
    PAGE_CACHE_LIMITS: ClassVar[dict[str, int]] = {
        "slow": 4,
        "medium": 6,
        "fast": 8,
    }
    TELEMETRY_WINDOW: ClassVar[int] = 60

    viewer: Viewer
    freeze: FreezePaneController
    streaming_enabled: bool = STREAMING_DEFAULTS.enabled
    streaming_batch_rows: int = STREAMING_DEFAULTS.batch_rows
    table: TableSlice | None = None
    start: int = 0
    end: int = 0
    cols: tuple[str, ...] = field(default_factory=tuple)
    plan_hash: str | None = None
    prefetch: int | None = None
    max_cells: int = DEFAULT_MAX_CELLS
    _visible_row_positions: list[int] = field(default_factory=list)
    _visible_frozen_row_count: int = 0
    _sheet_version: object | None = None
    _last_body_start: int | None = None
    _last_direction: int = 0
    _table_status: SliceStatus = SliceStatus.OK
    _last_warning_status: SliceStatus = SliceStatus.OK
    _stream_forced_eager: bool = False
    _last_body_start_sample: int | None = None
    _last_body_start_ns: int | None = None
    _last_movement_ns: int | None = None
    _rows_per_second: float = 0.0
    _speed_tier: str = "slow"
    _duration_samples_ms: deque[float] = field(
        default_factory=lambda: deque(maxlen=RowCacheController.TELEMETRY_WINDOW)
    )
    _cache_hit_samples: deque[bool] = field(
        default_factory=lambda: deque(maxlen=RowCacheController.TELEMETRY_WINDOW)
    )
    _bytes_samples: deque[tuple[int, int]] = field(
        default_factory=lambda: deque(maxlen=RowCacheController.TELEMETRY_WINDOW)
    )
    _telemetry: RowCacheTelemetry = field(default_factory=RowCacheTelemetry)
    _active_stream_future: Future[Any] | None = None
    _active_stream_generation: int | None = None
    _active_stream_start_ns: int = 0
    _active_stream_first_chunk_ns: int = 0
    _active_stream_batches: int = 0
    _active_stream_rows: int = 0
    _active_stream_cells: int = 0
    _active_stream_mode: str | None = None
    _active_stream_reason: str | None = None
    _active_stream_prefetch_dir: str = "none"
    _active_stream_prefetch_rows: int = 0
    _active_stream_evicted_rows: int = 0
    _active_stream_context: _StreamContext | None = None
    _page_cache: OrderedDict[tuple[str | None, tuple[str, ...], int], _PageCacheEntry] = field(
        default_factory=OrderedDict
    )
    _page_cache_limit: int = 4

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _cancel_active_stream(self) -> None:
        context = self._active_stream_context
        if context is not None:
            context.cancelled = True
        future = self._active_stream_future
        if future is not None:
            future.cancel()
        self._active_stream_future = None
        self._active_stream_generation = None
        self._active_stream_start_ns = 0
        self._active_stream_first_chunk_ns = 0
        self._active_stream_batches = 0
        self._active_stream_rows = 0
        self._active_stream_cells = 0
        self._active_stream_mode = None
        self._active_stream_reason = None
        self._active_stream_prefetch_dir = "none"
        self._active_stream_prefetch_rows = 0
        self._active_stream_evicted_rows = 0
        self._active_stream_context = None

    def _should_stream(self) -> bool:
        if not self.streaming_enabled:
            return False
        if self.streaming_batch_rows <= 0:
            return False
        if self._stream_forced_eager:
            return False
        viewer = self.viewer
        # In-memory viewers (no source path) should stay eager to avoid spawning
        # background stream jobs that only add noise during tests and small sessions.
        _missing = object()
        source_path = getattr(viewer, "_source_path", _missing)
        if source_path is None:
            return False
        if not callable(getattr(viewer.row_provider, "get_slice_stream", None)):
            return False
        sheet_id = getattr(viewer.sheet, "sheet_id", None)
        return sheet_id is not None

    def _trim_table_for_budget(
        self,
        table: TableSlice,
        *,
        start: int,
        body_start: int,
        body_end_needed: int,
        direction: int,
        column_count: int,
        window_cells_cap: int,
    ) -> tuple[TableSlice, int, int, int]:
        total_rows = table.height
        if total_rows <= 0:
            return table, start, start, 0

        max_rows_allowed = max(1, window_cells_cap // max(1, column_count))
        keep_start = start
        keep_end = start + total_rows

        if direction > 0:
            keep_end = min(start + total_rows, keep_start + max_rows_allowed)
            if keep_end < body_end_needed:
                keep_end = body_end_needed
                keep_start = max(start, keep_end - max_rows_allowed)
        elif direction < 0:
            keep_start = start
            keep_end = min(start + total_rows, keep_start + max_rows_allowed)
            if keep_end < body_end_needed:
                keep_end = body_end_needed
                keep_start = max(start, keep_end - max_rows_allowed)
            if keep_start > body_start:
                keep_start = body_start
                keep_end = min(start + total_rows, keep_start + max_rows_allowed)
        else:
            keep_span = max_rows_allowed
            keep_start = max(
                start,
                body_start - max(0, keep_span - (body_end_needed - body_start)) // 2,
            )
            keep_end = min(start + total_rows, keep_start + keep_span)
            if keep_start > body_start:
                keep_start = body_start
                keep_end = min(start + total_rows, keep_start + keep_span)
            if keep_end < body_end_needed:
                keep_end = body_end_needed
                keep_start = max(start, keep_end - keep_span)

        keep_start = max(start, keep_start)
        keep_end = min(start + total_rows, keep_end)
        keep_end = max(keep_end, keep_start)

        evicted_rows = 0
        trim_front = max(0, keep_start - start)
        new_table = table
        new_start = start
        if trim_front:
            new_table = new_table.slice(trim_front, total_rows - trim_front)
            new_start += trim_front
            total_rows = new_table.height
            evicted_rows += trim_front

        trim_back = max(0, (new_start + total_rows) - keep_end)
        if trim_back:
            new_table = new_table.slice(0, total_rows - trim_back)
            total_rows = new_table.height
            evicted_rows += trim_back

        new_end = new_start + total_rows
        return new_table, new_start, new_end, evicted_rows

    def _schedule_stream_fetch(
        self,
        *,
        plan: Any,
        plan_hash: str | None,
        column_list: list[str],
        column_count: int,
        fetch_start: int,
        fetch_count: int,
        body_start: int,
        body_end_needed: int,
        direction: int,
        backward_extra: int,
        forward_extra: int,
        window_cells_cap: int,
        prefetch_span: int,
        cache_status: str,
        should_record: bool,
        start_ns: int,
    ) -> bool:
        if not self._should_stream():
            return False

        viewer = self.viewer
        request = SliceStreamRequest(
            plan=plan,
            columns=tuple(column_list),
            start=fetch_start,
            count=fetch_count,
            batch_rows=self.streaming_batch_rows,
            streaming_enabled=True,
            telemetry={
                "viewer": "row_cache",
                "cache": cache_status,
            },
        )

        generation = viewer.job_generation()
        sheet_id = getattr(viewer.sheet, "sheet_id", None)

        context = _StreamContext(
            sheet_id=sheet_id,
            generation=generation,
            plan_hash=plan_hash,
            plan=plan,
            columns=tuple(column_list),
            column_count=column_count,
            fetch_start=fetch_start,
            fetch_count=fetch_count,
            target_start=fetch_start,
            target_end=fetch_start + fetch_count,
            body_start=body_start,
            body_end_needed=body_end_needed,
            direction=direction,
            backward_extra=backward_extra,
            forward_extra=forward_extra,
            window_cells_cap=window_cells_cap,
            prefetch_span=prefetch_span,
            cache_status=cache_status,
            start_ns=start_ns,
            first_chunk_ns=start_ns,
        )
        context.batches = 0
        self._cancel_active_stream()
        self._active_stream_context = context
        self._active_stream_generation = generation
        self._active_stream_start_ns = start_ns
        self._active_stream_first_chunk_ns = 0
        self._active_stream_batches = 0
        self._active_stream_rows = 0
        self._active_stream_cells = 0
        self._active_stream_mode = "stream"
        self._active_stream_reason = "scheduled"
        self._active_stream_prefetch_dir = "none"
        self._active_stream_prefetch_rows = 0
        self._active_stream_evicted_rows = 0

        self._active_stream_future = self._schedule_stream_consumer(context, request)
        return True

    def _schedule_stream_consumer(
        self, context: _StreamContext, request: SliceStreamRequest
    ) -> Future[Any] | None:
        viewer = self.viewer
        runner = viewer.job_runner
        sheet = viewer.sheet

        cols_key = normalized_columns_key(context.columns)
        tag = f"row-window:{context.plan_hash or 'none'}:{cols_key}"

        def _consume(
            _: int,
            *,
            ctx: _StreamContext = context,
            req: SliceStreamRequest = request,
        ) -> None:
            row_provider = viewer.row_provider
            try:
                iterator = row_provider.get_slice_stream(req)
            except Exception:
                ctx.cancelled = True
                return
            for chunk in iterator:
                if ctx.cancelled:
                    break
                self._deliver_stream_chunk(ctx, chunk)
                if chunk.is_final:
                    break

        try:
            future = runner.submit(
                sheet,
                tag,
                _consume,
                cache_result=False,
                priority=self.STREAM_JOB_PRIORITY,
            )
        except Exception:
            thread = threading.Thread(
                target=_consume,
                args=(context.generation or 0,),
                daemon=True,
            )
            thread.start()
            return None
        return future

    def _deliver_stream_chunk(self, context: _StreamContext, chunk: TableSliceChunk) -> None:
        viewer = self.viewer
        viewer_ref = weakref.ref(viewer)

        def _apply() -> None:
            viewer_obj = viewer_ref()
            if viewer_obj is None:
                context.cancelled = True
                return
            if context.cancelled:
                return
            if context.generation is not None and context.sheet_id is not None:
                with contextlib.suppress(Exception):
                    current_gen = viewer.job_runner.current_generation(context.sheet_id)
                    if current_gen != context.generation:
                        context.cancelled = True
                        return
            if self._active_stream_context is not context:
                return
            self._apply_stream_chunk(context, chunk)
            hooks = viewer_obj.ui_hooks
            with contextlib.suppress(Exception):
                hooks.invalidate()

        hooks = viewer.ui_hooks
        try:
            hooks.call_soon(_apply)
        except Exception:
            timer = threading.Timer(0.01, _apply)
            timer.daemon = True
            timer.start()

    def _apply_stream_chunk(self, context: _StreamContext, chunk: TableSliceChunk) -> None:
        if context.cancelled:
            return
        if self._active_stream_context is not context:
            return

        if not context.first_chunk_seen:
            context.first_chunk_seen = True
            context.first_chunk_rows = chunk.slice.height
            context.first_chunk_cells = chunk.slice.height * max(1, context.column_count)
            if context.start_ns:
                context.first_chunk_duration_ns = max(0, monotonic_ns() - context.start_ns)
            else:
                context.first_chunk_duration_ns = 0
            self._active_stream_first_chunk_ns = context.first_chunk_duration_ns
            self._active_stream_rows = context.first_chunk_rows
            self._active_stream_cells = context.first_chunk_cells
            self._active_stream_batches = max(self._active_stream_batches, 1)

        self._active_stream_mode = chunk.telemetry.get("mode", context.mode)
        if self._active_stream_mode:
            context.mode = self._active_stream_mode
        reason = chunk.telemetry.get("reason")
        if reason:
            context.reason = reason
            self._active_stream_reason = reason
        if self._active_stream_mode and self._active_stream_mode != "stream":
            self._stream_forced_eager = True

        context.status = self._combine_status(context.status, chunk.status)

        column_count = max(1, context.column_count)
        fetched_delta = chunk.slice.height * column_count
        chunk_index = chunk.telemetry.get("chunk_index")
        if chunk_index is not None:
            with contextlib.suppress(TypeError, ValueError):
                context.batches = max(context.batches, int(chunk_index))
        total_chunks = chunk.telemetry.get("chunks")
        if total_chunks is not None:
            with contextlib.suppress(TypeError, ValueError):
                context.batches = max(context.batches, int(total_chunks))
        if chunk_index is None and total_chunks is None:
            context.batches += 1
        context.fetched_cells += fetched_delta

        if self.table is None or self.table.height == 0 or chunk.is_final:
            new_table = chunk.slice
            new_start = chunk.offset
        else:
            expected_offset = self.end
            if chunk.offset < self.start or (chunk.offset == self.start and chunk.is_final):
                new_table = chunk.slice
                new_start = chunk.offset
            elif chunk.offset >= expected_offset:
                new_table = self.table.concat_vertical(chunk.slice)
                new_start = self.start
            else:
                overlap_start = max(0, chunk.offset - self.start)
                head = self.table.slice(0, overlap_start) if overlap_start > 0 else None
                tail_start = overlap_start + chunk.slice.height
                tail = None
                if tail_start < self.table.height:
                    tail = self.table.slice(tail_start, self.table.height - tail_start)
                new_table = chunk.slice
                if head is not None:
                    new_table = head.concat_vertical(new_table)
                if tail is not None:
                    new_table = new_table.concat_vertical(tail)
                new_start = self.start

        trimmed_table, trimmed_start, trimmed_end, evicted = self._trim_table_for_budget(
            new_table,
            start=new_start,
            body_start=context.body_start,
            body_end_needed=context.body_end_needed,
            direction=context.direction,
            column_count=context.column_count,
            window_cells_cap=context.window_cells_cap,
        )

        self.table = trimmed_table
        self.start = trimmed_start
        self.end = trimmed_end
        context.evicted_rows += evicted
        self._active_stream_evicted_rows = context.evicted_rows

        self._table_status = context.status

        total_rows = self.table.height if self.table is not None else 0
        self._active_stream_rows = total_rows
        self._active_stream_cells = total_rows * column_count
        self._active_stream_batches = max(self._active_stream_batches, context.batches)

        if chunk.is_final:
            context.final_rows = total_rows
            context.final_cells = total_rows * column_count
            if context.start_ns:
                context.final_duration_ns = max(0, monotonic_ns() - context.start_ns)
            self._finalize_stream_context(context)

    def _finalize_stream_context(self, context: _StreamContext) -> None:
        if context.cancelled:
            return

        viewer = self.viewer
        row_provider = viewer.row_provider
        plan = context.plan
        columns = list(context.columns)

        prefetch_dir = "none"
        prefetch_rows = 0
        if context.direction < 0:
            prefetch_start = max(0, self.start - context.backward_extra)
            prefetch_rows = self.start - prefetch_start
            if prefetch_rows > 0:
                with contextlib.suppress(Exception):
                    row_provider.prefetch(plan, columns, prefetch_start, prefetch_rows)
                    prefetch_dir = "backward"
        else:
            prefetch_start = self.end
            prefetch_rows = context.forward_extra
            if prefetch_rows > 0:
                with contextlib.suppress(Exception):
                    row_provider.prefetch(plan, columns, prefetch_start, prefetch_rows)
                    prefetch_dir = "forward"

        context.prefetch_dir = prefetch_dir
        context.prefetch_rows = prefetch_rows

        self._active_stream_prefetch_dir = prefetch_dir
        self._active_stream_prefetch_rows = prefetch_rows
        self._active_stream_future = None
        self._active_stream_context = context

    def invalidate(self) -> None:
        self._cancel_active_stream()
        self.table = None
        self.cols = ()
        self.start = 0
        self.end = 0
        self.plan_hash = None
        self._visible_row_positions = []
        self._visible_frozen_row_count = 0
        self._sheet_version = None
        self._last_body_start = None
        self._last_direction = 0
        self._table_status = SliceStatus.OK
        self._last_warning_status = SliceStatus.OK
        self._page_cache.clear()
        self._last_body_start_sample = None
        self._last_body_start_ns = None
        self._last_movement_ns = None
        self._rows_per_second = 0.0
        self._speed_tier = "slow"
        self._duration_samples_ms.clear()
        self._cache_hit_samples.clear()
        self._bytes_samples.clear()
        self._telemetry = RowCacheTelemetry()

    def get_prefetch(self, hint: int | None = None) -> int:
        """Return the number of body rows to fetch for the active viewport."""

        viewer = self.viewer
        fallback = max(viewer.view_height * 2, 64)
        base = self.prefetch if self.prefetch is not None else fallback

        if hint is None or hint <= 0:
            return max(base, viewer.view_height)

        try:
            capped = int(hint)
        except (TypeError, ValueError):  # pragma: no cover - defensive
            return max(base, viewer.view_height)

        capped = max(viewer.view_height, capped)
        if base <= capped:
            return max(base, viewer.view_height)
        return capped

    def visible_row_positions(self) -> list[int]:
        return list(self._visible_row_positions)

    def visible_frozen_row_count(self) -> int:
        return self._visible_frozen_row_count

    def telemetry_snapshot(self) -> RowCacheTelemetry:
        return self._telemetry

    def _update_speed_tier(self, rows_per_second: float, now_ns: int) -> str:
        tier = self._speed_tier
        if rows_per_second <= 0:
            if (
                self._last_movement_ns is not None
                and now_ns - self._last_movement_ns > self.SPEED_IDLE_RESET_NS
            ):
                return "slow"
            return tier

        self._last_movement_ns = now_ns

        if tier == "slow":
            if rows_per_second >= self.SPEED_TIER_SLOW_UP:
                return "medium"
            return tier
        if tier == "medium":
            if rows_per_second >= self.SPEED_TIER_FAST_UP:
                return "fast"
            if rows_per_second <= self.SPEED_TIER_MEDIUM_DOWN:
                return "slow"
            return tier
        if rows_per_second <= self.SPEED_TIER_FAST_DOWN:
            return "medium"
        return tier

    def _overscan_rows_for_tier(self, tier: str, viewport_rows: int) -> int:
        factor = self.OVERSCAN_FACTORS.get(tier, 0.25)
        return max(0, int(viewport_rows * factor))

    def _prefetch_pages_for_tier(self, tier: str) -> int:
        return max(1, self.PREFETCH_PAGES.get(tier, 1))

    def _set_page_cache_limit(self, limit: int) -> int:
        self._page_cache_limit = max(1, limit)
        evicted_rows = 0
        while len(self._page_cache) > self._page_cache_limit:
            _, entry = self._page_cache.popitem(last=False)
            evicted_rows += entry.slice.height
        return evicted_rows

    def _percentile(self, values: Sequence[float], percentile: float) -> float:
        if not values:
            return 0.0
        ordered = sorted(values)
        idx = math.ceil((len(ordered) - 1) * percentile)
        idx = max(0, min(idx, len(ordered) - 1))
        return ordered[idx]

    def _record_telemetry(
        self,
        *,
        duration_ns: int,
        fetched_cells: int,
        cache_status: str,
        rows_per_second: float,
        speed_tier: str,
        prefetch_pages: int,
        prefetch_dir: str,
    ) -> RowCacheTelemetry:
        duration_ms = duration_ns / 1_000_000 if duration_ns else 0.0
        bytes_copied = fetched_cells * self.APPROX_BYTES_PER_CELL
        self._duration_samples_ms.append(duration_ms)
        self._cache_hit_samples.append(cache_status == "hit")
        self._bytes_samples.append((bytes_copied, duration_ns))

        cache_hits = sum(1 for hit in self._cache_hit_samples if hit)
        cache_samples = self._cache_hit_samples
        cache_hit_rate = cache_hits / len(cache_samples) if cache_samples else 1.0

        total_bytes = sum(b for b, _ in self._bytes_samples)
        total_ns = sum(ns for _, ns in self._bytes_samples)
        bytes_per_second = (total_bytes / (total_ns / 1_000_000_000)) if total_ns else 0.0

        p50 = self._percentile(list(self._duration_samples_ms), 0.50)
        p95 = self._percentile(list(self._duration_samples_ms), 0.95)

        self._telemetry = RowCacheTelemetry(
            rows_per_second=rows_per_second,
            speed_tier=speed_tier,
            cache_hit_rate=cache_hit_rate,
            bytes_copied_per_second=bytes_per_second,
            p50_row_cache_ms=p50,
            p95_row_cache_ms=p95,
            last_duration_ms=duration_ms,
            last_bytes_copied=bytes_copied,
            last_cache_status=cache_status,
            last_prefetch_pages=prefetch_pages,
            last_prefetch_dir=prefetch_dir,
        )
        return self._telemetry

    def get_visible_table_slice(
        self, columns: Sequence[str], overscan_hint: int | None = None
    ) -> TableSliceLike:
        viewer = self.viewer
        call_start_ns = monotonic_ns()

        if not columns:
            self._visible_row_positions = []
            self._visible_frozen_row_count = 0
            return TableSlice.empty()

        should_record = viewer._perf_callback is not None

        height = max(1, viewer.view_height)
        column_list = list(columns)
        col_key = tuple(column_list)
        plan = viewer._current_plan()
        plan_hash = viewer.plan_hash()
        row_provider = viewer.row_provider

        frozen_target = min(self.freeze.effective_row_count(), height)
        frozen_slices: list[TableSlice] = []
        frozen_positions: list[int] = []

        overall_status = SliceStatus.OK

        actual_frozen = 0
        if frozen_target > 0:
            try:
                frozen_slice, frozen_status = row_provider.get_slice(
                    plan,
                    column_list,
                    0,
                    frozen_target,
                )
            except Exception:
                self.invalidate()
                raise
            if frozen_slice.height > 0:
                frozen_slices.append(frozen_slice)
                actual_frozen = frozen_slice.height
                frozen_positions.extend(range(actual_frozen))
                overall_status = self._combine_status(overall_status, frozen_status)

        self._visible_frozen_row_count = actual_frozen

        remaining_height = min(self.freeze.body_view_height(), max(0, height - actual_frozen))
        body_start = max(0, viewer.row0)
        if actual_frozen:
            body_start = max(body_start, actual_frozen)

        body_slice: TableSlice | TableSliceView = TableSlice.empty(column_list, viewer.schema)
        body_positions: list[int] = []

        body_start_ns = monotonic_ns() if (should_record and remaining_height > 0) else 0

        prev_direction = self._last_direction
        direction = 0
        if self._last_body_start is not None:
            if body_start > self._last_body_start:
                direction = 1
            elif body_start < self._last_body_start:
                direction = -1
            else:
                direction = self._last_direction
        self._last_body_start = body_start
        self._last_direction = direction
        direction_flip = prev_direction not in (None, 0, direction)

        rows_per_second = self._rows_per_second
        if self._last_body_start_sample is not None and self._last_body_start_ns is not None:
            delta = abs(body_start - self._last_body_start_sample)
            dt_ns = max(0, call_start_ns - self._last_body_start_ns)
            if dt_ns > 0:
                rows_per_second = (delta / dt_ns) * 1_000_000_000 if delta > 0 else 0.0
        self._last_body_start_sample = body_start
        self._last_body_start_ns = call_start_ns
        self._rows_per_second = rows_per_second
        speed_tier = self._update_speed_tier(rows_per_second, call_start_ns)
        self._speed_tier = speed_tier

        column_count = len(col_key) or 1
        page_size = max(1, row_provider.page_size)
        use_page_cache = remaining_height <= page_size
        page_stride = max(1, page_size - remaining_height) if use_page_cache else 0
        page_cells = page_size * column_count
        page_cache_limit = self.PAGE_CACHE_LIMITS.get(speed_tier, 4)
        if self.max_cells > 0 and page_cells > 0:
            max_pages_for_budget = max(1, self.max_cells // page_cells)
            page_cache_limit = min(page_cache_limit, max_pages_for_budget)
        page_cache_evicted_rows = self._set_page_cache_limit(page_cache_limit)

        body_start_ns = body_start_ns if remaining_height > 0 else 0
        fetched_cells = 0
        evicted_rows = page_cache_evicted_rows
        cache_status = "hit"
        viewport_fill_rows = 0
        prepend_rows = 0
        append_rows = 0
        did_concat = False
        did_rebuild_cache = False
        did_rebuild_columns = False
        rebase_window = False
        sheet_version = getattr(viewer.sheet, "cache_version", None)
        if (
            self.plan_hash != plan_hash
            or self.cols != col_key
            or self._sheet_version != sheet_version
        ):
            self._page_cache.clear()

        stream_allowed = self._should_stream()
        prefetch_dir = "none"
        prefetch_rows = 0
        stream_mode = "page_cache" if stream_allowed else "disabled"
        stream_reason = "page_cache" if stream_allowed else "disabled"
        stream_batches = 0
        stream_rows = 0
        stream_cells = 0
        first_batch_ns = 0
        window_rows = 0
        window_cells = 0
        prefetch_pages = 0

        if remaining_height > 0:
            overscan_floor = self._overscan_rows_for_tier(speed_tier, remaining_height)
            if overscan_hint is None:
                overscan_hint = overscan_floor
            elif overscan_floor > 0:
                overscan_hint = max(overscan_floor, overscan_hint)

            page_slice: TableSlice | None = None
            page_status = SliceStatus.OK
            if not use_page_cache:
                fetch_start = body_start
                fetch_count = remaining_height
                try:
                    page_slice, page_status = row_provider.get_slice(
                        plan,
                        column_list,
                        fetch_start,
                        fetch_count,
                    )
                except Exception:
                    self.invalidate()
                    raise
                fetched_cells += page_slice.height * column_count
                cache_status = "miss"
                did_rebuild_cache = True
                overall_status = self._combine_status(overall_status, page_status)
                self.table = page_slice
                self.start = fetch_start
                self.end = fetch_start + page_slice.height
                self.cols = col_key
                self.plan_hash = plan_hash
                self._sheet_version = sheet_version
                self._table_status = page_status
                if page_slice.height > 0:
                    body_slice = TableSliceView(
                        page_slice, 0, min(remaining_height, page_slice.height)
                    )
                else:
                    body_slice = TableSlice.empty(column_list, viewer.schema)
            else:
                page_start = max(0, (body_start // page_stride) * page_stride)
                page_cache_key = (plan_hash, col_key, page_start)
                page_entry = self._page_cache.get(page_cache_key)
                cache_hit = False
                page_slice_start = page_start

                if page_entry is not None:
                    page_slice = page_entry.slice
                    page_status = page_entry.status
                    cache_hit = True
                    self._page_cache.move_to_end(page_cache_key)
                else:
                    cached_page = row_provider.get_page_if_cached(
                        plan,
                        column_list,
                        page_start,
                    )
                    if cached_page is not None:
                        page_slice, page_status = cached_page
                        cache_hit = True
                    if page_slice is None:
                        reused_table = self._maybe_rebuild_columns(
                            plan,
                            column_list,
                            page_start,
                            page_size,
                        )
                        if reused_table is not None:
                            page_slice, page_status, cache_hit, fetched_count = reused_table
                            if fetched_count:
                                fetched_cells += fetched_count
                                cache_status = "miss"
                            did_rebuild_columns = True
                    if page_slice is None:
                        should_fetch = (
                            speed_tier == "slow" or not stream_allowed or self.table is None
                        )
                        if should_fetch:
                            try:
                                page_slice, page_status, cache_hit = row_provider.get_page(
                                    plan,
                                    column_list,
                                    page_start,
                                )
                            except Exception:
                                self.invalidate()
                                raise
                            if not cache_hit:
                                fetched_cells += page_slice.height * column_count
                                cache_status = "miss"
                                did_rebuild_cache = True
                        else:
                            future = None
                            with contextlib.suppress(Exception):
                                future = row_provider.prefetch_page(plan, column_list, page_start)
                            if future is not None:
                                hooks = viewer.ui_hooks

                                def _invalidate(_: object) -> None:
                                    with contextlib.suppress(Exception):
                                        hooks.invalidate()

                                with contextlib.suppress(Exception):
                                    future.add_done_callback(_invalidate)
                            cache_status = "pending"
                if page_slice is not None and cache_status != "pending":
                    self._page_cache[page_cache_key] = _PageCacheEntry(page_slice, page_status)
                    self._page_cache.move_to_end(page_cache_key)
                    while len(self._page_cache) > self._page_cache_limit:
                        _, evicted = self._page_cache.popitem(last=False)
                        evicted_rows += evicted.slice.height

                if page_slice is None:
                    if (
                        self.table is not None
                        and self.plan_hash == plan_hash
                        and self.cols == col_key
                        and self._sheet_version == sheet_version
                        and self.start <= body_start < self.end
                    ):
                        page_slice = self.table
                        page_status = self._table_status
                        cache_hit = True
                        page_slice_start = self.start
                    else:
                        page_slice = TableSlice.empty(column_list, viewer.schema)
                        page_status = SliceStatus.OK

                overall_status = self._combine_status(overall_status, page_status)
                if page_slice is not None and (
                    cache_status != "pending" or page_slice is self.table
                ):
                    self.table = page_slice
                    self.start = page_slice_start
                    self.end = page_slice_start + page_slice.height
                    self.cols = col_key
                    self.plan_hash = plan_hash
                    self._sheet_version = sheet_version
                    self._table_status = page_status

                offset = max(0, body_start - page_slice_start)
                body_length = min(remaining_height, max(0, page_slice.height - offset))
                if body_length > 0:
                    body_slice = TableSliceView(page_slice, offset, body_length)
                else:
                    body_slice = TableSlice.empty(column_list, viewer.schema)

            if use_page_cache:
                if direction:
                    prefetch_pages = self._prefetch_pages_for_tier(speed_tier)
                    if overscan_hint and overscan_hint > 0:
                        hint_pages = max(1, math.ceil(overscan_hint / page_size))
                        prefetch_pages = max(prefetch_pages, hint_pages)
                    max_prefetch = max(0, self._page_cache_limit - 1)
                    prefetch_pages = min(prefetch_pages, max_prefetch)
                if direction < 0 and prefetch_pages:
                    for idx in range(1, prefetch_pages + 1):
                        prefetch_start = max(0, page_start - page_stride * idx)
                        if prefetch_start < page_start:
                            row_provider.prefetch_page(plan, column_list, prefetch_start)
                    prefetch_dir = "backward"
                    prefetch_rows = page_size * prefetch_pages
                elif direction > 0 and prefetch_pages:
                    for idx in range(1, prefetch_pages + 1):
                        prefetch_start = page_start + page_stride * idx
                        row_provider.prefetch_page(plan, column_list, prefetch_start)
                    prefetch_dir = "forward"
                    prefetch_rows = page_size * prefetch_pages

            window_rows = self.table.height if self.table is not None else 0
            window_cells = window_rows * column_count

            first_batch_ms = first_batch_ns / 1_000_000 if first_batch_ns else 0.0
            telemetry = self._record_telemetry(
                duration_ns=max(0, monotonic_ns() - call_start_ns),
                fetched_cells=fetched_cells,
                cache_status=cache_status,
                rows_per_second=rows_per_second,
                speed_tier=speed_tier,
                prefetch_pages=prefetch_pages,
                prefetch_dir=prefetch_dir,
            )

            payload: dict[str, int | float | str] = {
                "row0": body_start,
                "height": body_slice.height,
                "viewport_shortfall": max(0, remaining_height - body_slice.height),
                "viewport_fill_rows": viewport_fill_rows,
                "cache": cache_status,
                "cache_start": self.start,
                "cache_end": self.end,
                "direction": direction,
                "direction_flip": int(direction_flip),
                "rebase": int(rebase_window),
                "prepend_rows": prepend_rows,
                "append_rows": append_rows,
                "did_concat": int(did_concat),
                "did_rebuild_cache": int(did_rebuild_cache),
                "did_rebuild_columns": int(did_rebuild_columns),
                "cols": column_count,
                "window_rows": window_rows,
                "window_cells": window_cells,
                "window_bytes": window_cells * self.APPROX_BYTES_PER_CELL,
                "fetched_rows": fetched_cells // column_count if column_count else 0,
                "fetched_cells": fetched_cells,
                "evicted_rows": evicted_rows,
                "prefetch_dir": prefetch_dir,
                "prefetch_rows": prefetch_rows,
                "stream_mode": stream_mode,
                "stream_reason": stream_reason,
                "stream_batches": stream_batches,
                "stream_rows": stream_rows,
                "stream_cells": stream_cells,
                "first_batch_ms": first_batch_ms,
                "speed_tier": speed_tier,
                "rows_per_second": rows_per_second,
                "cache_hit_rate": telemetry.cache_hit_rate,
                "bytes_copied_per_second": telemetry.bytes_copied_per_second,
                "p95_row_cache_ms": telemetry.p95_row_cache_ms,
            }

            if should_record:
                duration_ms = (monotonic_ns() - body_start_ns) / 1_000_000 if body_start_ns else 0.0
                viewer._record_perf_event("viewer.row_cache", duration_ms, payload)

            body_positions.extend(range(body_start, body_start + body_slice.height))
        else:
            # No scrollable body; still honour frozen rows.
            self.table = TableSlice.empty(column_list, viewer.schema)
            self.start = body_start
            self.end = body_start
            self.cols = col_key
            self.plan_hash = plan_hash
            self._sheet_version = sheet_version
            self._table_status = SliceStatus.OK
            self._record_telemetry(
                duration_ns=max(0, monotonic_ns() - call_start_ns),
                fetched_cells=fetched_cells,
                cache_status=cache_status,
                rows_per_second=rows_per_second,
                speed_tier=speed_tier,
                prefetch_pages=prefetch_pages,
                prefetch_dir=prefetch_dir,
            )

        self._visible_row_positions = frozen_positions + body_positions

        slices: list[TableSlice | TableSliceView] = []
        slices.extend(frozen_slices)
        if body_slice.height:
            slices.append(body_slice)

        if not slices:
            self._handle_slice_status(overall_status)
            return TableSlice.empty(column_list, viewer.schema)

        result = slices[0] if len(slices) == 1 else TableSliceComposite(slices)

        if result.row_ids is None and result.start_offset is not None:
            row_id_column = getattr(viewer.row_provider, "_row_id_column", None)
            if row_id_column:
                rescue_slice = None
                try:
                    rescue_slice, _ = row_provider.get_slice(
                        plan,
                        (row_id_column,),
                        max(0, result.start_offset or 0),
                        result.height,
                    )
                except Exception:
                    rescue_slice = None

                if rescue_slice is not None:
                    row_ids = rescue_slice.row_ids
                    if row_ids is None and row_id_column in rescue_slice.column_names:
                        try:
                            row_ids = rescue_slice.column(row_id_column).values
                        except Exception:
                            row_ids = None

                    if row_ids is not None:
                        if isinstance(result, TableSlice):
                            try:
                                result = TableSlice(
                                    result.columns,
                                    result.schema,
                                    start_offset=result.start_offset,
                                    row_ids=row_ids,
                                )
                            except ValueError:
                                with contextlib.suppress(Exception):
                                    result.row_ids = row_ids
                        else:
                            with contextlib.suppress(Exception):
                                result.row_ids = row_ids
        global _BOOT_TRACE_FIRST_VIEWPORT
        if _BOOT_TRACE_FIRST_VIEWPORT and result.height:
            _BOOT_TRACE_FIRST_VIEWPORT = False
            _boot_trace("viewer:viewport populated")
        self._handle_slice_status(overall_status)
        return result

    def _maybe_rebuild_columns(
        self,
        plan: QueryPlan | None,
        column_list: Sequence[str],
        page_start: int,
        page_size: int,
    ) -> tuple[TableSlice, SliceStatus, bool, int] | None:
        if self.table is None:
            return None
        if self.start != page_start:
            return None
        if self.end != page_start + self.table.height:
            return None
        plan_hash = self.viewer.plan_hash()
        sheet_version = getattr(self.viewer.sheet, "cache_version", None)
        if self.plan_hash != plan_hash or self._sheet_version != sheet_version:
            return None

        existing_names = {column.name for column in self.table.columns}
        missing = [name for name in column_list if name not in existing_names]
        base_status = self._table_status or SliceStatus.OK
        if not missing:
            merged = self._merge_table_columns(self.table, None, column_list)
            if merged is None:
                return None
            return merged, base_status, True, 0

        try:
            missing_slice, missing_status, cache_hit = self.viewer.row_provider.get_page(
                plan,
                missing,
                page_start,
            )
        except Exception:
            self.invalidate()
            raise
        merged = self._merge_table_columns(self.table, missing_slice, column_list)
        if merged is None:
            return None
        combined_status = self._combine_status(base_status, missing_status)
        fetched_cells = 0 if cache_hit else missing_slice.height * len(missing)
        return merged, combined_status, cache_hit, fetched_cells

    def _merge_table_columns(
        self,
        base: TableSlice,
        extra: TableSlice | None,
        column_list: Sequence[str],
    ) -> TableSlice | None:
        base_map = {column.name: column for column in base.columns}
        extra_map = {column.name: column for column in extra.columns} if extra is not None else {}
        merged_columns: list[Any] = []
        for name in column_list:
            column = base_map.get(name) or extra_map.get(name)
            if column is None:
                return None
            merged_columns.append(column)
        start_offset = base.start_offset
        if start_offset is None and extra is not None:
            start_offset = extra.start_offset
        row_ids = base.row_ids if base.row_ids is not None else (extra.row_ids if extra else None)
        try:
            return TableSlice(
                tuple(merged_columns),
                self.viewer.schema,
                start_offset=start_offset,
                row_ids=row_ids,
            )
        except ValueError:
            return None

    @staticmethod
    def _combine_status(left: SliceStatus, right: SliceStatus) -> SliceStatus:
        if right is SliceStatus.SCHEMA_MISMATCH:
            return SliceStatus.SCHEMA_MISMATCH
        if right is SliceStatus.PARTIAL and left is SliceStatus.OK:
            return SliceStatus.PARTIAL
        return left

    def _handle_slice_status(self, status: SliceStatus) -> None:
        if status is SliceStatus.OK:
            self._last_warning_status = SliceStatus.OK
            return
        if status is self._last_warning_status:
            return

        viewer = self.viewer
        if viewer.status_message:
            self._last_warning_status = status
            return

        if status is SliceStatus.SCHEMA_MISMATCH:
            message = "slice schema mismatch — check column names"
        else:
            message = "some requested columns are missing"
        viewer.status_message = message
        viewer.mark_status_dirty()
        self._last_warning_status = status


class ColumnWidthController:
    """Handle column width calculations and width modes."""

    WIDTH_SAMPLE_MAX_ROWS = 10_000
    WIDTH_SAMPLE_BATCH_ROWS = 1_000
    WIDTH_SAMPLE_BUDGET_NS = 100_000_000  # 100ms
    WIDTH_TARGET_PERCENTILE = 0.99
    WIDTH_PADDING = 2

    def __init__(
        self,
        viewer: Viewer,
        *,
        sample_max_rows: int | None = None,
        sample_batch_rows: int | None = None,
        sample_budget_ns: int | None = None,
        target_percentile: float | None = None,
        padding: int | None = None,
    ) -> None:
        self.viewer = viewer
        self._sample_max_rows = (
            sample_max_rows
            if isinstance(sample_max_rows, int) and sample_max_rows > 0
            else self.WIDTH_SAMPLE_MAX_ROWS
        )
        self._sample_batch_rows = (
            sample_batch_rows
            if isinstance(sample_batch_rows, int) and sample_batch_rows > 0
            else self.WIDTH_SAMPLE_BATCH_ROWS
        )
        self._sample_budget_ns = (
            sample_budget_ns
            if isinstance(sample_budget_ns, int) and sample_budget_ns > 0
            else self.WIDTH_SAMPLE_BUDGET_NS
        )
        self._target_percentile = (
            target_percentile
            if isinstance(target_percentile, float) and 0.0 <= target_percentile <= 1.0
            else self.WIDTH_TARGET_PERCENTILE
        )
        self._padding = padding if isinstance(padding, int) and padding >= 0 else self.WIDTH_PADDING

    def content_width_for_column(
        self,
        col_idx: int,
        *,
        sampled_lengths: dict[int, list[int]] | None = None,
    ) -> int:
        viewer = self.viewer
        if col_idx < 0 or col_idx >= len(viewer.columns):
            return viewer._min_col_width

        col_name = viewer.columns[col_idx]
        header_width = len(col_name) + self._padding

        samples = sampled_lengths or {}
        lengths = samples.get(col_idx)
        if lengths is None:
            lengths = self._sample_column_lengths((col_idx,)).get(col_idx, [])

        target_length = self._percentile_length(lengths) if lengths else 0
        content_width = target_length + self._padding

        width = max(header_width, content_width)
        width = self._clamp_width(width)
        return width

    def _clamp_width(self, width: int) -> int:
        viewer = self.viewer
        max_viewport = max(viewer._min_col_width, viewer.view_width_chars - 1)
        return max(viewer._min_col_width, min(width, max_viewport))

    def _percentile_length(self, lengths: Sequence[int]) -> int:
        if not lengths:
            return 0
        ordered = sorted(lengths)
        if len(ordered) == 1:
            return ordered[0]
        idx = math.ceil((len(ordered) - 1) * self._target_percentile)
        idx = max(0, min(idx, len(ordered) - 1))
        return ordered[idx]

    def _coerce_display(self, raw_value: Any, rendered: str) -> str:
        if raw_value is None or rendered == "":
            return "null"
        if isinstance(raw_value, float) and (math.isnan(raw_value) or math.isinf(raw_value)):
            if math.isnan(raw_value):
                return "NaN"
            return "inf" if raw_value > 0 else "-inf"
        return rendered

    def _fallback_display(self, value: Any) -> str:
        if value is None:
            return "null"
        if _is_float_like(value):
            try:
                as_float = float(value)
            except Exception:
                return str(value)
            if math.isnan(as_float):
                return "NaN"
            if math.isinf(as_float):
                return "inf" if as_float > 0 else "-inf"
            return _format_float_two_decimals(as_float)
        return str(value)

    def _measure_column_lengths(
        self,
        column: Any,
        limit: int,
        budget_exceeded: Callable[[], bool],
    ) -> list[int]:
        if limit <= 0:
            return []

        lengths: list[int] = []
        try:
            formatted_values = column.formatted(0)
        except Exception:
            formatted_values = None

        if formatted_values:
            for raw_value, rendered in zip(column.values, formatted_values, strict=False):
                if len(lengths) >= limit or budget_exceeded():
                    break
                display = self._coerce_display(raw_value, rendered)
                lengths.append(len(display))
        else:
            for raw_value in column.values:
                if len(lengths) >= limit or budget_exceeded():
                    break
                lengths.append(len(self._fallback_display(raw_value)))
        return lengths

    def _sample_column_lengths(self, column_indices: Sequence[int]) -> dict[int, list[int]]:
        viewer = self.viewer
        if not column_indices:
            return {}

        valid_indices = [idx for idx in column_indices if 0 <= idx < len(viewer.columns)]
        if not valid_indices:
            return {}

        names = {idx: viewer.columns[idx] for idx in valid_indices}
        lengths: dict[int, list[int]] = {idx: [] for idx in valid_indices}

        total_rows_hint = getattr(viewer, "_total_rows", None)
        max_rows = self._sample_max_rows
        if isinstance(total_rows_hint, int) and total_rows_hint > 0:
            max_rows = min(max_rows, total_rows_hint)

        start_ns = monotonic_ns()

        def budget_exceeded() -> bool:
            return monotonic_ns() - start_ns >= self._sample_budget_ns

        def measure(table_slice: Any) -> None:
            if table_slice is None or getattr(table_slice, "height", 0) <= 0:
                return
            for idx, name in names.items():
                if len(lengths[idx]) >= max_rows:
                    continue
                if name not in table_slice.column_names:
                    continue
                column = table_slice.column(name)
                remaining = max_rows - len(lengths[idx])
                samples = self._measure_column_lengths(column, remaining, budget_exceeded)
                if samples:
                    lengths[idx].extend(samples)
                if budget_exceeded():
                    return

        measure(getattr(viewer._row_cache, "table", None))

        next_offset = 0
        batch_rows = self._sample_batch_rows
        column_names = list(names.values())

        while not budget_exceeded():
            remaining_targets = [
                max_rows - len(lengths[idx])
                for idx in valid_indices
                if len(lengths[idx]) < max_rows
            ]
            if not remaining_targets:
                break

            rows_to_fetch = min(batch_rows, max(remaining_targets))
            try:
                sample_slice = viewer.sheet.fetch_slice(next_offset, rows_to_fetch, column_names)
            except Exception:
                break

            measure(sample_slice)

            consumed = getattr(sample_slice, "height", 0)
            if consumed <= 0:
                break
            next_offset += consumed
            if consumed < rows_to_fetch:
                break
            if (
                isinstance(total_rows_hint, int)
                and total_rows_hint > 0
                and next_offset >= total_rows_hint
            ):
                break

        return lengths

    def compute_initial_widths(self) -> list[int]:
        """Compute initial column widths based on header and sample data."""
        viewer = self.viewer
        if not viewer.columns:
            return []

        # Fetch one sample slice for all columns to avoid repeated cold scans.
        sample_rows = min(100, viewer._total_rows if viewer._total_rows else 50)
        sample_slice = None
        try:
            sample_slice = viewer.sheet.fetch_slice(0, sample_rows, viewer.columns)
        except Exception:
            sample_slice = None

        widths = []
        for col_name in viewer.columns:
            # Start with header width
            header_width = len(col_name) + 2  # +2 for padding

            # Sample data to estimate content width.
            if sample_slice is not None:
                try:
                    if col_name in sample_slice.column_names and sample_slice.height > 0:
                        column = sample_slice.column(col_name)
                        header_width = self._compute_sampled_width(
                            column,
                            header_width,
                            viewer._default_col_width_cap,
                        )
                except Exception:
                    pass
            else:
                try:
                    fallback_slice = viewer.sheet.fetch_slice(0, sample_rows, [col_name])
                    if col_name in fallback_slice.column_names and fallback_slice.height > 0:
                        column = fallback_slice.column(col_name)
                        header_width = self._compute_sampled_width(
                            column,
                            header_width,
                            viewer._default_col_width_cap,
                        )
                except Exception:
                    # If sampling fails, fall back to header width.
                    pass

            # Ensure minimum width
            final_width = max(viewer._min_col_width, header_width)
            widths.append(final_width)

        return widths

    def _compute_sampled_width(self, column: Any, header_width: int, width_cap: int) -> int:
        try:
            formatted_values = column.formatted(0)
        except Exception:
            formatted_values = None

        if formatted_values:
            max_display = header_width
            for raw_value, rendered in zip(column.values, formatted_values, strict=False):
                if raw_value is None or rendered == "":
                    display = "null"
                elif isinstance(raw_value, float) and (
                    math.isnan(raw_value) or math.isinf(raw_value)
                ):
                    display = "NaN" if math.isnan(raw_value) else "inf" if raw_value > 0 else "-inf"
                else:
                    display = rendered
                max_display = max(max_display, len(display) + 2)
            return max(header_width, min(max_display, width_cap))

        lengths = [len(str(value)) for value in column.values if value is not None]
        if lengths:
            content_width = min(max(lengths) + 2, width_cap)
            return max(header_width, content_width)
        return header_width

    def invalidate_cache(self) -> None:
        viewer = self.viewer
        viewer._width_cache_all = None
        viewer._width_cache_single.clear()

    def ensure_default_widths(self) -> None:
        viewer = self.viewer
        if len(viewer._default_header_widths) == len(viewer.columns):
            return

        viewer._header_widths = self.compute_initial_widths()
        viewer._default_header_widths = list(viewer._header_widths)
        self.invalidate_cache()

    def normalize_mode(self) -> None:
        viewer = self.viewer
        if not viewer.columns:
            viewer._width_mode = "default"
            viewer._width_target = None
            return

        if viewer._width_mode == "single":
            if viewer._width_target is None or not (
                0 <= viewer._width_target < len(viewer.columns)
            ):
                viewer._width_mode = "default"
                viewer._width_target = None
        elif viewer._width_mode == "all":
            viewer._width_target = None
        else:
            viewer._width_mode = "default"
            viewer._width_target = None

    def apply_width_mode(self) -> None:
        viewer = self.viewer
        self.ensure_default_widths()
        self.normalize_mode()

        if viewer._width_mode == "all":
            cache = viewer._width_cache_all
            if cache is None or len(cache) != len(viewer.columns):
                samples = self._sample_column_lengths(range(len(viewer.columns)))
                cache = [
                    self.content_width_for_column(idx, sampled_lengths=samples)
                    for idx in range(len(viewer.columns))
                ]
                viewer._width_cache_all = list(cache)
            viewer._header_widths = [self._clamp_width(width) for width in cache]
            viewer._width_cache_all = list(viewer._header_widths)
            viewer._width_cache_single.clear()
        elif viewer._width_mode == "single" and viewer._width_target is not None:
            target = viewer._width_target
            base_widths = list(viewer._default_header_widths)
            if 0 <= target < len(viewer.columns):
                width = viewer._width_cache_single.get(target)
                if width is None:
                    samples = self._sample_column_lengths((target,))
                    width = self.content_width_for_column(target, sampled_lengths=samples)
                width = self._clamp_width(width)
                viewer._width_cache_single[target] = width
                base_widths[target] = width
                viewer._header_widths = base_widths
            else:
                viewer._width_mode = "default"
                viewer._width_target = None
                viewer._header_widths = list(viewer._default_header_widths)
        else:
            viewer._header_widths = list(viewer._default_header_widths)
            if viewer._width_mode == "default":
                viewer._width_cache_single.clear()

        viewer._visible_key = None

    def autosize_visible_columns(self, column_indices: list[int]) -> None:
        viewer = self.viewer
        if not column_indices:
            viewer._autosized_widths.clear()
            return

        available_inner = max(1, viewer.view_width_chars - (len(column_indices) + 1))

        base_widths = [viewer._header_widths[idx] for idx in column_indices]
        base_total = sum(base_widths)

        compact_default = (
            getattr(viewer, "_compact_width_layout", False) and viewer._width_mode == "default"
        )
        if compact_default:
            capped_widths = [min(width, viewer._default_col_width_cap) for width in base_widths]
            viewer._autosized_widths = dict(zip(column_indices, capped_widths, strict=False))
            return

        if base_total >= available_inner:
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        frozen_set = viewer._freeze.column_index_set()
        dynamic_positions = [pos for pos, idx in enumerate(column_indices) if idx not in frozen_set]

        slack = available_inner - base_total

        if not dynamic_positions:
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        if viewer._width_mode == "single" and viewer._width_target is not None:
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        if viewer._width_mode != "default":
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        rooms: list[int] = []
        total_room = 0
        for pos in dynamic_positions:
            base = base_widths[pos]
            target = viewer._default_col_width_cap
            room = max(0, target - base)
            rooms.append(room)
            total_room += room

        new_widths = list(base_widths)

        if total_room <= 0:
            share, remainder = divmod(slack, len(dynamic_positions))
            if share:
                for pos in dynamic_positions:
                    new_widths[pos] += share
            if remainder:
                for offset in range(remainder):
                    pos = dynamic_positions[-(offset + 1)]
                    new_widths[pos] += 1
        else:
            allocations = [0] * len(dynamic_positions)
            for i, room in enumerate(rooms):
                if room == 0:
                    continue
                provisional = (slack * room) // total_room
                allocations[i] = min(room, provisional)

            allocated = sum(allocations)
            remaining = slack - allocated

            if remaining > 0:
                residual = [room - allocations[i] for i, room in enumerate(rooms)]
                while remaining > 0 and any(r > 0 for r in residual):
                    for i, rem in enumerate(residual):
                        if remaining == 0:
                            break
                        if rem > 0:
                            allocations[i] += 1
                            residual[i] -= 1
                            remaining -= 1
                    else:
                        break

            if remaining > 0:
                allocations[-1] += remaining

            for pos, alloc in zip(dynamic_positions, allocations, strict=False):
                new_widths[pos] += alloc

        current_total = sum(new_widths)
        if current_total < available_inner and new_widths:
            target_pos = dynamic_positions[-1] if dynamic_positions else len(new_widths) - 1
            new_widths[target_pos] += available_inner - current_total

        viewer._autosized_widths = dict(zip(column_indices, new_widths, strict=False))

    def force_default_mode(self) -> None:
        viewer = self.viewer
        viewer._width_mode = "default"
        viewer._width_target = None
        self.invalidate_cache()
        self.apply_width_mode()
        viewer._autosized_widths.clear()

    def toggle_maximize_current_col(self) -> None:
        viewer = self.viewer
        if not viewer.columns:
            viewer.status_message = "no columns"
            return

        target = max(0, min(viewer.cur_col, len(viewer.columns) - 1))

        current_width = viewer._header_widths[target]
        desired_width = viewer._width_cache_single.get(target)
        if desired_width is None:
            desired_width = viewer._compute_content_width(target)
            viewer._width_cache_single[target] = desired_width

        if viewer._width_mode == "single" and viewer._width_target == target:
            viewer._width_mode = "default"
            viewer._width_target = None
            viewer.status_message = "width reset"
        else:
            if viewer._width_mode == "default" and desired_width <= current_width:
                viewer.status_message = f"'{viewer.columns[target]}' already at max width"
                viewer._visible_key = None
                viewer._autosized_widths.clear()
                viewer.clamp()
                return
            viewer._width_mode = "single"
            viewer._width_target = target
            viewer._width_cache_all = None
            viewer.status_message = f"maximize column '{viewer.columns[target]}'"

        self.apply_width_mode()

        if viewer._width_mode == "single":
            maximised_col_name = viewer.columns[target]
            if maximised_col_name not in viewer.visible_cols:
                viewer.col0 = target
                viewer._visible_key = None

        viewer.clamp()

    def toggle_maximize_all_cols(self) -> None:
        viewer = self.viewer
        if not viewer.columns:
            viewer.status_message = "no columns"
            return
        if viewer._width_mode == "all":
            viewer._width_mode = "default"
            viewer.status_message = "widths reset"
        else:
            viewer._width_mode = "all"
            viewer._width_target = None
            viewer._width_cache_all = None
            viewer._width_cache_single.clear()
            viewer.col0 = viewer.cur_col
            viewer.status_message = "maximize all columns"

        self.apply_width_mode()
        if viewer._width_mode != "default":
            viewer._autosized_widths.clear()
        viewer.clamp()
