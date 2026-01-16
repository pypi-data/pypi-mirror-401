"""Parquet row-group indexing utilities for row streaming."""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from threading import RLock

import polars as pl


@dataclass(slots=True, frozen=True)
class ParquetRowGroupIndex:
    path: str
    row_group_rows: tuple[int, ...]
    row_group_offsets: tuple[int, ...]
    total_rows: int

    @classmethod
    def build(cls, path: str) -> ParquetRowGroupIndex | None:
        try:
            metadata = pl.read_parquet_metadata(path)
        except Exception:
            return None

        groups = getattr(metadata, "row_groups", None)
        if not groups:
            return None

        rows: list[int] = []
        for group in groups:
            count = getattr(group, "num_rows", None)
            if count is None:
                count = getattr(group, "rows", None)
            if count is None:
                continue
            try:
                rows.append(max(0, int(count)))
            except (TypeError, ValueError):
                continue

        if not rows:
            return None

        offsets: list[int] = []
        running = 0
        for count in rows:
            offsets.append(running)
            running += count

        total_rows = getattr(metadata, "num_rows", None)
        if total_rows is None:
            total_rows = running
        try:
            total_rows = int(total_rows)
        except (TypeError, ValueError):
            total_rows = running

        return cls(path, tuple(rows), tuple(offsets), max(0, total_rows))

    def seek(self, row: int) -> tuple[int, int]:
        if row <= 0:
            return 0, 0
        index = bisect_right(self.row_group_offsets, row) - 1
        index = max(0, min(index, len(self.row_group_offsets) - 1))
        return index, self.row_group_offsets[index]


class ParquetRowGroupIndexer:
    def __init__(self, *, lock: RLock) -> None:
        self._lock = lock
        self._indices: dict[str, ParquetRowGroupIndex] = {}

    def get(self, path: str) -> ParquetRowGroupIndex | None:
        with self._lock:
            cached = self._indices.get(path)
        if cached is not None:
            return cached

        index = ParquetRowGroupIndex.build(path)
        if index is None:
            return None

        with self._lock:
            self._indices[path] = index
        return index

    def clear(self) -> None:
        with self._lock:
            self._indices.clear()


__all__ = ["ParquetRowGroupIndex", "ParquetRowGroupIndexer"]
