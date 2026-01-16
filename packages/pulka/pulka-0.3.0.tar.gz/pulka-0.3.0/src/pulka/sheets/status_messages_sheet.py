"""Sheet implementation exposing status message history."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import ClassVar

import polars as pl

from ..core.interfaces import JobRunnerProtocol
from ..core.plan import QueryPlan
from ..core.sheet import Sheet
from .data_sheet import DataSheet


class StatusMessagesSheet(DataSheet):
    """Read-only sheet listing status messages captured in the current session."""

    _COLUMNS: ClassVar[tuple[str, ...]] = (
        "timestamp",
        "elapsed",
        "severity",
        "source",
        "message",
        "sheet_id",
        "sheet_type",
        "stack_depth",
    )
    _SCHEMA: ClassVar[dict[str, pl.DataType]] = {
        "timestamp": pl.Utf8,
        "elapsed": pl.Utf8,
        "severity": pl.Utf8,
        "source": pl.Utf8,
        "message": pl.Utf8,
        "sheet_id": pl.Utf8,
        "sheet_type": pl.Utf8,
        "stack_depth": pl.Int64,
    }

    def __init__(
        self,
        base_sheet: Sheet,
        *,
        records: Sequence[Mapping[str, object]],
        runner: JobRunnerProtocol,
    ) -> None:
        self.base_sheet = base_sheet
        self.is_insight_soft_disabled = True
        df = self._build_dataframe(records)
        super().__init__(df.lazy(), columns=list(self._COLUMNS), runner=runner)
        self.source_sheet = self

    def _build_dataframe(self, records: Sequence[Mapping[str, object]]) -> pl.DataFrame:
        rows: list[dict[str, object]] = []
        for record in reversed(records):
            rows.append({col: record.get(col) for col in self._COLUMNS})

        if not rows:
            return pl.DataFrame(
                {col: pl.Series(col, [], dtype=self._SCHEMA[col]) for col in self._COLUMNS}
            )
        return pl.DataFrame(rows, schema=self._SCHEMA)

    def with_plan(self, plan: QueryPlan) -> StatusMessagesSheet:
        if plan == self.plan:
            return self
        sheet = self.__class__.__new__(self.__class__)
        DataSheet.__init__(
            sheet,
            self._physical_source_handle,
            plan=plan,
            schema=self.schema,
            columns=self.columns,
            sheet_id=self.sheet_id,
            generation=self._runner.bump_generation(self.sheet_id),
            compiler=self._compiler,
            materializer=self._materializer,
            runner=self._runner,
        )
        sheet.base_sheet = self.base_sheet
        sheet.is_insight_soft_disabled = True
        sheet.source_sheet = sheet
        return sheet


__all__ = ["StatusMessagesSheet"]
