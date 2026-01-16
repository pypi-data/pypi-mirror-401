"""Row slice provider that bridges viewer requests to engine adapters."""

from __future__ import annotations

import logging
from collections import OrderedDict
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import Future
from threading import RLock
from typing import TYPE_CHECKING, Any, cast

import polars as pl

from ..config.settings import CACHE_DEFAULTS, STREAMING_DEFAULTS
from .column_insight import CellPreview, summarize_value_preview
from .engine.contracts import TableColumn, TableSlice
from .engine.polars_adapter import table_slice_from_dataframe
from .errors import CompileError, MaterializeError, PulkaCoreError
from .interfaces import (
    EngineAdapterProtocol,
    JobRunnerProtocol,
    MaterializerProtocol,
    is_materializer_compatible,
)
from .jobs import JobRequest, JobResult
from .plan import QueryPlan, normalized_columns_key
from .row_provider_cache import RowCacheManager
from .row_provider_parquet import ParquetRowGroupIndexer
from .row_provider_sidecar import SidecarWindow, SidecarWindowManager
from .row_provider_streaming import RowStreamingPipeline
from .row_provider_types import (
    PlanContext,
    RowKey,
    SliceStatus,
    SliceStreamRequest,
    TableSliceChunk,
)
from .sheet import SHEET_FEATURE_SLICE, sheet_supports
from .strategy import Strategy, compile_strategy

LOGGER = logging.getLogger(__name__)


if TYPE_CHECKING:
    from .source_traits import SourceTraits


class RowProvider:
    """Serve row slices for a sheet, optionally prefetching upcoming ranges."""

    __slots__ = (
        "_engine_factory",
        "_columns_getter",
        "_fetcher",
        "_job_context",
        "_runner",
        "_lock",
        "_materializer",
        "_empty_result_factory",
        "_empty_template",
        "_cache",
        "_max_cache_cells",
        "_max_cache_entries",
        "_max_page_cache_cells",
        "_max_page_cache_entries",
        "_streaming_enabled",
        "_streaming_batch_rows",
        "_streaming_last_chunks",
        "_streaming_last_rows",
        "_streaming_last_cells",
        "_streaming_last_duration_ns",
        "_streaming_last_mode",
        "_source_traits_cache",
        "_strategy",
        "_strategy_cache",
        "_streaming_enabled_configured",
        "_streaming_batch_rows_configured",
        "_sidecar",
        "_page_size",
        "_row_id_column",
        "_parquet_indexer",
        "_streaming",
    )

    MAX_CACHE_CELLS = CACHE_DEFAULTS.row_provider_max_cells
    MAX_CACHE_ENTRIES = CACHE_DEFAULTS.row_provider_max_entries
    PAGE_SIZE = CACHE_DEFAULTS.row_provider_page_size
    STREAMING_ENABLED = STREAMING_DEFAULTS.enabled
    STREAMING_BATCH_ROWS = STREAMING_DEFAULTS.batch_rows
    SOURCE_TRAITS_CACHE_LIMIT = 8
    STRATEGY_CACHE_LIMIT = SOURCE_TRAITS_CACHE_LIMIT

    _max_cache_cells: int
    _max_cache_entries: int
    _max_page_cache_cells: int
    _max_page_cache_entries: int

    _LIMIT_ATTRS = {
        "_max_cache_cells",
        "_max_cache_entries",
        "_max_page_cache_cells",
        "_max_page_cache_entries",
    }

    def __init__(
        self,
        *,
        engine_factory: Callable[[], EngineAdapterProtocol] | None = None,
        columns_getter: Callable[[], Sequence[str]] | None = None,
        materializer: MaterializerProtocol | None = None,
        fetcher: Callable[[int, int, Sequence[str]], Any] | None = None,
        job_context: Callable[[], tuple[str, int, str]] | None = None,
        empty_result_factory: Callable[[], Any] | None = None,
        runner: JobRunnerProtocol,
        streaming_enabled: bool | None = None,
        streaming_batch_rows: int | None = None,
        row_id_column: str | None = None,
    ) -> None:
        if engine_factory is None:
            if fetcher is None:
                msg = "RowProvider requires either engine_factory or fetcher"
                raise ValueError(msg)
            self._fetcher: Callable[[int, int, Sequence[str]], Any] | None = fetcher
            self._engine_factory = None
            self._columns_getter = None
            self._materializer = None
        else:
            if columns_getter is None:
                msg = "columns_getter is required when engine_factory is provided"
                raise ValueError(msg)
            if materializer is None:
                msg = "materializer is required when engine_factory is provided"
                raise ValueError(msg)
            if not is_materializer_compatible(materializer):
                msg = "materializer must implement MaterializerProtocol"
                raise TypeError(msg)
            self._engine_factory = engine_factory
            self._columns_getter = columns_getter
            self._materializer = materializer
            self._fetcher = None

        if empty_result_factory is None:
            msg = "RowProvider requires an empty_result_factory"
            raise ValueError(msg)

        self._empty_result_factory = empty_result_factory
        self._job_context = job_context
        if runner is None:
            msg = "RowProvider requires a JobRunner instance"
            raise ValueError(msg)
        if not isinstance(runner, JobRunnerProtocol):
            msg = "runner must implement JobRunnerProtocol"
            raise TypeError(msg)
        self._runner = runner
        self._empty_template: TableSlice | None = None
        self._streaming_enabled_configured = streaming_enabled is not None
        self._streaming_enabled = (
            self.STREAMING_ENABLED if streaming_enabled is None else bool(streaming_enabled)
        )
        batch_default = self.STREAMING_BATCH_ROWS
        self._streaming_batch_rows_configured = (
            streaming_batch_rows is not None and streaming_batch_rows > 0
        )
        if streaming_batch_rows is not None and streaming_batch_rows > 0:
            batch_default = int(streaming_batch_rows)
        self._streaming_batch_rows = max(1, batch_default)
        self._streaming_last_chunks = 0
        self._streaming_last_rows = 0
        self._streaming_last_cells = 0
        self._streaming_last_duration_ns = 0
        self._streaming_last_mode = "init"
        self._lock = RLock()
        self._page_size = max(1, self.PAGE_SIZE)
        self._row_id_column = row_id_column
        object.__setattr__(self, "_max_cache_cells", self.MAX_CACHE_CELLS)
        object.__setattr__(self, "_max_cache_entries", self.MAX_CACHE_ENTRIES)
        object.__setattr__(self, "_max_page_cache_cells", self.MAX_CACHE_CELLS)
        object.__setattr__(self, "_max_page_cache_entries", self.MAX_CACHE_ENTRIES)
        self._cache = RowCacheManager(
            lock=self._lock,
            cell_counter=self._cell_count,
            max_cache_cells=self._max_cache_cells,
            max_cache_entries=self._max_cache_entries,
            max_page_cache_cells=self._max_page_cache_cells,
            max_page_cache_entries=self._max_page_cache_entries,
        )
        self._source_traits_cache: OrderedDict[str, SourceTraits] = OrderedDict()
        self._strategy: Strategy | None = None
        self._strategy_cache: OrderedDict[str, Strategy] = OrderedDict()
        self._sidecar = SidecarWindowManager(
            lock=self._lock,
            runner=self._runner,
            traits_getter=self.get_source_traits,
        )
        self._parquet_indexer = ParquetRowGroupIndexer(lock=self._lock)
        self._streaming = RowStreamingPipeline(self)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._LIMIT_ATTRS:
            object.__setattr__(self, name, value)
            cache = getattr(self, "_cache", None)
            if cache is not None:
                cache.update_limits(
                    max_cache_cells=self._max_cache_cells,
                    max_cache_entries=self._max_cache_entries,
                    max_page_cache_cells=self._max_page_cache_cells,
                    max_page_cache_entries=self._max_page_cache_entries,
                )
            return
        super().__setattr__(name, value)

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    @classmethod
    def for_sheet(cls, sheet: Any, *, runner: JobRunnerProtocol) -> RowProvider:
        """Build a provider for ``sheet`` by introspecting available hooks."""

        config_factory = getattr(sheet, "row_provider_config", None)
        if callable(config_factory):
            config = dict(config_factory())
            return cls(runner=runner, **config)

        if sheet_supports(sheet, SHEET_FEATURE_SLICE):

            def fetcher(start: int, count: int, cols: Sequence[str]) -> Any:
                return sheet.fetch_slice(start, count, list(cols))

            def empty_result() -> Any:
                base_columns = list(getattr(sheet, "columns", []))
                try:
                    return sheet.fetch_slice(0, 0, base_columns)
                except Exception:
                    return sheet.fetch_slice(0, 0, [])

            job_ctx = getattr(sheet, "job_context", None)
            return cls(
                fetcher=fetcher,
                job_context=job_ctx,
                runner=runner,
                empty_result_factory=empty_result,
            )

        msg = "Sheet does not expose a supported row interface"
        raise TypeError(msg)

    @classmethod
    def for_plan_source(
        cls,
        *,
        engine_factory: Callable[[], EngineAdapterProtocol],
        columns_getter: Callable[[], Sequence[str]],
        job_context: Callable[[], tuple[str, int, str]] | None,
        materializer: MaterializerProtocol,
        empty_result_factory: Callable[[], Any],
        runner: JobRunnerProtocol,
        row_id_column: str | None = None,
    ) -> RowProvider:
        return cls(
            engine_factory=engine_factory,
            columns_getter=columns_getter,
            job_context=job_context,
            materializer=materializer,
            empty_result_factory=empty_result_factory,
            runner=runner,
            row_id_column=row_id_column,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def page_size(self) -> int:
        return self._page_size

    def current_strategy(self) -> Strategy | None:
        """Return the active access strategy, if available."""

        return self._strategy

    def get_page_if_cached(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
    ) -> tuple[TableSlice, SliceStatus] | None:
        """Return a cached page slice without triggering a fetch."""

        columns = tuple(columns)
        if start < 0:
            start = 0

        context = self._resolve_context(plan, columns)
        if context is None:
            empty = self._empty_slice(columns)
            return empty, SliceStatus.SCHEMA_MISMATCH

        count = self._page_size
        key = self._cache_key(context.plan_hash, start, count, context.fetch_columns)
        cached = self._cache.get_page_cache(key)
        if cached is None:
            return None

        slice_, status = self._finalize_slice(context, cached)
        return slice_, status

    def get_page(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
    ) -> tuple[TableSlice, SliceStatus, bool]:
        """Return a fixed-size page starting at ``start``."""

        columns = tuple(columns)
        if start < 0:
            start = 0

        context = self._resolve_context(plan, columns)
        if context is None:
            empty = self._empty_slice(columns)
            return empty, SliceStatus.SCHEMA_MISMATCH, False

        count = self._page_size
        key = self._cache_key(context.plan_hash, start, count, context.fetch_columns)
        cache_hit = False
        cached = self._cache.get_page_cache(key)
        if cached is not None:
            cache_hit = True
        if cached is not None:
            slice_, status = self._finalize_slice(context, cached)
            return slice_, status, cache_hit

        if not context.fetch_columns:
            raw_slice, _ = self._fetch_slice(context, start, count)
            slice_, status = self._finalize_slice(context, raw_slice)
            self._cache.store_page_cache(key, raw_slice)
            return slice_, status, cache_hit

        self._ensure_strategy_for_context(context)
        raw_slice, _ = self._fetch_slice(context, start, count)
        self._cache.store_page_cache(key, raw_slice)
        slice_, status = self._finalize_slice(context, raw_slice)
        return slice_, status, cache_hit

    def get_slice(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
    ) -> tuple[TableSlice, SliceStatus]:
        """Return ``count`` rows starting from ``start`` for ``columns``."""

        columns = tuple(columns)

        if count <= 0:
            empty = self._empty_slice(columns)
            status = SliceStatus.PARTIAL if columns else SliceStatus.OK
            return empty, status

        context = self._resolve_context(plan, columns)
        if context is None:
            empty = self._empty_slice(columns)
            return empty, SliceStatus.SCHEMA_MISMATCH

        if self._fetcher is None and context.fetch_columns:
            self.prepare_sidecar_window(context, start, count, record_progress=True)

        page_size = self._page_size
        page_start = max(0, (start // page_size) * page_size)
        end_row = max(start, start + count - 1)
        last_page_start = max(0, (end_row // page_size) * page_size)

        slices: list[TableSlice] = []
        status = SliceStatus.OK
        remaining = count
        cursor = start
        for page_offset in range(page_start, last_page_start + page_size, page_size):
            page_slice, page_status, _cache_hit = self.get_page(plan, columns, page_offset)
            status = self._merge_status(status, page_status)
            if page_slice.height <= 0:
                if remaining <= 0:
                    break
                cursor = max(cursor, page_offset + page_size)
                continue
            local_start = max(0, cursor - page_offset)
            local_len = min(remaining, max(0, page_slice.height - local_start))
            if local_len <= 0:
                cursor = max(cursor, page_offset + page_size)
                continue
            slices.append(page_slice.slice(local_start, local_len))
            cursor += local_len
            remaining -= local_len
            if remaining <= 0:
                break

        if not slices:
            empty = self._empty_slice(columns)
            return empty, status

        result = slices[0]
        for additional in slices[1:]:
            result = result.concat_vertical(additional)
        return result, status

    def iter_slice_stream(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int | None,
        *,
        batch_rows: int | None = None,
    ) -> Iterator[TableSlice]:
        """Yield slices for ``[start, start + count)`` without assembling a composite."""

        columns = tuple(columns)

        if count is not None and count <= 0:
            return

        if start < 0:
            start = 0

        context = self._resolve_context(plan, columns)
        if context is None:
            yield self._empty_slice(columns)
            return

        if self._fetcher is not None:
            if count is None:
                chunk = self._page_size
                cursor = start
                while True:
                    slice_, _status = self.get_slice(plan, columns, cursor, chunk)
                    if slice_.height <= 0:
                        break
                    yield slice_
                    cursor = (
                        slice_.start_offset + slice_.height
                        if slice_.start_offset is not None
                        else cursor + slice_.height
                    )
                return
            slice_, _status = self.get_slice(plan, columns, start, count)
            yield slice_
            return

        prepared = self._prepare_materializer(context.plan)
        if prepared is None:
            yield self._empty_slice(columns)
            return

        materializer, physical_plan = prepared
        self._record_source_traits(context.plan, physical_plan)

        stream_attr = getattr(materializer, "collect_slice_stream", None)
        stream_iterator: Iterator[TableSlice] | None = None
        stream_kwargs: dict[str, object] = {"start": start, "columns": tuple(context.fetch_columns)}
        if count is not None:
            stream_kwargs["length"] = count
        if callable(stream_attr):
            if batch_rows is not None and batch_rows > 0:
                stream_kwargs["batch_rows"] = batch_rows
            try:
                stream_iterator = iter(stream_attr(physical_plan, **stream_kwargs))
            except TypeError:
                stream_kwargs.pop("batch_rows", None)
                try:
                    stream_iterator = iter(stream_attr(physical_plan, **stream_kwargs))
                except Exception:
                    stream_iterator = None
            except Exception:
                stream_iterator = None

        if stream_iterator is None:
            if count is None:
                chunk = self._page_size
                cursor = start
                while True:
                    slice_, _status = self.get_slice(plan, columns, cursor, chunk)
                    if slice_.height <= 0:
                        break
                    yield slice_
                    cursor = (
                        slice_.start_offset + slice_.height
                        if slice_.start_offset is not None
                        else cursor + slice_.height
                    )
                return
            slice_, _status = self.get_slice(plan, columns, start, count)
            yield slice_
            return

        total_rows = 0
        try:
            for raw_chunk in stream_iterator:
                chunk_slice = self._coerce_slice(raw_chunk, row_id_column=self._row_id_column)
                if chunk_slice.height <= 0:
                    continue
                remaining = None if count is None else max(0, count - total_rows)
                if remaining is not None and remaining <= 0:
                    break
                if remaining is not None and chunk_slice.height > remaining:
                    chunk_slice = chunk_slice.slice(0, remaining)
                if chunk_slice.height <= 0:
                    continue
                chunk_offset = start + total_rows
                total_rows += chunk_slice.height
                if chunk_slice.start_offset is None:
                    chunk_slice = TableSlice(
                        tuple(chunk_slice.columns),
                        chunk_slice.schema,
                        start_offset=chunk_offset,
                        row_ids=chunk_slice.row_ids,
                    )
                yield chunk_slice
                if count is not None and total_rows >= count:
                    break
        except Exception as exc:  # pragma: no cover - defensive
            msg = "Failed to stream row slices"
            raise MaterializeError(msg) from exc

    def prime_page_cache(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        raw_slice: TableSlice,
    ) -> None:
        """Seed the internal page cache with full pages covered by ``raw_slice``.

        This is a best-effort optimization used by navigation commands that
        already streamed through the target area and want the subsequent render
        to hit the row cache rather than triggering a cold seek.
        """

        if raw_slice.height <= 0:
            return
        if raw_slice.start_offset is None:
            return

        context = self._resolve_context(plan, tuple(columns))
        if context is None or not context.fetch_columns:
            return

        page_size = self._page_size
        slice_start = raw_slice.start_offset
        slice_end = slice_start + raw_slice.height
        first_full_page = ((slice_start + page_size - 1) // page_size) * page_size
        last_full_page = (slice_end // page_size) * page_size
        if first_full_page >= last_full_page:
            return

        for page_start in range(first_full_page, last_full_page, page_size):
            local_start = page_start - slice_start
            if local_start < 0:
                continue
            page_slice = raw_slice.slice(local_start, page_size)
            if page_slice.height != page_size:
                continue
            if page_slice.start_offset is None:
                page_slice = TableSlice(
                    tuple(page_slice.columns),
                    page_slice.schema,
                    start_offset=page_start,
                    row_ids=page_slice.row_ids,
                )
            key = self._cache_key(context.plan_hash, page_start, page_size, context.fetch_columns)
            self._cache.store_page_cache(key, page_slice)

    def get_slice_stream(self, request: SliceStreamRequest) -> Iterator[TableSliceChunk]:
        """Yield streaming chunks that resolve to the requested slice."""

        yield from self._streaming.get_slice_stream(request)

    def build_plan_compiler(self) -> EngineAdapterProtocol | None:
        """Return an engine adapter for validation when exposed by the sheet."""

        return self._engine_adapter()

    def prefetch(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
    ) -> None:
        """Warm ``[start, start + count)`` in the background when possible."""

        if count <= 0:
            return

        if self._fetcher is not None:
            # Nothing clever to do for passthrough providers.
            return

        columns = tuple(columns)
        context = self._resolve_context(plan, columns)
        if context is None or not context.fetch_columns:
            return

        if context.sheet_id is None or context.generation is None:
            return

        page_size = self._page_size
        start_page = max(0, (start // page_size) * page_size)
        end_row = max(start, start + count - 1)
        end_page = max(0, (end_row // page_size) * page_size)
        for page_start in range(start_page, end_page + page_size, page_size):
            self.prefetch_page(plan, columns, page_start)

    def prefetch_page(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
    ) -> Future[JobResult] | None:
        """Warm a single page starting at ``start`` in the background."""

        if start < 0:
            return None

        if self._fetcher is not None:
            return None

        columns = tuple(columns)
        context = self._resolve_context(plan, columns)
        if context is None or not context.fetch_columns:
            return None

        if context.sheet_id is None or context.generation is None:
            return None

        count = self._page_size
        key = self._cache_key(context.plan_hash, start, count, context.fetch_columns)
        scheduled = self._cache.reserve_page_prefetch(key)
        if not scheduled:
            return None

        tag_hash = context.plan_hash or "none"
        cols_sig = normalized_columns_key(context.fetch_columns)
        job_tag = f"rows:{tag_hash}:{start}:{count}:{cols_sig}"

        def _job(_: int) -> Any:
            slice_result, _prefetch_window = self._fetch_slice(
                context,
                start,
                count,
                record_progress=False,
            )
            return slice_result

        req = JobRequest(
            sheet_id=context.sheet_id,
            generation=context.generation,
            tag=job_tag,
            fn=_job,
            cache_result=False,
        )
        future = self._runner.enqueue(req)
        self._cache.register_prefetch_future(key, future)
        scheduled_count = self._cache.cache_metrics().get("prefetch_scheduled", 0)
        if scheduled and LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.prefetch_schedule",
                extra={
                    "event": "row_prefetch_schedule",
                    "plan_hash": context.plan_hash,
                    "start": start,
                    "count": count,
                    "columns": cols_sig,
                    "scheduled": scheduled_count,
                },
            )

        def _store_result(fut: Any, *, row_key: RowKey = key) -> None:
            self._cache.clear_pending(row_key)

            try:
                result = fut.result()
            except Exception:
                return

            if getattr(result, "error", None) is not None:
                return

            value = getattr(result, "value", None)
            generation = getattr(result, "generation", None)
            if generation != context.generation:
                return

            if value is None:
                return

            self._cache.store_page_cache(row_key, value, prefetched=True)

        future.add_done_callback(_store_result)
        return future

    def current_cell_value(
        self,
        plan: QueryPlan | None,
        column: str,
        row: int,
        *,
        preview_chars: int = 160,
    ) -> CellPreview | None:
        """Return a lightweight preview for ``column`` at ``row``."""

        if row < 0:
            return None

        slice_, _status = self.get_slice(plan, (column,), row, 1)
        if slice_.height <= 0:
            return None

        try:
            table_column = slice_.column(column)
        except KeyError:
            return None

        values = table_column.values
        try:
            raw_value = values[0]
        except (IndexError, TypeError):
            return None
        display, truncated = summarize_value_preview(raw_value, max_chars=preview_chars)
        dtype = str(table_column.dtype) if table_column.dtype is not None else None
        absolute_row = slice_.start_offset
        if absolute_row is None:
            absolute_row = row

        return CellPreview(
            column=column,
            row=row,
            absolute_row=absolute_row,
            dtype=dtype,
            raw_value=raw_value,
            display=display,
            truncated=truncated,
        )

    def get_source_traits(self, plan: QueryPlan | None) -> SourceTraits | None:
        """Return cached or inferred source traits for ``plan`` when available."""

        effective_plan = plan or QueryPlan()
        key = self._plan_signature(effective_plan)
        with self._lock:
            cached = self._source_traits_cache.get(key)
        if cached is not None:
            return cached

        if self._fetcher is not None:
            return None

        prepared = self._prepare_materializer(effective_plan)
        if prepared is None:
            return None
        _materializer, physical_plan = prepared
        self._record_source_traits(effective_plan, physical_plan)
        with self._lock:
            return self._source_traits_cache.get(key)

    @staticmethod
    def _plan_is_simple(plan: QueryPlan) -> bool:
        if plan.filter_clauses or plan.sort or plan.search_text:
            return False
        return plan.offset == 0 and plan.limit is None

    def _ensure_strategy_for_context(self, context: PlanContext) -> Strategy | None:
        plan = context.plan
        key = self._plan_signature(plan)
        with self._lock:
            cached = self._strategy_cache.get(key)
            if cached is not None:
                self._apply_strategy_locked(cached)
                return cached

        traits = self.get_source_traits(plan)
        if traits is None:
            return None

        strategy = compile_strategy(traits)
        with self._lock:
            cache = self._strategy_cache
            cache[key] = strategy
            cache.move_to_end(key)
            while len(cache) > self.STRATEGY_CACHE_LIMIT:
                cache.popitem(last=False)
            self._apply_strategy_locked(strategy)
        return strategy

    def _apply_strategy_locked(self, strategy: Strategy) -> None:
        self._strategy = strategy
        if not self._streaming_enabled_configured:
            self._streaming_enabled = strategy.mode == "streaming"
        if not self._streaming_batch_rows_configured:
            self._streaming_batch_rows = max(1, strategy.batch_rows)

    def clear(self) -> None:
        """Cancel pending work and drop cached prefetches."""

        with self._lock:
            self._cache.clear()
            self._source_traits_cache.clear()
            self._strategy_cache.clear()
            self._strategy = None
            self._sidecar.clear()
            self._parquet_indexer.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _resolve_context(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
    ) -> PlanContext | None:
        requested = tuple(columns)
        if self._fetcher is not None:
            sheet_id, generation, plan_hash = self._current_job_metadata(plan)
            effective_plan = plan or QueryPlan()
            base_columns = tuple(self._schema_template().column_names)
            available_set = set(base_columns)
            present = tuple(col for col in requested if col in available_set)
            missing = tuple(col for col in requested if col not in available_set)
            return PlanContext(
                effective_plan,
                present,
                requested,
                missing,
                plan_hash,
                sheet_id,
                generation,
            )

        if self._engine_factory is None or self._columns_getter is None:
            return None

        available_columns = tuple(self._columns_getter())
        row_id_column = self._row_id_column
        if not available_columns:
            sheet_id, generation, plan_hash = self._current_job_metadata(plan)
            effective_plan = plan or QueryPlan()
            missing = tuple(requested)
            return PlanContext(
                effective_plan,
                (),
                requested,
                missing,
                plan_hash,
                sheet_id,
                generation,
            )

        available_set = set(available_columns)
        if row_id_column:
            available_set.add(row_id_column)
        present = tuple(col for col in requested if col in available_set)

        effective_plan = (plan or QueryPlan()).with_limit(None).with_offset(0)

        if effective_plan.projection:
            plan_for_fetch = effective_plan
        else:
            projection: list[str] = []
            for name in present:
                if name not in projection:
                    projection.append(name)
            for column, _ in effective_plan.sort:
                if column in available_set and column not in projection:
                    projection.append(column)
            if not projection:
                projection = list(available_columns)
            plan_for_fetch = effective_plan.with_projection(projection)

        if plan_for_fetch.projection:
            visible_columns = tuple(name for name in present if name in plan_for_fetch.projection)
        else:
            visible_columns = present

        def _dedup(seq: Sequence[str]) -> tuple[str, ...]:
            seen: set[str] = set()
            unique: list[str] = []
            for name in seq:
                if name in seen:
                    continue
                seen.add(name)
                unique.append(name)
            return tuple(unique)

        if row_id_column and row_id_column in available_set:
            projection_for_fetch = (
                list(plan_for_fetch.projection) if plan_for_fetch.projection else []
            )
            if row_id_column not in projection_for_fetch:
                projection_for_fetch.append(row_id_column)
                plan_for_fetch = plan_for_fetch.with_projection(_dedup(projection_for_fetch))

        sheet_id, generation, plan_hash = self._current_job_metadata(plan_for_fetch)
        missing = tuple(col for col in requested if col not in available_set)
        fetch_columns: tuple[str, ...]
        if row_id_column and row_id_column in available_set:
            fetch_columns = _dedup(list(visible_columns) + [row_id_column])
        else:
            fetch_columns = visible_columns
        return PlanContext(
            plan_for_fetch,
            fetch_columns,
            requested,
            missing,
            plan_hash,
            sheet_id,
            generation,
        )

    def _collect_plan_slice(
        self,
        plan: QueryPlan,
        start: int,
        count: int,
        columns: Sequence[str],
    ) -> TableSlice:
        prepared = self._prepare_materializer(plan)
        if prepared is None:
            return self._empty_slice(columns)
        materializer, physical_plan = prepared
        self._record_source_traits(plan, physical_plan)

        try:
            raw = materializer.collect_slice(
                physical_plan,
                start=start,
                length=count,
                columns=tuple(columns),
            )
        except PulkaCoreError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            msg = "Failed to materialise row slice"
            raise MaterializeError(msg) from exc
        return self._coerce_slice(raw, row_id_column=self._row_id_column)

    def prepare_sidecar_window(
        self,
        context: PlanContext,
        start: int,
        count: int,
        *,
        record_progress: bool,
    ) -> SidecarWindow:
        if self._fetcher is not None:
            return SidecarWindow.identity(start, count)
        with self._lock:
            strategy = self._strategy
        return self._sidecar.prepare_window(
            context,
            start,
            count,
            strategy=strategy,
            record_progress=record_progress,
        )

    def apply_sidecar_window(
        self,
        raw_slice: TableSlice,
        window: SidecarWindow,
        requested_count: int,
    ) -> TableSlice:
        return self._sidecar.apply_window(raw_slice, window, requested_count)

    def _prepare_materializer(self, plan: QueryPlan) -> tuple[MaterializerProtocol, Any] | None:
        adapter = self._engine_adapter()
        materializer = self._materializer
        if adapter is None or materializer is None:
            return None
        try:
            physical_plan = adapter.compile(plan)
        except PulkaCoreError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            msg = "Failed to compile plan for row slice"
            raise CompileError(msg) from exc
        return materializer, physical_plan

    def _record_source_traits(self, plan: QueryPlan, physical_plan: Any) -> None:
        traits = self._infer_source_traits_from_physical_plan(physical_plan)
        if traits is None:
            return
        key = self._plan_signature(plan)
        with self._lock:
            cache = self._source_traits_cache
            cache[key] = traits
            cache.move_to_end(key)
            while len(cache) > self.SOURCE_TRAITS_CACHE_LIMIT:
                cache.popitem(last=False)
            self._strategy_cache.pop(key, None)

    @staticmethod
    def _infer_source_traits_from_physical_plan(plan: Any) -> SourceTraits | None:
        try:
            from .engine.viewer_engine import infer_source_traits_from_plan
        except Exception:
            return None
        try:
            return infer_source_traits_from_plan(plan)
        except Exception:
            return None

    @staticmethod
    def _plan_signature(plan: QueryPlan) -> str:
        snapshot = plan.snapshot()
        return cast(str, snapshot["hash"])

    def _fetch_slice(
        self,
        context: PlanContext,
        start: int,
        count: int,
        *,
        window: SidecarWindow | None = None,
        record_progress: bool = True,
    ) -> tuple[TableSlice, SidecarWindow]:
        if not context.fetch_columns:
            empty = self._empty_slice(context.fetch_columns)
            return empty, SidecarWindow.identity(start, count)

        if self._fetcher is not None:
            raw = self._fetcher(start, count, context.fetch_columns)
            coerced = self._coerce_slice(raw, row_id_column=self._row_id_column)
            if coerced.start_offset is None:
                coerced = TableSlice(
                    coerced.columns,
                    coerced.schema,
                    start_offset=start,
                    row_ids=coerced.row_ids,
                )
            return coerced, SidecarWindow.identity(start, count)

        effective_window = window or self.prepare_sidecar_window(
            context,
            start,
            count,
            record_progress=record_progress,
        )
        fetch_start = effective_window.fetch_start
        fetch_count = effective_window.fetch_count
        raw = self._collect_plan_slice(
            context.plan,
            fetch_start,
            fetch_count,
            context.fetch_columns,
        )
        if raw.start_offset is None:
            raw = TableSlice(
                raw.columns,
                raw.schema,
                start_offset=fetch_start,
                row_ids=raw.row_ids,
            )
        trimmed = self.apply_sidecar_window(raw, effective_window, count)
        return trimmed, effective_window

    def _engine_adapter(self) -> EngineAdapterProtocol | None:
        if self._engine_factory is None:
            return None
        adapter = self._engine_factory()
        if not isinstance(adapter, EngineAdapterProtocol):
            msg = "engine_factory must return an EngineAdapterProtocol"
            raise TypeError(msg)
        return adapter

    def _empty_slice(self, columns: Sequence[str] | None = None) -> TableSlice:
        template = self._schema_template()
        if columns is None:
            return TableSlice.empty(template.column_names, template.schema)
        return TableSlice.empty(columns, template.schema)

    @staticmethod
    def _coerce_slice(result: Any, *, row_id_column: str | None = None) -> TableSlice:
        if isinstance(result, TableSlice):
            return result
        if result is None:
            return TableSlice.empty()
        if isinstance(result, pl.DataFrame):
            schema = getattr(result, "schema", {})
            return table_slice_from_dataframe(result, schema, row_id_column=row_id_column)
        try:
            frame = pl.DataFrame(result)
        except Exception as exc:  # pragma: no cover - defensive
            msg = (
                "RowProvider requires slice results compatible with TableSlice; "
                f"received {type(result)!r}"
            )
            raise MaterializeError(msg) from exc
        return table_slice_from_dataframe(frame, frame.schema, row_id_column=row_id_column)

    def _schema_template(self) -> TableSlice:
        template = self._empty_template
        if template is None:
            template = self._coerce_slice(
                self._empty_result_factory(), row_id_column=self._row_id_column
            )
            self._empty_template = template
        return template

    def _finalize_slice(
        self,
        context: PlanContext,
        raw_slice: TableSlice,
    ) -> tuple[TableSlice, SliceStatus]:
        status = SliceStatus.OK
        if context.missing_columns:
            status = self._merge_status(status, SliceStatus.PARTIAL)

        template = self._schema_template()
        schema = dict(template.schema)
        schema.update(raw_slice.schema)

        row_id_column = self._row_id_column

        raw_columns = {column.name: column for column in raw_slice.columns}
        raw_height = raw_slice.height

        row_ids = raw_slice.row_ids
        if row_id_column:
            column = raw_columns.pop(row_id_column, None)
            if row_ids is None and column is not None:
                row_ids = getattr(column, "data", None) or column.values

        result_columns: list[TableColumn] = []

        effective_expected = [
            name for name in context.fetch_columns if not row_id_column or name != row_id_column
        ]
        expected_fetch = set(effective_expected)
        missing_from_raw = [name for name in effective_expected if name not in raw_columns]
        if missing_from_raw:
            status = self._merge_status(status, SliceStatus.SCHEMA_MISMATCH)

        extra_columns = [
            name
            for name in raw_columns
            if name not in expected_fetch and (not row_id_column or name != row_id_column)
        ]
        if extra_columns:
            status = self._merge_status(status, SliceStatus.SCHEMA_MISMATCH)

        placeholder_reason = (
            SliceStatus.SCHEMA_MISMATCH
            if status is SliceStatus.SCHEMA_MISMATCH
            else SliceStatus.PARTIAL
        )

        for name in context.requested_columns:
            column = raw_columns.get(name)
            if column is not None:
                result_columns.append(column)
                continue
            dtype = schema.get(name)
            result_columns.append(
                self._placeholder_column(name, raw_height, dtype, placeholder_reason)
            )

        if not result_columns and raw_columns:
            result_columns.extend(raw_columns[name] for name in raw_slice.column_names)

        if row_id_column and row_ids is None and raw_height > 0:
            base_start = raw_slice.start_offset if raw_slice.start_offset is not None else 0
            row_ids = tuple(base_start + idx for idx in range(raw_height))

        final_slice = TableSlice(
            tuple(result_columns),
            schema,
            start_offset=raw_slice.start_offset,
            row_ids=row_ids,
        )
        return final_slice, status

    def _placeholder_column(
        self,
        name: str,
        height: int,
        dtype: Any,
        status: SliceStatus,
    ) -> TableColumn:
        values = tuple(None for _ in range(max(0, height)))
        null_count = len(values)

        label = "⟂ missing" if status is SliceStatus.PARTIAL else "⟂ schema"

        def _display(
            _row: int,
            _abs_row: int,
            _value: Any,
            _width: int | None,
            *,
            _label: str = label,
        ) -> str:
            return _label

        return TableColumn(name, values, dtype, null_count, _display)

    @staticmethod
    def _merge_status(left: SliceStatus, right: SliceStatus) -> SliceStatus:
        if right is SliceStatus.SCHEMA_MISMATCH:
            return SliceStatus.SCHEMA_MISMATCH
        if right is SliceStatus.PARTIAL and left is SliceStatus.OK:
            return SliceStatus.PARTIAL
        return left

    @staticmethod
    def _cell_count(slice_: TableSlice) -> int:
        return slice_.height * len(slice_.column_names)

    @staticmethod
    def _augment_telemetry(
        payload: dict[str, Any],
        *,
        strategy_payload: dict[str, Any] | None,
        window: SidecarWindow | None = None,
    ) -> dict[str, Any]:
        if strategy_payload is not None:
            payload["strategy"] = strategy_payload
        if window is not None and window.used:
            payload["sidecar"] = "checkpoints_used"
            if window.checkpoint_row is not None:
                payload["sidecar_checkpoint_row"] = window.checkpoint_row
        return payload

    def update_streaming_metrics(
        self,
        *,
        mode: str,
        chunks: int,
        rows: int,
        cells: int,
        duration_ns: int,
    ) -> None:
        with self._lock:
            self._streaming_last_mode = mode
            self._streaming_last_chunks = max(0, chunks)
            self._streaming_last_rows = max(0, rows)
            self._streaming_last_cells = max(0, cells)
            self._streaming_last_duration_ns = max(0, duration_ns)

    def cache_metrics(self) -> dict[str, int | str]:
        """Return current cache occupancy and eviction counters."""

        metrics: dict[str, int | str] = dict(self._cache.cache_metrics())
        with self._lock:
            metrics.update(
                {
                    "streaming_last_mode": self._streaming_last_mode,
                    "streaming_last_chunks": self._streaming_last_chunks,
                    "streaming_last_rows": self._streaming_last_rows,
                    "streaming_last_cells": self._streaming_last_cells,
                    "streaming_last_duration_ns": self._streaming_last_duration_ns,
                }
            )
        return metrics

    @property
    def _page_cache(self) -> OrderedDict[RowKey, TableSlice]:
        return self._cache.page_cache

    def _current_job_metadata(
        self, plan: QueryPlan | None
    ) -> tuple[str | None, int | None, str | None]:
        if self._job_context is None:
            plan_hash = plan.snapshot()["hash"] if plan is not None else None
            return None, None, plan_hash

        sheet_id, generation, plan_hash = self._job_context()
        if plan_hash is None and plan is not None:
            plan_hash = plan.snapshot()["hash"]
        return sheet_id, generation, plan_hash

    def _schedule_prefetch_windows(
        self,
        *,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
        windows: int,
    ) -> None:
        if windows <= 0 or count <= 0:
            return
        for window_index in range(1, windows + 1):
            next_start = start + window_index * count
            self.prefetch(plan, columns, next_start, count)

    @staticmethod
    def _cache_key(
        plan_hash: str | None,
        start: int,
        count: int,
        columns: Sequence[str],
    ) -> RowKey:
        cols_sig = normalized_columns_key(columns)
        return plan_hash, start, count, cols_sig


__all__ = [
    "CellPreview",
    "RowProvider",
    "SliceStatus",
    "SliceStreamRequest",
    "TableSliceChunk",
]
