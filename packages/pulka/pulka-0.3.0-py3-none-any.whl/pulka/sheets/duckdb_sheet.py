"""DuckDB-backed sheet used for database sources."""

from __future__ import annotations

import copy
from collections.abc import Sequence
from dataclasses import replace
from typing import Any, ClassVar, cast
from uuid import uuid4

from ..core.column_insight import ColumnInsight, ColumnInsightProvider
from ..core.engine.contracts import PhysicalPlan, TableSlice
from ..core.engine.duckdb_adapter import (
    DuckDBEngineAdapter,
    DuckDBMaterializer,
    DuckDBPhysicalPlan,
    duckdb_dtype_category,
    duckdb_dtype_label,
    inspect_source_schema,
    make_physical_plan_handle,
    unwrap_physical_plan,
)
from ..core.interfaces import JobRunnerProtocol, MaterializerProtocol, is_materializer_compatible
from ..core.jobs.duckdb_column_insight_job import (
    build_duckdb_column_insight_source,
    compute_duckdb_column_insight,
)
from ..core.plan import QueryPlan, normalized_columns_key
from ..core.plan_ops import set_projection as plan_set_projection
from ..core.plan_ops import toggle_sort as plan_toggle_sort
from ..core.row_provider import RowProvider
from ..core.sheet import (
    SHEET_FEATURE_PLAN,
    SHEET_FEATURE_PREVIEW,
    SHEET_FEATURE_ROW_COUNT,
    SHEET_FEATURE_SLICE,
    SHEET_FEATURE_VALUE_AT,
    SheetFeature,
)
from ..data.db import DbSource
from ..utils import _boot_trace


class DuckDBSheet:
    """Sheet implementation wrapping a DuckDB table source."""

    hide_transforms_panel_by_default: ClassVar[bool] = True
    hide_insight_panel_by_default: ClassVar[bool] = True

    _CAPABILITIES: ClassVar[frozenset[SheetFeature]] = frozenset(
        {
            SHEET_FEATURE_PLAN,
            SHEET_FEATURE_PREVIEW,
            SHEET_FEATURE_SLICE,
            SHEET_FEATURE_VALUE_AT,
            SHEET_FEATURE_ROW_COUNT,
        }
    )

    def __init__(
        self,
        source: DbSource | PhysicalPlan,
        *,
        plan: QueryPlan | None = None,
        schema: dict[str, Any] | None = None,
        columns: Sequence[str] | None = None,
        sheet_id: str | None = None,
        generation: int | None = None,
        adapter: DuckDBEngineAdapter | None = None,
        materializer: MaterializerProtocol | None = None,
        runner: JobRunnerProtocol,
    ) -> None:
        _boot_trace("duckdb_sheet:init start")
        physical = self._coerce_physical_plan(source, schema)
        self._physical_source_handle: PhysicalPlan = make_physical_plan_handle(physical)
        if not isinstance(runner, JobRunnerProtocol):
            msg = "runner must implement JobRunnerProtocol"
            raise TypeError(msg)
        self.sheet_id = sheet_id or uuid4().hex
        self._runner = runner
        self._generation = generation or self._runner.bump_generation(self.sheet_id)

        base_schema = dict(physical.schema)
        self.schema: dict[str, Any] = dict(base_schema)
        self.columns = list(columns or base_schema.keys())

        self._adapter = adapter or DuckDBEngineAdapter(physical)
        if materializer is None:
            materializer = DuckDBMaterializer()
        elif not is_materializer_compatible(materializer):
            msg = "materializer must implement MaterializerProtocol"
            raise TypeError(msg)
        self._materializer = cast(MaterializerProtocol, materializer)

        self._plan: QueryPlan = plan or QueryPlan()
        self._row_provider = RowProvider.for_plan_source(
            engine_factory=self._compiler_factory,
            columns_getter=lambda: self.columns,
            job_context=self.job_context,
            materializer=self._materializer,
            empty_result_factory=self._empty_result,
            runner=self._runner,
            row_id_column=None,
        )
        self._cached_plan_snapshot: dict[str, Any] | None = None
        _boot_trace("duckdb_sheet:init done")

    # Public accessors -------------------------------------------------
    @property
    def plan(self) -> QueryPlan:
        return self._plan

    def with_plan(self, plan: QueryPlan) -> DuckDBSheet:
        if plan == self._plan:
            return self
        clone = copy.copy(self)
        materializer = clone._materializer
        share_fn = getattr(materializer, "share", None)
        if callable(share_fn):
            materializer = share_fn()
        clone._materializer = materializer
        clone._plan = plan
        clone._cached_plan_snapshot = None
        clone._generation = clone._runner.bump_generation(clone.sheet_id)
        config = clone.row_provider_config()
        clone._row_provider = RowProvider.for_plan_source(**config)
        return clone

    # ------------------------------------------------------------------
    # Sheet protocol helpers
    # ------------------------------------------------------------------
    def schema_dict(self) -> dict[str, Any]:
        return dict(self.schema)

    def _column_signature(self) -> str:
        return normalized_columns_key(self.columns)

    def physical_plan(self) -> PhysicalPlan:
        return self._physical_source_handle

    def plan_snapshot(self) -> dict[str, Any]:
        if self._cached_plan_snapshot is None:
            self._cached_plan_snapshot = self._plan.snapshot()
        return dict(self._cached_plan_snapshot)

    # ------------------------------------------------------------------
    # Core protocol
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        plan = self._adapter.compile(self._plan)
        count = self._materializer.count(plan)
        if count is None:
            return 0
        return int(count)

    def fetch_slice(self, row_start: int, row_count: int, columns: Sequence[str]) -> TableSlice:
        slice_, _status = self.row_provider.get_slice(
            self._plan,
            columns,
            row_start,
            row_count,
        )
        return slice_

    def get_value_at(self, row_index: int, column_name: str | None = None) -> object:
        if row_index < 0:
            raise IndexError("row index must be non-negative")

        available = self.columns
        if not available:
            raise IndexError("sheet has no columns")

        target_column = column_name or available[0]
        if target_column not in available:
            raise KeyError(f"unknown column: {target_column}")

        base_plan = self._plan
        projection = base_plan.projection
        if not projection:
            projection = (target_column,)
            for column, _ in base_plan.sort:
                if column in available and column not in projection:
                    projection = (*projection, column)
        plan_for_value = replace(base_plan, projection=tuple(projection))

        table_slice, _status = self.row_provider.get_slice(
            plan_for_value,
            [target_column],
            row_index,
            1,
        )
        if table_slice.height == 0:
            raise IndexError("row index out of range")
        column = table_slice.column(target_column)
        if not column.values:
            raise IndexError("row index out of range")
        return column.values[0]

    def snapshot_transforms(self) -> QueryPlan:
        return self._plan

    def restore_transforms(self, snapshot: QueryPlan) -> None:
        if isinstance(snapshot, QueryPlan):
            self._update_plan(snapshot)

    def restore_plan(self, plan: QueryPlan) -> None:
        self.restore_transforms(plan)

    # ------------------------------------------------------------------
    # Query helpers used by the viewer layer
    # ------------------------------------------------------------------
    def preview(self, rows: int, cols: Sequence[str] | None = None) -> TableSlice:
        projection = cols if cols is not None else self._plan.projection
        plan = plan_set_projection(self._plan, projection or self.columns)
        plan = replace(plan, offset=0, limit=rows)
        compiled = self._adapter.compile(plan)
        return self._materializer.collect_slice(
            compiled,
            start=0,
            length=rows,
            columns=plan.projection_or(self.columns),
        )

    def toggle_sort(self, column: str) -> None:
        self._update_plan(plan_toggle_sort(self._plan, column))

    def value_at(self, row: int, col: str) -> object:
        return self.get_value_at(row, col)

    def row_count(self) -> int | None:
        plan = self._adapter.compile(self._plan)
        return self._materializer.count(plan)

    def column_insight_provider(self) -> ColumnInsightProvider:
        plan = self._plan
        physical = unwrap_physical_plan(self._physical_source_handle)
        schema = dict(self.schema)
        insight_source = build_duckdb_column_insight_source(physical, plan)

        def _build_job(config):
            def _job(_: int) -> ColumnInsight:
                return compute_duckdb_column_insight(
                    insight_source=insight_source,
                    config=config,
                    schema=schema,
                )

            return _job

        def _supports_histogram(column: str) -> bool:
            dtype = schema.get(column)
            try:
                return duckdb_dtype_category(dtype) in {"numeric", "temporal"}
            except Exception:
                return False

        def _dtype_for_column(column: str) -> str | None:
            dtype = schema.get(column)
            try:
                return duckdb_dtype_label(dtype)
            except Exception:
                return None

        return ColumnInsightProvider(
            build_job=_build_job,
            supports_histogram=_supports_histogram,
            dtype_for_column=_dtype_for_column,
        )

    def supports(self, feature: SheetFeature, /) -> bool:
        return feature in self._CAPABILITIES

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------
    def close(self) -> None:
        """Release any shared materializer resources."""

        close_fn = getattr(self._materializer, "close", None)
        if callable(close_fn):
            close_fn()

    # ------------------------------------------------------------------
    # Viewer/job helpers
    # ------------------------------------------------------------------
    @property
    def job_runner(self) -> JobRunnerProtocol:
        return self._runner

    @property
    def row_provider(self) -> RowProvider:
        return self._row_provider

    def row_provider_config(self) -> dict[str, Any]:
        return {
            "engine_factory": self._compiler_factory,
            "columns_getter": lambda: self.columns,
            "materializer": self._materializer,
            "job_context": self.job_context,
            "empty_result_factory": self._empty_result,
            "runner": self._runner,
            "row_id_column": None,
        }

    def job_context(self) -> tuple[str, int, str]:
        snapshot = self.plan_snapshot()
        return (self.sheet_id, self._generation, snapshot["hash"])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _update_plan(self, plan: QueryPlan) -> None:
        if plan == self._plan:
            return
        self._plan = plan
        self._cached_plan_snapshot = None
        self._generation = self._runner.bump_generation(self.sheet_id)
        self._row_provider.clear()

    def _compiler_factory(self) -> DuckDBEngineAdapter:
        return self._adapter

    def _empty_result(self) -> TableSlice:
        return TableSlice.empty(self.columns, self.schema)

    def _coerce_physical_plan(
        self, source: DbSource | DuckDBPhysicalPlan | PhysicalPlan, schema: dict[str, Any] | None
    ) -> DuckDBPhysicalPlan:
        if isinstance(source, DbSource):
            table_schema = schema or inspect_source_schema(
                scheme=source.scheme,
                connection_uri=source.connection_uri,
                table=source.table,
            )
            return DuckDBPhysicalPlan(
                scheme=source.scheme,
                connection_uri=source.connection_uri,
                table=source.table,
                schema=table_schema,
            )
        if isinstance(source, DuckDBPhysicalPlan):
            return source
        handle = source
        try:
            return unwrap_physical_plan(handle)
        except Exception as exc:
            msg = "Unsupported source type for DuckDBSheet"
            raise TypeError(msg) from exc


__all__ = ["DuckDBSheet"]
