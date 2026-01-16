"""Sidecar window manager for row provider fetches."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from threading import RLock
from typing import Any

from ..data import csv_checkpoints
from ..data.sidecar import SidecarStore
from .engine.contracts import TableSlice
from .interfaces import JobRunnerProtocol
from .jobs import JobRequest
from .row_provider_types import PlanContext
from .source_traits import SourceTraits
from .strategy import Strategy

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class SidecarWindow:
    fetch_start: int
    fetch_count: int
    trim_leading: int
    used: bool
    checkpoint_row: int | None

    @classmethod
    def identity(cls, start: int, count: int) -> SidecarWindow:
        return cls(start, count, 0, False, None)


@dataclass(slots=True)
class _SidecarProgress:
    max_seen_start: int = -1
    last_span: int = 0
    screens_seen: int = 0

    def reset(self) -> None:
        self.max_seen_start = -1
        self.last_span = 0
        self.screens_seen = 0

    def observe(self, *, start: int, span: int) -> None:
        if span > 0:
            self.last_span = span if self.last_span <= 0 else max(self.last_span, span)
        if start < 0:
            return
        if self.max_seen_start < 0:
            self.max_seen_start = start
            return
        if start <= self.max_seen_start:
            return
        height = self.last_span or span or 1
        delta = start - self.max_seen_start
        steps = max(1, delta // max(height, 1))
        self.screens_seen += steps
        self.max_seen_start = start
        self.last_span = span if span > 0 else self.last_span


@dataclass(slots=True)
class _SidecarState:
    store: SidecarStore
    offsets: tuple[int, ...] | None = None
    building: bool = False
    failed: bool = False
    progress: _SidecarProgress = field(default_factory=_SidecarProgress)
    generation: int | None = None


class SidecarWindowManager:
    def __init__(
        self,
        *,
        lock: RLock,
        runner: JobRunnerProtocol,
        traits_getter: Callable[[Any], SourceTraits | None],
    ) -> None:
        self._lock = lock
        self._runner = runner
        self._traits_getter = traits_getter
        self._states: dict[str, _SidecarState] = {}

    def prepare_window(
        self,
        context: PlanContext,
        start: int,
        count: int,
        *,
        strategy: Strategy | None,
        record_progress: bool,
    ) -> SidecarWindow:
        if count <= 0 or start < 0:
            return SidecarWindow.identity(start, count)

        if strategy is None or strategy.build_sidecar_after_screens is None:
            return SidecarWindow.identity(start, count)

        traits = self._traits_getter(context.plan)
        if traits is None or traits.kind not in {"csv", "tsv", "jsonl"}:
            return SidecarWindow.identity(start, count)

        path = traits.path
        if not path:
            return SidecarWindow.identity(start, count)

        interval = max(1, csv_checkpoints.CHECKPOINT_EVERY_ROWS)

        with self._lock:
            state = self._get_or_create_sidecar_state_locked(path)
            if context.generation is not None and state.generation != context.generation:
                state.progress.reset()
                state.generation = context.generation
                state.building = False
                state.failed = False

            if record_progress:
                state.progress.observe(start=start, span=count)
            elif count > 0 and state.progress.last_span <= 0:
                state.progress.last_span = count

            offsets = state.offsets
            threshold = strategy.build_sidecar_after_screens
            should_schedule = (
                record_progress
                and threshold is not None
                and state.progress.screens_seen >= threshold
                and not state.building
                and not state.failed
                and offsets is None
            )
            if should_schedule:
                self._schedule_sidecar_job_locked(state, path, context, interval)
            offsets = state.offsets

        if not offsets or len(offsets) <= 1:
            return SidecarWindow.identity(start, count)

        index = max(0, min(len(offsets) - 1, start // interval))
        checkpoint_row = index * interval
        if checkpoint_row >= start and index > 0:
            checkpoint_row = (index - 1) * interval

        if checkpoint_row < 0 or checkpoint_row >= start:
            return SidecarWindow.identity(start, count)

        trim_leading = start - checkpoint_row
        if trim_leading <= 0:
            return SidecarWindow.identity(start, count)

        fetch_count = count + trim_leading
        return SidecarWindow(
            fetch_start=checkpoint_row,
            fetch_count=fetch_count,
            trim_leading=trim_leading,
            used=True,
            checkpoint_row=checkpoint_row,
        )

    def apply_window(
        self,
        raw_slice: TableSlice,
        window: SidecarWindow,
        requested_count: int,
    ) -> TableSlice:
        trimmed = raw_slice
        if window.trim_leading > 0:
            trimmed = trimmed.slice(window.trim_leading, None)

        if requested_count >= 0 and trimmed.height > requested_count:
            trimmed = trimmed.slice(0, requested_count)

        return trimmed

    def clear(self) -> None:
        with self._lock:
            self._states.clear()

    def _get_or_create_sidecar_state_locked(self, path: str) -> _SidecarState:
        state = self._states.get(path)
        if state is not None:
            return state

        store = SidecarStore(path)
        offsets: tuple[int, ...] | None = None
        if store.has(csv_checkpoints.CHECKPOINT_ARTIFACT):
            try:
                offsets = store.read_offsets(csv_checkpoints.CHECKPOINT_ARTIFACT)
            except Exception as exc:  # pragma: no cover - defensive guardrail
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "row_provider.sidecar_load_failed",
                        extra={
                            "event": "row_sidecar_load_failed",
                            "path": path,
                        },
                        exc_info=exc,
                    )
                offsets = None

        state = _SidecarState(store=store, offsets=offsets)
        self._states[path] = state
        return state

    def _schedule_sidecar_job_locked(
        self,
        state: _SidecarState,
        path: str,
        context: PlanContext,
        interval: int,
    ) -> None:
        sheet_id = context.sheet_id
        generation = context.generation
        if sheet_id is None or generation is None:
            return

        job_tag = f"sidecar:{state.store.key}:{csv_checkpoints.CHECKPOINT_ARTIFACT}"

        def _job(
            _: int,
            *,
            _path: str = path,
            _store: SidecarStore = state.store,
            _interval: int = interval,
        ) -> tuple[int, ...] | None:
            return csv_checkpoints.build_csv_checkpoints(_path, store=_store, every_n=_interval)

        req = JobRequest(
            sheet_id=sheet_id,
            generation=generation,
            tag=job_tag,
            fn=_job,
            cache_result=False,
        )

        future = self._runner.enqueue(req)
        state.building = True
        state.failed = False

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.sidecar_schedule",
                extra={
                    "event": "row_sidecar_schedule",
                    "path": path,
                    "interval": interval,
                    "plan_hash": context.plan_hash,
                },
            )

        def _on_done(fut: Any) -> None:
            try:
                result = fut.result()
            except Exception as exc:  # pragma: no cover - defensive guardrail
                if LOGGER.isEnabledFor(logging.WARNING):
                    LOGGER.warning(
                        "row_provider.sidecar_error",
                        extra={
                            "event": "row_sidecar_error",
                            "path": path,
                        },
                        exc_info=exc,
                    )
                with self._lock:
                    state.building = False
                    state.failed = True
                return

            if result.error is not None:
                if LOGGER.isEnabledFor(logging.WARNING):
                    LOGGER.warning(
                        "row_provider.sidecar_error",
                        extra={
                            "event": "row_sidecar_error",
                            "path": path,
                        },
                        exc_info=result.error,
                    )
                with self._lock:
                    state.building = False
                    state.failed = True
                return

            offsets_value = result.value or ()
            if result.generation != generation:
                with self._lock:
                    state.building = False
                return

            offsets_tuple = tuple(offsets_value)
            with self._lock:
                state.building = False
                state.offsets = offsets_tuple
                state.failed = False

        future.add_done_callback(_on_done)


__all__ = ["SidecarWindow", "SidecarWindowManager"]
