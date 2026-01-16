"""Shared types for the row provider pipeline."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .engine.contracts import TableSlice
from .plan import QueryPlan

RowKey = tuple[str | None, int, int, str]


class SliceStatus(Enum):
    """Describe how closely a slice matches the requested schema."""

    OK = "ok"
    PARTIAL = "partial"
    SCHEMA_MISMATCH = "schema_mismatch"


@dataclass(slots=True, frozen=True)
class SliceStreamRequest:
    """Parameters for streaming a table slice."""

    plan: QueryPlan | None
    columns: Sequence[str]
    start: int
    count: int
    batch_rows: int | None = None
    streaming_enabled: bool | None = None
    telemetry: dict[str, Any] | None = None


@dataclass(slots=True)
class TableSliceChunk:
    """Chunk of a streaming slice, enriched with telemetry."""

    offset: int
    slice: TableSlice
    status: SliceStatus
    is_final: bool
    telemetry: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlanContext:
    plan: QueryPlan
    fetch_columns: tuple[str, ...]
    requested_columns: tuple[str, ...]
    missing_columns: tuple[str, ...]
    plan_hash: str | None
    sheet_id: str | None
    generation: int | None


__all__ = [
    "PlanContext",
    "RowKey",
    "SliceStatus",
    "SliceStreamRequest",
    "TableSliceChunk",
]
