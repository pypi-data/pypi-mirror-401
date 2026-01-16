"""Cache manager for row provider slices."""

from __future__ import annotations

import logging
from collections import OrderedDict
from collections.abc import Callable
from concurrent.futures import Future
from threading import RLock
from typing import Any

from .engine.contracts import TableSlice
from .row_provider_types import RowKey

LOGGER = logging.getLogger(__name__)


class RowCacheManager:
    def __init__(
        self,
        *,
        lock: RLock,
        cell_counter: Callable[[TableSlice], int],
        max_cache_cells: int,
        max_cache_entries: int,
        max_page_cache_cells: int,
        max_page_cache_entries: int,
    ) -> None:
        self._lock = lock
        self._cell_count = cell_counter
        self._cache: OrderedDict[RowKey, TableSlice] = OrderedDict()
        self._cache_cells = 0
        self._cache_evictions = 0
        self._page_cache: OrderedDict[RowKey, TableSlice] = OrderedDict()
        self._page_cache_cells = 0
        self._page_cache_evictions = 0
        self._prefetched_keys: set[RowKey] = set()
        self._prefetch_scheduled = 0
        self._prefetch_hits = 0
        self._prefetch_evictions = 0
        self._pending: set[RowKey] = set()
        self._pending_futures: dict[RowKey, Future[Any]] = {}
        self._max_cache_cells = max_cache_cells
        self._max_cache_entries = max_cache_entries
        self._max_page_cache_cells = max_page_cache_cells
        self._max_page_cache_entries = max_page_cache_entries

    def get_cache(self, key: RowKey) -> TableSlice | None:
        with self._lock:
            cached = self._cache.get(key)
            if cached is not None:
                self._cache.move_to_end(key)
                self._note_prefetch_hit_locked(key)
            return cached

    def get_page_cache(self, key: RowKey) -> TableSlice | None:
        with self._lock:
            cached = self._page_cache.get(key)
            if cached is not None:
                self._page_cache.move_to_end(key)
                self._note_prefetch_hit_locked(key)
            return cached

    def store_cache(self, key: RowKey, value: TableSlice, *, prefetched: bool = False) -> None:
        with self._lock:
            self._store_cache_entry_locked(key, value, prefetched=prefetched)

    def store_page_cache(self, key: RowKey, value: TableSlice, *, prefetched: bool = False) -> None:
        with self._lock:
            self._store_page_cache_entry_locked(key, value, prefetched=prefetched)

    def reserve_page_prefetch(self, key: RowKey) -> bool:
        with self._lock:
            if key in self._pending or key in self._page_cache:
                return False
            self._pending.add(key)
            self._prefetch_scheduled += 1
            return True

    def register_prefetch_future(self, key: RowKey, future: Future[Any]) -> None:
        with self._lock:
            self._pending_futures[key] = future

    def clear_pending(self, key: RowKey) -> None:
        with self._lock:
            self._pending.discard(key)
            self._pending_futures.pop(key, None)

    def mark_prefetched(self, key: RowKey, *, is_prefetched: bool) -> None:
        with self._lock:
            if is_prefetched:
                self._prefetched_keys.add(key)
            else:
                self._prefetched_keys.discard(key)

    def cancel_pending(self) -> None:
        with self._lock:
            for future in self._pending_futures.values():
                future.cancel()
            self._pending_futures.clear()
            self._pending.clear()

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._cache_cells = 0
            self._page_cache.clear()
            self._page_cache_cells = 0
            self._prefetched_keys.clear()
            self._pending.clear()
            for future in self._pending_futures.values():
                future.cancel()
            self._pending_futures.clear()

    def cache_metrics(self) -> dict[str, int]:
        with self._lock:
            return {
                "page_entries": len(self._page_cache),
                "page_cells": self._page_cache_cells,
                "page_evictions": self._page_cache_evictions,
                "page_max_entries": self._max_page_cache_entries,
                "page_max_cells": self._max_page_cache_cells,
                "entries": len(self._cache),
                "cells": self._cache_cells,
                "evictions": self._cache_evictions,
                "prefetch_scheduled": self._prefetch_scheduled,
                "prefetch_hits": self._prefetch_hits,
                "prefetch_evictions": self._prefetch_evictions,
                "max_entries": self._max_cache_entries,
                "max_cells": self._max_cache_cells,
            }

    @property
    def page_cache(self) -> OrderedDict[RowKey, TableSlice]:
        return self._page_cache

    def update_limits(
        self,
        *,
        max_cache_cells: int | None = None,
        max_cache_entries: int | None = None,
        max_page_cache_cells: int | None = None,
        max_page_cache_entries: int | None = None,
    ) -> None:
        with self._lock:
            if max_cache_cells is not None:
                self._max_cache_cells = max_cache_cells
            if max_cache_entries is not None:
                self._max_cache_entries = max_cache_entries
            if max_page_cache_cells is not None:
                self._max_page_cache_cells = max_page_cache_cells
            if max_page_cache_entries is not None:
                self._max_page_cache_entries = max_page_cache_entries

    def _note_prefetch_hit_locked(self, key: RowKey) -> None:
        if key not in self._prefetched_keys:
            return
        self._prefetched_keys.discard(key)
        self._prefetch_hits += 1
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.prefetch_hit",
                extra={
                    "event": "row_prefetch_hit",
                    "plan_hash": key[0],
                    "start": key[1],
                    "count": key[2],
                    "columns": key[3],
                    "hits": self._prefetch_hits,
                },
            )

    def _store_cache_entry_locked(
        self, key: RowKey, value: TableSlice, *, prefetched: bool = False
    ) -> None:
        existing = self._cache.pop(key, None)
        if existing is not None:
            self._cache_cells -= self._cell_count(existing)
            self._prefetched_keys.discard(key)
        self._cache[key] = value
        self._cache.move_to_end(key)
        self._cache_cells += self._cell_count(value)
        if prefetched:
            self._prefetched_keys.add(key)
        else:
            self._prefetched_keys.discard(key)
        self._enforce_cache_limits_locked()

    def _store_page_cache_entry_locked(
        self, key: RowKey, value: TableSlice, *, prefetched: bool = False
    ) -> None:
        existing = self._page_cache.pop(key, None)
        if existing is not None:
            self._page_cache_cells -= self._cell_count(existing)
            self._prefetched_keys.discard(key)
        self._page_cache[key] = value
        self._page_cache.move_to_end(key)
        self._page_cache_cells += self._cell_count(value)
        if prefetched:
            self._prefetched_keys.add(key)
        else:
            self._prefetched_keys.discard(key)
        self._enforce_page_cache_limits_locked()

    def _enforce_cache_limits_locked(self) -> None:
        while len(self._cache) > self._max_cache_entries or (
            self._max_cache_cells and self._cache_cells > self._max_cache_cells
        ):
            old_key, old_value = self._cache.popitem(last=False)
            removed_cells = self._cell_count(old_value)
            self._cache_cells -= removed_cells
            self._pending.discard(old_key)
            self._pending_futures.pop(old_key, None)
            if old_key in self._prefetched_keys:
                self._prefetched_keys.discard(old_key)
                self._prefetch_evictions += 1
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "row_provider.prefetch_evicted",
                        extra={
                            "event": "row_prefetch_evicted",
                            "plan_hash": old_key[0],
                            "start": old_key[1],
                            "count": old_key[2],
                            "columns": old_key[3],
                            "evictions": self._prefetch_evictions,
                        },
                    )
            self._cache_evictions += 1
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(
                    "row_provider.cache_eviction",
                    extra={
                        "event": "row_cache_eviction",
                        "plan_hash": old_key[0],
                        "start": old_key[1],
                        "count": old_key[2],
                        "columns": old_key[3],
                        "cells": removed_cells,
                        "evictions": self._cache_evictions,
                    },
                )

    def _enforce_page_cache_limits_locked(self) -> None:
        while len(self._page_cache) > self._max_page_cache_entries or (
            self._max_page_cache_cells and self._page_cache_cells > self._max_page_cache_cells
        ):
            old_key, old_value = self._page_cache.popitem(last=False)
            removed_cells = self._cell_count(old_value)
            self._page_cache_cells -= removed_cells
            self._pending.discard(old_key)
            self._pending_futures.pop(old_key, None)
            if old_key in self._prefetched_keys:
                self._prefetched_keys.discard(old_key)
                self._prefetch_evictions += 1
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "row_provider.prefetch_evicted",
                        extra={
                            "event": "row_prefetch_evicted",
                            "plan_hash": old_key[0],
                            "start": old_key[1],
                            "count": old_key[2],
                            "columns": old_key[3],
                            "evictions": self._prefetch_evictions,
                        },
                    )
            self._page_cache_evictions += 1
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(
                    "row_provider.page_cache_eviction",
                    extra={
                        "event": "row_page_cache_eviction",
                        "plan_hash": old_key[0],
                        "start": old_key[1],
                        "count": old_key[2],
                        "columns": old_key[3],
                        "cells": removed_cells,
                        "evictions": self._page_cache_evictions,
                    },
                )


__all__ = ["RowCacheManager"]
