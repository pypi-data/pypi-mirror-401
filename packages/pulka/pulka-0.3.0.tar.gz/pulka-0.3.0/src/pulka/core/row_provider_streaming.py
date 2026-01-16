"""Streaming pipeline for row provider slices."""

from __future__ import annotations

import inspect
import logging
from collections.abc import Iterator, Sequence
from dataclasses import asdict
from time import monotonic_ns
from typing import TYPE_CHECKING, Any, Protocol

import polars as pl

from .engine.contracts import TableSlice
from .engine.polars_adapter import table_slice_from_dataframe
from .errors import MaterializeError, PulkaCoreError
from .interfaces import MaterializerProtocol
from .row_provider_sidecar import SidecarWindow
from .row_provider_types import PlanContext, SliceStatus, SliceStreamRequest, TableSliceChunk
from .strategy import Strategy

if TYPE_CHECKING:
    from .row_provider_cache import RowCacheManager
    from .row_provider_parquet import ParquetRowGroupIndexer
    from .row_provider_sidecar import SidecarWindowManager
    from .source_traits import SourceTraits


LOGGER = logging.getLogger(__name__)

_PARQUET_ROW_GROUP_PARAM: str | None = None
try:  # pragma: no cover - depends on polars version
    _params = inspect.signature(pl.read_parquet).parameters
    if "row_groups" in _params:
        _PARQUET_ROW_GROUP_PARAM = "row_groups"
    elif "row_group" in _params:
        _PARQUET_ROW_GROUP_PARAM = "row_group"
except Exception:
    _PARQUET_ROW_GROUP_PARAM = None


class RowStreamingHost(Protocol):
    _fetcher: Any
    _row_id_column: str | None
    _streaming_enabled: bool
    _streaming_batch_rows: int
    _page_size: int
    _cache: RowCacheManager
    _parquet_indexer: ParquetRowGroupIndexer
    _sidecar: SidecarWindowManager

    def _resolve_context(self, plan: Any, columns: Sequence[str]) -> PlanContext | None: ...

    def _empty_slice(self, columns: Sequence[str] | None = None) -> TableSlice: ...

    def _finalize_slice(
        self, context: PlanContext, raw_slice: TableSlice
    ) -> tuple[TableSlice, SliceStatus]: ...

    def _cache_key(
        self, plan_hash: str | None, start: int, count: int, columns: Sequence[str]
    ) -> Any: ...

    def _fetch_slice(
        self,
        context: PlanContext,
        start: int,
        count: int,
        *,
        window: SidecarWindow | None = None,
        record_progress: bool = True,
    ) -> tuple[TableSlice, SidecarWindow]: ...

    def _prepare_materializer(self, plan: Any) -> tuple[MaterializerProtocol, Any] | None: ...

    def _record_source_traits(self, plan: Any, physical_plan: Any) -> None: ...

    def _coerce_slice(self, result: Any, *, row_id_column: str | None = None) -> TableSlice: ...

    def get_source_traits(self, plan: Any) -> SourceTraits | None: ...

    def _plan_is_simple(self, plan: Any) -> bool: ...

    def _ensure_strategy_for_context(self, context: PlanContext) -> Strategy | None: ...

    def current_strategy(self) -> Strategy | None: ...

    def prepare_sidecar_window(
        self, context: PlanContext, start: int, count: int, *, record_progress: bool
    ) -> SidecarWindow: ...

    def apply_sidecar_window(
        self, raw_slice: TableSlice, window: SidecarWindow, requested_count: int
    ) -> TableSlice: ...

    def _augment_telemetry(
        self,
        payload: dict[str, Any],
        *,
        strategy_payload: dict[str, Any] | None,
        window: SidecarWindow | None = None,
    ) -> dict[str, Any]: ...

    def update_streaming_metrics(
        self, *, mode: str, chunks: int, rows: int, cells: int, duration_ns: int
    ) -> None: ...

    def _cell_count(self, slice_: TableSlice) -> int: ...

    def _schedule_prefetch_windows(
        self, *, plan: Any, columns: Sequence[str], start: int, count: int, windows: int
    ) -> None: ...


class RowStreamingPipeline:
    def __init__(self, host: RowStreamingHost) -> None:
        self._host = host

    def get_slice_stream(self, request: SliceStreamRequest) -> Iterator[TableSliceChunk]:
        columns = tuple(request.columns)
        request_start = int(request.start)
        count = int(request.count)
        telemetry_base = dict(request.telemetry or {})

        if count <= 0:
            yield from self._stream_empty(request_start, columns, telemetry_base)
            return

        context = self._host._resolve_context(request.plan, columns)
        if context is None:
            yield from self._stream_schema_mismatch(request_start, columns, telemetry_base)
            return

        if not context.fetch_columns:
            yield from self._stream_direct_columns(
                context,
                request,
                telemetry_base,
                columns=columns,
                request_start=request_start,
                count=count,
            )
            return

        parquet_stream = self._stream_parquet_rows(
            context,
            request,
            telemetry_base,
            columns=columns,
            request_start=request_start,
            count=count,
        )
        if parquet_stream is not None:
            yield from parquet_stream
            return

        yield from self._stream_sidecar(
            context,
            request,
            telemetry_base,
            columns=columns,
            request_start=request_start,
            count=count,
        )

    def _stream_empty(
        self,
        request_start: int,
        columns: tuple[str, ...],
        telemetry_base: dict[str, Any],
    ) -> Iterator[TableSliceChunk]:
        empty = self._host._empty_slice(columns)
        status = SliceStatus.PARTIAL if columns else SliceStatus.OK
        telemetry = {
            **telemetry_base,
            "mode": "empty",
            "chunks": 1,
            "rows": 0,
            "cells": 0,
            "duration_ns": 0,
            "offset": request_start,
        }
        self._host.update_streaming_metrics(mode="empty", chunks=1, rows=0, cells=0, duration_ns=0)
        yield TableSliceChunk(request_start, empty, status, True, telemetry)

    def _stream_schema_mismatch(
        self,
        request_start: int,
        columns: tuple[str, ...],
        telemetry_base: dict[str, Any],
    ) -> Iterator[TableSliceChunk]:
        empty = self._host._empty_slice(columns)
        telemetry = {
            **telemetry_base,
            "mode": "schema_mismatch",
            "chunks": 1,
            "rows": 0,
            "cells": 0,
            "duration_ns": 0,
            "offset": request_start,
        }
        self._host.update_streaming_metrics(
            mode="schema_mismatch",
            chunks=1,
            rows=0,
            cells=0,
            duration_ns=0,
        )
        yield TableSliceChunk(request_start, empty, SliceStatus.SCHEMA_MISMATCH, True, telemetry)

    def _stream_direct_columns(
        self,
        context: PlanContext,
        request: SliceStreamRequest,
        telemetry_base: dict[str, Any],
        *,
        columns: tuple[str, ...],
        request_start: int,
        count: int,
    ) -> Iterator[TableSliceChunk]:
        key = self._host._cache_key(context.plan_hash, request_start, count, context.fetch_columns)
        cached = self._host._cache.get_cache(key)
        strategy = self._host.current_strategy()
        strategy_payload = asdict(strategy) if strategy is not None else None

        if cached is not None:
            final_slice, status = self._host._finalize_slice(context, cached)
            cells = self._host._cell_count(final_slice)
            telemetry = self._host._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "cache",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": 0,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
            )
            self._host.update_streaming_metrics(
                mode="cache",
                chunks=1,
                rows=final_slice.height,
                cells=cells,
                duration_ns=0,
            )
            self._host._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=strategy.prefetch_windows if strategy is not None else 0,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        raw = self._host._empty_slice(context.fetch_columns)
        final_slice, status = self._host._finalize_slice(context, raw)
        cells = self._host._cell_count(final_slice)
        telemetry = self._host._augment_telemetry(
            {
                **telemetry_base,
                "mode": "empty",
                "chunks": 1,
                "rows": final_slice.height,
                "cells": cells,
                "duration_ns": 0,
                "offset": request_start,
                "plan_hash": context.plan_hash,
            },
            strategy_payload=strategy_payload,
        )
        self._host._cache.store_cache(key, raw)
        self._host.update_streaming_metrics(
            mode="empty",
            chunks=1,
            rows=final_slice.height,
            cells=cells,
            duration_ns=0,
        )
        yield TableSliceChunk(request_start, final_slice, status, True, telemetry)

    def _stream_parquet_rows(
        self,
        context: PlanContext,
        request: SliceStreamRequest,
        telemetry_base: dict[str, Any],
        *,
        columns: tuple[str, ...],
        request_start: int,
        count: int,
    ) -> Iterator[TableSliceChunk] | None:
        if self._host._fetcher is not None or _PARQUET_ROW_GROUP_PARAM is None:
            return None
        if request.streaming_enabled is False:
            return None
        if not self._host._plan_is_simple(context.plan):
            return None

        traits = self._host.get_source_traits(context.plan)
        if traits is None or traits.kind != "parquet" or not traits.path:
            return None

        index = self._host._parquet_indexer.get(traits.path)
        if index is None or not index.row_group_rows:
            return None

        if count <= 0:
            return None

        def _iterator() -> Iterator[TableSliceChunk]:
            request_start_local = max(0, int(request_start))
            if request_start_local >= index.total_rows:
                empty = self._host._empty_slice(context.fetch_columns)
                status = SliceStatus.PARTIAL if context.requested_columns else SliceStatus.OK
                telemetry = self._host._augment_telemetry(
                    {
                        **telemetry_base,
                        "mode": "stream",
                        "reason": "row_group_seek",
                        "chunks": 1,
                        "rows": 0,
                        "cells": 0,
                        "duration_ns": 0,
                        "offset": request_start_local,
                        "plan_hash": context.plan_hash,
                    },
                    strategy_payload=None,
                )
                self._host.update_streaming_metrics(
                    mode="stream",
                    chunks=1,
                    rows=0,
                    cells=0,
                    duration_ns=0,
                )
                yield TableSliceChunk(request_start_local, empty, status, True, telemetry)
                return

            strategy = self._host._ensure_strategy_for_context(context)
            strategy_payload = asdict(strategy) if strategy is not None else None
            prefetch_windows = strategy.prefetch_windows if strategy is not None else 0
            prefetch_scheduled = False

            batch_rows = (
                request.batch_rows
                if request.batch_rows and request.batch_rows > 0
                else self._host._streaming_batch_rows
            )

            parquet_path = traits.path
            if parquet_path is None:  # pragma: no cover - defensive
                raise RuntimeError("Parquet streaming requested without a dataset path")

            def _read_group(group_index: int) -> pl.DataFrame:
                kwargs: dict[str, Any] = {}
                if context.fetch_columns:
                    source_columns = [
                        name for name in context.fetch_columns if name != self._host._row_id_column
                    ]
                    if source_columns:
                        kwargs["columns"] = source_columns
                if _PARQUET_ROW_GROUP_PARAM == "row_groups":
                    kwargs["row_groups"] = [group_index]
                elif _PARQUET_ROW_GROUP_PARAM == "row_group":
                    kwargs["row_group"] = group_index
                return pl.read_parquet(parquet_path, **kwargs)

            start_ns = monotonic_ns()
            last_chunk_ns = start_ns
            total_rows = 0
            chunk_index = 0
            remaining = max(0, int(count))
            start_group, group_start = index.seek(request_start_local)
            trim_leading = max(0, request_start_local - group_start)
            assembled_raw: TableSlice | None = None

            try:
                for group_idx in range(start_group, len(index.row_group_rows)):
                    if remaining <= 0:
                        break
                    group_start = index.row_group_offsets[group_idx]
                    df = _read_group(group_idx)
                    if trim_leading:
                        df = df.slice(trim_leading, None)
                        group_start += trim_leading
                        trim_leading = 0
                    if remaining < df.height:
                        df = df.slice(0, remaining)
                    if df.height <= 0:
                        continue

                    if self._host._row_id_column:
                        row_ids = pl.Series(
                            self._host._row_id_column,
                            range(group_start, group_start + df.height),
                        )
                        df = df.with_columns(row_ids)

                    raw_slice = table_slice_from_dataframe(
                        df,
                        df.schema,
                        row_id_column=self._host._row_id_column,
                    )
                    if raw_slice.start_offset is None:
                        raw_slice = TableSlice(
                            raw_slice.columns,
                            raw_slice.schema,
                            start_offset=group_start,
                            row_ids=raw_slice.row_ids,
                        )

                    chunk_slices = [raw_slice]
                    if batch_rows and raw_slice.height > batch_rows:
                        chunk_slices = []
                        offset = 0
                        while offset < raw_slice.height:
                            length = min(batch_rows, raw_slice.height - offset)
                            chunk_slices.append(raw_slice.slice(offset, length))
                            offset += length

                    for chunk_slice in chunk_slices:
                        if chunk_slice.height <= 0:
                            continue
                        chunk_offset = chunk_slice.start_offset or (
                            request_start_local + total_rows
                        )
                        total_rows += chunk_slice.height
                        remaining = max(0, count - total_rows)
                        assembled_raw = (
                            chunk_slice
                            if assembled_raw is None
                            else assembled_raw.concat_vertical(chunk_slice)
                        )
                        finalized_chunk, chunk_status = self._host._finalize_slice(
                            context, chunk_slice
                        )
                        now_ns = monotonic_ns()
                        chunk_duration_ns = now_ns - last_chunk_ns
                        last_chunk_ns = now_ns
                        chunk_index += 1
                        chunk_cells = self._host._cell_count(finalized_chunk)
                        chunk_telemetry = self._host._augment_telemetry(
                            {
                                **telemetry_base,
                                "mode": "stream",
                                "reason": "row_group_seek",
                                "chunk_index": chunk_index,
                                "rows": finalized_chunk.height,
                                "cells": chunk_cells,
                                "duration_ns": chunk_duration_ns,
                                "offset": chunk_offset,
                                "plan_hash": context.plan_hash,
                                "row_group_start": group_start,
                                "row_group_index": group_idx,
                            },
                            strategy_payload=strategy_payload,
                        )
                        yield TableSliceChunk(
                            chunk_offset,
                            finalized_chunk,
                            chunk_status,
                            False,
                            chunk_telemetry,
                        )
                        if not prefetch_scheduled and prefetch_windows > 0:
                            self._host._schedule_prefetch_windows(
                                plan=request.plan,
                                columns=columns,
                                start=request_start_local,
                                count=count,
                                windows=prefetch_windows,
                            )
                            prefetch_scheduled = True
                        if remaining <= 0:
                            break
            except Exception as exc:
                msg = "Failed to stream parquet row groups"
                raise MaterializeError(msg) from exc

            if assembled_raw is None:
                assembled_raw = self._host._empty_slice(context.fetch_columns)

            total_duration_ns = monotonic_ns() - start_ns
            final_slice, status = self._host._finalize_slice(context, assembled_raw)
            final_cells = self._host._cell_count(final_slice)
            total_chunks = max(1, chunk_index + 1)
            summary_telemetry = self._host._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "stream",
                    "reason": "row_group_seek",
                    "chunk_index": total_chunks,
                    "chunks": total_chunks,
                    "rows": final_slice.height,
                    "cells": final_cells,
                    "duration_ns": total_duration_ns,
                    "offset": request_start_local,
                    "plan_hash": context.plan_hash,
                    "row_group_index": start_group,
                },
                strategy_payload=strategy_payload,
            )
            key = self._host._cache_key(
                context.plan_hash,
                request_start_local,
                count,
                context.fetch_columns,
            )
            self._host._cache.store_cache(key, assembled_raw)
            self._host.update_streaming_metrics(
                mode="stream",
                chunks=total_chunks,
                rows=final_slice.height,
                cells=final_cells,
                duration_ns=total_duration_ns,
            )
            if not prefetch_scheduled and prefetch_windows > 0:
                self._host._schedule_prefetch_windows(
                    plan=request.plan,
                    columns=columns,
                    start=request_start_local,
                    count=count,
                    windows=prefetch_windows,
                )
            yield TableSliceChunk(request_start_local, final_slice, status, True, summary_telemetry)

        return _iterator()

    def _stream_sidecar(
        self,
        context: PlanContext,
        request: SliceStreamRequest,
        telemetry_base: dict[str, Any],
        *,
        columns: tuple[str, ...],
        request_start: int,
        count: int,
    ) -> Iterator[TableSliceChunk]:
        strategy = self._host._ensure_strategy_for_context(context)
        window = SidecarWindow.identity(request_start, count)
        if self._host._fetcher is None:
            window = self._host.prepare_sidecar_window(
                context,
                request_start,
                count,
                record_progress=True,
            )

        strategy_payload = asdict(strategy) if strategy is not None else None

        key = self._host._cache_key(context.plan_hash, request_start, count, context.fetch_columns)
        cached = self._host._cache.get_cache(key)
        if cached is not None:
            final_slice, status = self._host._finalize_slice(context, cached)
            cells = self._host._cell_count(final_slice)
            telemetry = self._host._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "cache",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": 0,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
                window=window,
            )
            self._host.update_streaming_metrics(
                mode="cache",
                chunks=1,
                rows=final_slice.height,
                cells=cells,
                duration_ns=0,
            )
            self._host._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=strategy.prefetch_windows if strategy is not None else 0,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        stream_enabled = (
            request.streaming_enabled
            if request.streaming_enabled is not None
            else self._host._streaming_enabled
        )
        batch_rows = (
            request.batch_rows
            if request.batch_rows and request.batch_rows > 0
            else self._host._streaming_batch_rows
        )

        if self._host._fetcher is not None:
            start_ns = monotonic_ns()
            raw_slice, _ = self._host._fetch_slice(
                context,
                request_start,
                count,
                record_progress=False,
            )
            final_slice, status = self._host._finalize_slice(context, raw_slice)
            duration_ns = monotonic_ns() - start_ns
            cells = self._host._cell_count(final_slice)
            telemetry = self._host._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "passthrough",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": duration_ns,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
            )
            self._host._cache.store_cache(key, raw_slice)
            self._host.update_streaming_metrics(
                mode="passthrough",
                chunks=1,
                rows=final_slice.height,
                cells=cells,
                duration_ns=duration_ns,
            )
            self._host._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=strategy.prefetch_windows if strategy is not None else 0,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        start_ns = monotonic_ns()
        prepared = self._host._prepare_materializer(context.plan)
        if prepared is None:
            raw_slice = self._host._empty_slice(context.fetch_columns)
            final_slice, status = self._host._finalize_slice(context, raw_slice)
            cells = self._host._cell_count(final_slice)
            telemetry = self._host._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "collect",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": 0,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
                window=window,
            )
            self._host._cache.store_cache(key, raw_slice)
            self._host.update_streaming_metrics(
                mode="collect",
                chunks=1,
                rows=final_slice.height,
                cells=cells,
                duration_ns=0,
            )
            self._host._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=strategy.prefetch_windows if strategy is not None else 0,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        materializer, physical_plan = prepared
        self._host._record_source_traits(context.plan, physical_plan)
        stream_attr = getattr(materializer, "collect_slice_stream", None)
        stream_iterator: Iterator[TableSlice] | None = None
        stream_mode = "collect"
        stream_reason = "disabled"
        prefetch_windows = strategy.prefetch_windows if strategy is not None else 0
        prefetch_scheduled = False
        stream_kwargs = {
            "start": window.fetch_start,
            "length": window.fetch_count,
            "columns": tuple(context.fetch_columns),
        }
        if stream_enabled and callable(stream_attr):
            if batch_rows > 0:
                stream_kwargs["batch_rows"] = batch_rows
            try:
                stream_iterator = iter(stream_attr(physical_plan, **stream_kwargs))
                stream_mode = "stream"
                stream_reason = "stream"
            except TypeError:
                stream_kwargs.pop("batch_rows", None)
                try:
                    stream_iterator = iter(stream_attr(physical_plan, **stream_kwargs))
                    stream_mode = "stream"
                    stream_reason = "stream"
                except TypeError:
                    stream_iterator = None
                    stream_reason = "type_error"
                except PulkaCoreError:
                    raise
                except Exception:
                    stream_iterator = None
                    stream_reason = "error"
            except PulkaCoreError:
                raise
            except Exception:
                stream_iterator = None
                stream_reason = "error"
        else:
            if not stream_enabled:
                stream_reason = "disabled"
            elif stream_attr is None:
                stream_reason = "missing"
            else:
                stream_reason = "invalid"

        if stream_iterator is None:
            try:
                raw = materializer.collect_slice(
                    physical_plan,
                    start=window.fetch_start,
                    length=window.fetch_count,
                    columns=tuple(context.fetch_columns),
                )
            except PulkaCoreError:
                raise
            except Exception as exc:  # pragma: no cover - defensive
                msg = "Failed to materialise row slice"
                raise MaterializeError(msg) from exc
            coerced = self._host._coerce_slice(raw, row_id_column=self._host._row_id_column)
            trimmed = self._host.apply_sidecar_window(coerced, window, count)
            final_slice, status = self._host._finalize_slice(context, trimmed)
            duration_ns = monotonic_ns() - start_ns
            cells = self._host._cell_count(final_slice)
            telemetry = self._host._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": stream_mode,
                    "reason": stream_reason,
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": duration_ns,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
                window=window,
            )
            self._host._cache.store_cache(key, trimmed)
            self._host.update_streaming_metrics(
                mode=stream_mode,
                chunks=1,
                rows=final_slice.height,
                cells=cells,
                duration_ns=duration_ns,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        total_rows = 0
        chunk_index = 0
        last_chunk_ns = start_ns
        skip_rows = window.trim_leading
        assembled_raw: TableSlice | None = None
        try:
            while True:
                try:
                    raw_chunk = next(stream_iterator)
                except StopIteration:
                    break
                chunk_slice = self._host._coerce_slice(
                    raw_chunk, row_id_column=self._host._row_id_column
                )
                if chunk_slice.height <= 0:
                    continue
                if skip_rows > 0:
                    if chunk_slice.height <= skip_rows:
                        skip_rows -= chunk_slice.height
                        continue
                    chunk_slice = chunk_slice.slice(skip_rows, None)
                    skip_rows = 0
                remaining = max(0, count - total_rows)
                if remaining <= 0:
                    break
                if chunk_slice.height > remaining:
                    chunk_slice = chunk_slice.slice(0, remaining)
                if chunk_slice.height <= 0:
                    continue
                chunk_offset = request_start + total_rows
                total_rows += chunk_slice.height
                if chunk_slice.start_offset is None:
                    chunk_slice = TableSlice(
                        tuple(chunk_slice.columns),
                        chunk_slice.schema,
                        start_offset=chunk_offset,
                        row_ids=chunk_slice.row_ids,
                    )
                assembled_raw = (
                    chunk_slice
                    if assembled_raw is None
                    else assembled_raw.concat_vertical(chunk_slice)
                )
                finalized_chunk, chunk_status = self._host._finalize_slice(context, chunk_slice)
                now_ns = monotonic_ns()
                chunk_duration_ns = now_ns - last_chunk_ns
                last_chunk_ns = now_ns
                chunk_index += 1
                chunk_cells = self._host._cell_count(finalized_chunk)
                chunk_telemetry = self._host._augment_telemetry(
                    {
                        **telemetry_base,
                        "mode": stream_mode,
                        "reason": stream_reason,
                        "chunk_index": chunk_index,
                        "rows": finalized_chunk.height,
                        "cells": chunk_cells,
                        "duration_ns": chunk_duration_ns,
                        "offset": chunk_offset,
                        "plan_hash": context.plan_hash,
                    },
                    strategy_payload=strategy_payload,
                    window=window,
                )
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "row_provider.stream_chunk",
                        extra={
                            "event": "row_stream_chunk",
                            "plan_hash": context.plan_hash,
                            "chunk_index": chunk_index,
                            "rows": finalized_chunk.height,
                            "offset": chunk_offset,
                        },
                    )
                yield TableSliceChunk(
                    chunk_offset,
                    finalized_chunk,
                    chunk_status,
                    False,
                    chunk_telemetry,
                )
                if not prefetch_scheduled and prefetch_windows > 0:
                    self._host._schedule_prefetch_windows(
                        plan=request.plan,
                        columns=columns,
                        start=request_start,
                        count=count,
                        windows=prefetch_windows,
                    )
                    prefetch_scheduled = True
                chunk_offset += chunk_slice.height
                if total_rows >= count:
                    break
        except PulkaCoreError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            msg = "Failed to materialise streaming slice"
            raise MaterializeError(msg) from exc

        if assembled_raw is None:
            assembled_raw = self._host._empty_slice(context.fetch_columns)
        total_duration_ns = monotonic_ns() - start_ns
        final_slice, status = self._host._finalize_slice(context, assembled_raw)
        final_cells = self._host._cell_count(final_slice)
        total_chunks = chunk_index + 1
        summary_telemetry = self._host._augment_telemetry(
            {
                **telemetry_base,
                "mode": stream_mode,
                "reason": stream_reason,
                "chunk_index": total_chunks,
                "chunks": total_chunks,
                "rows": final_slice.height,
                "cells": final_cells,
                "duration_ns": total_duration_ns,
                "offset": request_start,
                "plan_hash": context.plan_hash,
            },
            strategy_payload=strategy_payload,
            window=window,
        )
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.stream_complete",
                extra={
                    "event": "row_stream_complete",
                    "plan_hash": context.plan_hash,
                    "chunks": total_chunks,
                    "rows": final_slice.height,
                    "duration_ns": total_duration_ns,
                },
            )
        self._host._cache.store_cache(key, assembled_raw)
        self._host.update_streaming_metrics(
            mode=stream_mode,
            chunks=total_chunks,
            rows=final_slice.height,
            cells=final_cells,
            duration_ns=total_duration_ns,
        )
        if not prefetch_scheduled and prefetch_windows > 0:
            self._host._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=prefetch_windows,
            )
        yield TableSliceChunk(request_start, final_slice, status, True, summary_telemetry)


__all__ = ["RowStreamingPipeline"]
