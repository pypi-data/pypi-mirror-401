"""Histogram sheet implementation for numeric columns."""

from __future__ import annotations

import contextlib
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar

import polars as pl

from ..core.engine.contracts import EnginePayloadHandle, TableColumn, TableSlice
from ..core.engine.duckdb_adapter import (
    DuckDBPhysicalPlan,
    compile_duckdb_plan_sql,
    duckdb_dtype_category,
    execute_duckdb_query,
    quote_duckdb_identifier,
)
from ..core.engine.duckdb_adapter import (
    unwrap_physical_plan as unwrap_duckdb_physical_plan,
)
from ..core.engine.polars_adapter import (
    collect_lazyframe,
    table_slice_from_dataframe,
    unwrap_lazyframe_handle,
)
from ..core.formatting import (
    _format_float_two_decimals,
    _format_number_with_thousands_separator,
    _is_float_like,
    _is_temporal_dtype,
)
from ..core.interfaces import JobRunnerProtocol
from ..core.plan import QueryPlan
from ..core.sheet import (
    SHEET_FEATURE_SLICE,
    SHEET_FEATURE_VALUE_AT,
    Sheet,
    SheetFeature,
)
from ..render.braille import FILL_CHAR, SPROUT_CHAR, render_hist_bar


def _fit_text(text: str, width: int) -> str:
    """Left-justify text within a fixed width, adding ellipsis when needed."""

    if width <= 0:
        return ""
    if len(text) <= width:
        return text.ljust(width)
    if width == 1:
        return text[:1]
    return text[: width - 1] + "…"


@dataclass(frozen=True)
class HistogramStats:
    """Summary statistics required for histogram rendering."""

    n: int
    nulls: int
    minimum: float | None
    q1: float | None
    median: float | None
    q3: float | None
    maximum: float | None


def _format_edge(value: float | None, *, formatter: callable[[float], str]) -> str:
    """Format a histogram bucket edge using a provided formatter."""

    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "NA"
    return formatter(value)


def _duckdb_source_for_sheet(
    sheet: Sheet,
) -> tuple[DuckDBPhysicalPlan, str, tuple[Any, ...]] | None:
    physical_plan = getattr(sheet, "physical_plan", None)
    if not callable(physical_plan):
        return None
    try:
        physical_handle = physical_plan()
    except Exception:
        return None
    try:
        physical = unwrap_duckdb_physical_plan(physical_handle)
    except Exception:
        return None
    plan = getattr(sheet, "plan", None)
    if plan is None:
        plan = QueryPlan()
    try:
        sql, params = compile_duckdb_plan_sql(plan, physical)
    except Exception:
        return None
    return physical, sql, params


def _row_to_dict(row: Sequence[Any], schema: Mapping[str, Any]) -> dict[str, Any]:
    columns = list(schema.keys())
    payload: dict[str, Any] = {}
    for idx, name in enumerate(columns):
        payload[name] = row[idx] if idx < len(row) else None
    return payload


def _duckdb_histogram_stats(
    physical: DuckDBPhysicalPlan,
    base_sql: str,
    params: Sequence[Any],
    column: str,
) -> dict[str, Any]:
    quoted = quote_duckdb_identifier(column)
    base = f"({base_sql}) AS pulka_base"
    query = (
        "SELECT "
        "COUNT(*) AS row_count, "
        f"SUM(CASE WHEN {quoted} IS NULL THEN 1 ELSE 0 END) AS null_count, "
        f"SUM(CASE WHEN {quoted} IS NOT NULL THEN 1 ELSE 0 END) AS non_null_count, "
        f"COUNT(DISTINCT {quoted}) AS distinct_count, "
        f"MIN({quoted}) AS min, "
        f"QUANTILE_CONT({quoted}, 0.25) AS q1, "
        f"MEDIAN({quoted}) AS median, "
        f"QUANTILE_CONT({quoted}, 0.75) AS q3, "
        f"MAX({quoted}) AS max "
        f"FROM {base}"
    )
    try:
        rows, schema = execute_duckdb_query(physical, query, params=params)
    except Exception:
        return {}
    if not rows:
        return {}
    return _row_to_dict(rows[0], schema)


def _duckdb_histogram_counts(
    physical: DuckDBPhysicalPlan,
    base_sql: str,
    params: Sequence[Any],
    column: str,
    *,
    min_value: float,
    bin_width: float,
    bin_count: int,
) -> list[int]:
    if bin_count <= 0:
        return []
    if bin_width <= 0:
        return [0 for _ in range(bin_count)]
    quoted = quote_duckdb_identifier(column)
    base = f"({base_sql}) AS pulka_base"
    bucket_expr = f"CAST(FLOOR(({quoted} - ?) / ?) AS INTEGER)"
    query = (
        "WITH buckets AS ("
        " SELECT"
        f" CASE WHEN {quoted} IS NULL THEN NULL ELSE {bucket_expr} END AS bucket"
        f" FROM {base}"
        ")"
        " SELECT"
        f" CASE WHEN bucket < 0 THEN 0 WHEN bucket >= {bin_count} THEN {bin_count - 1}"
        " ELSE bucket END AS bucket,"
        " COUNT(*) AS count"
        " FROM buckets"
        " WHERE bucket IS NOT NULL"
        " GROUP BY bucket"
        " ORDER BY bucket"
    )
    query_params = (*params, min_value, bin_width)
    try:
        rows, schema = execute_duckdb_query(physical, query, params=query_params)
    except Exception:
        return [0 for _ in range(bin_count)]
    bucket_key = None
    count_key = None
    for name in schema:
        lowered = name.lower()
        if lowered == "bucket":
            bucket_key = name
        elif lowered == "count":
            count_key = name
    if bucket_key is None:
        bucket_key = "bucket"
    if count_key is None:
        count_key = "count"
    counts = [0 for _ in range(bin_count)]
    for row in rows:
        payload = _row_to_dict(row, schema)
        bucket = payload.get(bucket_key)
        count = payload.get(count_key)
        try:
            idx = int(bucket)
        except Exception:
            continue
        try:
            count_val = int(count)
        except Exception:
            count_val = 0
        if 0 <= idx < bin_count:
            counts[idx] = count_val
    return counts


class HistogramSheet:
    """Sheet that materializes histogram buckets for a numeric column."""

    _CAPABILITIES: ClassVar[frozenset[SheetFeature]] = frozenset(
        {
            SHEET_FEATURE_SLICE,
            SHEET_FEATURE_VALUE_AT,
        }
    )

    def __init__(
        self,
        base_sheet: Sheet,
        column_name: str,
        *,
        preferred_height: int | None = None,
        preferred_width: int | None = None,
        runner: JobRunnerProtocol,
        dtype: pl.DataType | None = None,
    ) -> None:
        self.source_sheet = base_sheet
        self.source_column = column_name
        self.is_insight_soft_disabled = True
        if runner is None:  # pragma: no cover - defensive guard
            msg = "HistogramSheet requires a JobRunner instance"
            raise ValueError(msg)
        self._runner: JobRunnerProtocol = runner

        inferred_dtype = dtype
        if inferred_dtype is None:
            schema = getattr(base_sheet, "schema", None) or {}
            inferred_dtype = schema.get(column_name)
        self._dtype = inferred_dtype
        self._is_temporal = False
        if inferred_dtype is not None:
            with contextlib.suppress(Exception):
                self._is_temporal = bool(_is_temporal_dtype(inferred_dtype))

        self.filter_text: str | None = None
        self.sort_col: str | None = None
        self.sort_asc: bool = True

        self._duckdb_source: DuckDBPhysicalPlan | None = None
        self._duckdb_sql: str | None = None
        self._duckdb_params: tuple[Any, ...] = ()

        base_lf_candidate = getattr(base_sheet, "lf", None)
        if base_lf_candidate is None:
            base_lf_candidate = getattr(base_sheet, "lf0", None)
        if base_lf_candidate is None:
            duckdb_source = _duckdb_source_for_sheet(base_sheet)
            if duckdb_source is None:
                raise ValueError("Histogram view requires a lazy frame source")
            physical, sql, params = duckdb_source
            category = duckdb_dtype_category(physical.schema.get(column_name))
            if category != "numeric":
                raise ValueError("Histogram view requires a numeric column")
            self._duckdb_source = physical
            self._duckdb_sql = sql
            self._duckdb_params = tuple(params)
            base_lf = None
        elif isinstance(base_lf_candidate, EnginePayloadHandle):
            base_lf = unwrap_lazyframe_handle(base_lf_candidate)
        else:
            base_lf = base_lf_candidate

        if self._duckdb_source is None:
            assert base_lf is not None
            value_expr = (
                pl.col(column_name).cast(pl.Int64, strict=False)
                if self._is_temporal
                else pl.col(column_name)
            )

            stats_df = collect_lazyframe(
                base_lf.select(
                    [
                        pl.col(column_name).count().alias("n"),
                        pl.col(column_name)
                        .filter(pl.col(column_name).is_not_null())
                        .n_unique()
                        .alias("distinct"),
                        value_expr.min().alias("min"),
                        value_expr.quantile(0.25, interpolation="nearest").alias("q1"),
                        value_expr.median().alias("median"),
                        value_expr.quantile(0.75, interpolation="nearest").alias("q3"),
                        value_expr.max().alias("max"),
                        pl.col(column_name).is_null().sum().alias("nulls"),
                    ]
                )
            )

            if stats_df.is_empty():
                n = 0
                distinct = 0
                minimum = q1 = median = q3 = maximum = None
                nulls = 0
            else:
                row = stats_df.row(0, named=True)
                n = int(row.get("n", 0) or 0)
                distinct = row.get("distinct")
                minimum = row.get("min")
                q1 = row.get("q1")
                median = row.get("median")
                q3 = row.get("q3")
                maximum = row.get("max")
                nulls = int(row.get("nulls", 0) or 0)

            # Keep a clean column for statistics + binning
            cast_expr = (
                value_expr.cast(pl.Int64, strict=False)
                if self._is_temporal
                else value_expr.cast(pl.Float64, strict=False)
            )
            self._clean_lf = (
                base_lf.select(cast_expr.alias("__value"))
                .drop_nulls()
                .rename({"__value": column_name})
            )
        else:
            stats_row = _duckdb_histogram_stats(
                self._duckdb_source,
                self._duckdb_sql or "",
                self._duckdb_params,
                column_name,
            )
            n = int(stats_row.get("row_count", 0) or 0) if stats_row else 0
            distinct = stats_row.get("distinct_count")
            minimum = stats_row.get("min")
            q1 = stats_row.get("q1")
            median = stats_row.get("median")
            q3 = stats_row.get("q3")
            maximum = stats_row.get("max")
            nulls = int(stats_row.get("null_count", 0) or 0) if stats_row else 0
            self._clean_lf = None

        self.distinct_count = int(distinct or 0) if n else 0

        def _coerce_stat(value: float | int | None) -> float | int | None:
            if value is None:
                return None
            return int(value) if self._is_temporal else float(value)

        self.stats = HistogramStats(
            n=n,
            nulls=nulls,
            minimum=_coerce_stat(minimum),
            q1=_coerce_stat(q1),
            median=_coerce_stat(median),
            q3=_coerce_stat(q3),
            maximum=_coerce_stat(maximum),
        )

        self._value_range = (
            0.0
            if self.stats.minimum is None or self.stats.maximum is None
            else float(self.stats.maximum - self.stats.minimum)
        )
        self._edge_formatter = self._build_edge_formatter()

        self.log_scale = False
        self._preferred_height = (
            max(1, int(preferred_height)) if preferred_height is not None else None
        )
        self._preferred_width = (
            max(20, int(preferred_width)) if preferred_width is not None else None
        )

        self.columns = ["from", "to", "hist", "count"]
        self.schema = {
            "from": pl.Utf8,
            "to": pl.Utf8,
            "hist": pl.Utf8,
            "count": pl.Int64,
        }

        self._bin_edges: list[float] = []
        self._counts: list[int] = []
        self._max_count: int = 0
        self._bucket_left_labels: list[str] = []
        self._bucket_right_labels: list[str] = []
        self._display_df: pl.DataFrame = pl.DataFrame(
            {col: pl.Series(col, [], dtype=self.schema[col]) for col in self.columns}
        )
        self._export_df: pl.DataFrame = pl.DataFrame(
            {
                "bin_left": pl.Series("bin_left", [], dtype=pl.Float64),
                "bin_right": pl.Series("bin_right", [], dtype=pl.Float64),
                "count": pl.Series("count", [], dtype=pl.Int64),
            }
        )

        self._column_widths: dict[str, int] = {col: max(4, len(col)) for col in self.columns}
        self._view_width_override = self._preferred_width
        self.lf0 = self._display_df.lazy()
        self.lf = self.lf0

        self.bin_count = self._initial_bin_count()
        self._recompute_table()

    @property
    def job_runner(self) -> JobRunnerProtocol:
        return self._runner

    # Sheet protocol -----------------------------------------------------
    def __len__(self) -> int:  # pragma: no cover - simple delegation
        return int(self._display_df.height)

    def fetch_slice(self, row_start: int, row_count: int, columns: Sequence[str]) -> TableSlice:
        if row_start < 0 or row_count < 0:
            raise ValueError("row_start and row_count must be non-negative")
        available = [col for col in columns if col in self.columns]
        if not available:
            return TableSlice.empty(columns, self.schema)
        sliced = self._display_df.select(available).slice(row_start, row_count)
        table_slice = table_slice_from_dataframe(sliced, sliced.schema)
        if "hist" in available:
            table_slice = self._with_hist_display(table_slice, sliced, available)
        return table_slice

    def _with_hist_display(
        self,
        table_slice: TableSlice,
        sliced_df: pl.DataFrame,
        visible_columns: Sequence[str],
    ) -> TableSlice:
        """Attach a width-aware display function for histogram bars."""

        try:
            hist_idx = list(visible_columns).index("hist")
        except ValueError:
            return table_slice

        if "count" in sliced_df.columns:
            try:
                counts = sliced_df.get_column("count").to_list()
            except Exception:
                counts = [0 for _ in range(len(sliced_df))]
        else:
            counts = [0 for _ in range(len(sliced_df))]

        max_count = self._max_count if self._max_count else max(counts or [0])
        hist_series = sliced_df.get_column("hist")
        dtype = hist_series.dtype
        null_count = int(hist_series.null_count())

        def _display_hist(row: int, _abs_row: int, _value: object, width: int | None) -> str:
            target_width = 0 if width is None else max(0, int(width))
            count_val = counts[row] if 0 <= row < len(counts) else 0
            return render_hist_bar(count_val, max_count, target_width)

        columns = list(table_slice.columns)
        columns[hist_idx] = TableColumn("hist", hist_series, dtype, null_count, _display_hist)
        return TableSlice(
            tuple(columns),
            table_slice.schema,
            table_slice.start_offset,
            table_slice.row_ids,
        )

    def get_value_at(self, row_index: int, column_name: str | None = None) -> object:
        if row_index < 0 or row_index >= len(self):
            raise IndexError("row index out of range")
        column = column_name or self.columns[0]
        if column not in self.columns:
            raise KeyError(f"unknown column: {column}")
        return self._display_df[column][row_index]

    def supports(self, feature: SheetFeature, /) -> bool:
        return feature in self._CAPABILITIES

    def get_column_widths(self) -> dict[str, int]:
        """Expose the current column width allocation used for rendering."""

        return dict(self._column_widths)

    def preferred_fill_column(self) -> str | None:  # pragma: no cover - simple hint
        return "hist"

    # Histogram specific helpers ----------------------------------------
    @property
    def counts(self) -> list[int]:
        return list(self._counts)

    def bucket_left_labels(self) -> list[str]:
        return list(self._bucket_left_labels)

    @property
    def bucket_right_labels(self) -> list[str]:
        return list(self._bucket_right_labels)

    def adjust_bins(self, delta: int) -> bool:
        if not self._counts or self._value_range == 0:
            return False
        target = self.bin_count + delta
        target = self._clamp_bins(target, allow_single=True)
        if target == self.bin_count:
            return False
        self.bin_count = target
        self._recompute_table()
        return True

    def toggle_log_scale(self) -> None:
        self.log_scale = not self.log_scale
        self._refresh_display_table()

    def export_bins(self) -> pl.DataFrame:
        return self._export_df.clone()

    def update_layout_for_view(
        self,
        *,
        view_width: int | None = None,
        view_height: int | None = None,
        viewer: object | None = None,
    ) -> None:
        """Refresh the rendered histogram layout for the active viewport."""

        height_changed = False
        if view_height is not None:
            with contextlib.suppress(Exception):  # pragma: no cover - defensive
                next_height = max(1, int(view_height))
                if viewer is not None and hasattr(viewer, "_body_view_height"):
                    body_height = viewer._body_view_height()
                    if isinstance(body_height, int):
                        next_height = max(1, body_height)
                if next_height != self._preferred_height:
                    self._preferred_height = next_height
                    height_changed = True

        width_changed = False
        width_candidate: int | None = None
        if view_width is not None:
            with contextlib.suppress(Exception):  # pragma: no cover - defensive
                width_candidate = max(20, int(view_width))
        if width_candidate is not None and width_candidate != self._view_width_override:
            self._view_width_override = width_candidate
            width_changed = True

        if height_changed:
            target_bins = self._initial_bin_count()
            if target_bins != self.bin_count:
                self.bin_count = target_bins
                self._recompute_table()
            elif width_changed:
                self._refresh_display_table()
        elif width_changed:
            self._refresh_display_table()

        if (
            (height_changed or width_changed)
            and viewer is not None
            and hasattr(viewer, "invalidate_row_cache")
        ):
            with contextlib.suppress(Exception):  # pragma: no cover - defensive
                viewer.invalidate_row_cache()

        if viewer is not None and hasattr(viewer, "__dict__"):
            total_rows: int | None = None
            with contextlib.suppress(Exception):  # pragma: no cover - defensive
                total_rows = len(self)
            if total_rows is not None:
                with contextlib.suppress(Exception):  # pragma: no cover - defensive
                    viewer._total_rows = int(total_rows)
                    viewer._row_count_stale = False
                    if hasattr(viewer, "clamp") and callable(viewer.clamp):
                        viewer.clamp()

    def status_text(self) -> str:
        parts: list[str] = []
        parts.append(self.source_column)
        parts.append(f"n={self.stats.n}")
        parts.append(f"nulls={self.stats.nulls}")
        parts.append(f"min={_format_edge(self.stats.minimum, formatter=self._edge_formatter)}")
        parts.append(f"q1={_format_edge(self.stats.q1, formatter=self._edge_formatter)}")
        parts.append(f"median={_format_edge(self.stats.median, formatter=self._edge_formatter)}")
        parts.append(f"q3={_format_edge(self.stats.q3, formatter=self._edge_formatter)}")
        parts.append(f"max={_format_edge(self.stats.maximum, formatter=self._edge_formatter)}")
        parts.append(f"bins={self.bin_count}")
        parts.append(f"log={'on' if self.log_scale else 'off'}")
        return " \u00b7 ".join(parts)

    # Internal helpers ---------------------------------------------------
    def _initial_bin_count(self) -> int:
        if self.stats.n <= 0 or self.stats.minimum is None or self.stats.maximum is None:
            return 0

        if self.stats.maximum == self.stats.minimum:
            return 1

        if self.stats.n < 2:
            return self._clamp_bins(self._sturges(self.stats.n), allow_single=True)

        q1 = self.stats.q1
        q3 = self.stats.q3
        iqr = None
        if q1 is not None and q3 is not None:
            iqr = q3 - q1
        if iqr is None or not math.isfinite(iqr):
            iqr = 0.0

        if iqr <= 0:
            return self._clamp_bins(self._sturges(self.stats.n), allow_single=True)

        width = 2 * iqr / (self.stats.n ** (1 / 3))
        if not math.isfinite(width) or width <= 0:
            return self._clamp_bins(self._sturges(self.stats.n), allow_single=True)

        approx = int(math.ceil(self._value_range / width))
        if approx < 1:
            return self._clamp_bins(self._sturges(self.stats.n), allow_single=True)

        return self._clamp_bins(approx, allow_single=True)

    @staticmethod
    def _sturges(n: int) -> int:
        if n <= 0:
            return 1
        return 1 + math.ceil(math.log2(n))

    def _clamp_bins(self, bins: int, *, allow_single: bool) -> int:
        bins = int(math.ceil(bins))
        if bins < 1:
            bins = 1

        minimum = 1 if allow_single else 4
        view_cap: int | None = None
        if self._preferred_height is not None:
            view_cap = max(1, min(100, self._preferred_height))
            if view_cap < minimum:
                minimum = view_cap if allow_single else max(1, view_cap)

        distinct_cap: int | None = None
        if getattr(self, "distinct_count", 0) > 0:
            distinct_cap = max(1, min(100, self.distinct_count))
            bins = min(bins, distinct_cap)
            if distinct_cap < minimum:
                minimum = distinct_cap if allow_single else max(1, distinct_cap)

        if bins < minimum:
            bins = minimum
        bins = min(100, bins)

        if view_cap is not None:
            bins = min(bins, view_cap)

        if distinct_cap is not None:
            bins = min(bins, distinct_cap)

        return bins

    def _recompute_table(self) -> None:
        if self._duckdb_source is not None:
            self._recompute_table_duckdb()
            return
        if self.stats.n <= 0 or self.stats.minimum is None or self.stats.maximum is None:
            self._counts = []
            self._max_count = 0
            self._bin_edges = []
            self._bucket_left_labels = []
            self._bucket_right_labels = []
            self._export_df = pl.DataFrame(
                {
                    "bin_left": pl.Series("bin_left", [], dtype=pl.Float64),
                    "bin_right": pl.Series("bin_right", [], dtype=pl.Float64),
                    "count": pl.Series("count", [], dtype=pl.Int64),
                }
            )
            self._refresh_display_table()
            return

        if self.stats.maximum == self.stats.minimum:
            counts = [self.stats.n]
            edges = [self.stats.minimum, self.stats.maximum]
        elif self._is_temporal:
            min_value = int(self.stats.minimum)
            max_value = int(self.stats.maximum)
            value_range = max_value - min_value
            effective_bins = max(1, min(self.bin_count, value_range + 1))
            width = max(1, math.ceil(value_range / effective_bins))

            edges: list[int] = [min_value]
            while edges[-1] < max_value:
                next_edge = edges[-1] + width
                if next_edge >= max_value:
                    edges.append(max_value)
                    break
                edges.append(next_edge)
            bin_count = max(1, len(edges) - 1)

            bin_expr = (pl.col(self.source_column).cast(pl.Int64) - min_value) // width
            grouped = collect_lazyframe(
                self._clean_lf.with_columns(
                    pl.when(bin_expr < 0)
                    .then(0)
                    .when(bin_expr >= bin_count)
                    .then(bin_count - 1)
                    .otherwise(bin_expr)
                    .cast(pl.Int64)
                    .alias("__bin")
                )
                .group_by("__bin")
                .agg(pl.len().alias("count"))
            )

            counts = [0] * bin_count
            for bin_index, count in grouped.iter_rows():
                idx = int(bin_index)
                if 0 <= idx < bin_count:
                    counts[idx] = int(count)
        else:
            width = self._value_range / self.bin_count
            edges = [self.stats.minimum + i * width for i in range(self.bin_count)]
            edges.append(self.stats.maximum)

            bin_expr = ((pl.col(self.source_column) - self.stats.minimum) / width).floor()
            grouped = collect_lazyframe(
                self._clean_lf.with_columns(
                    pl.when(bin_expr < 0)
                    .then(0)
                    .when(bin_expr >= self.bin_count)
                    .then(self.bin_count - 1)
                    .otherwise(bin_expr)
                    .cast(pl.Int64)
                    .alias("__bin")
                )
                .group_by("__bin")
                .agg(pl.len().alias("count"))
            )

            counts = [0] * self.bin_count
            for bin_index, count in grouped.iter_rows():
                idx = int(bin_index)
                if 0 <= idx < self.bin_count:
                    counts[idx] = int(count)

        bin_left = edges[:-1]
        bin_right = edges[1:]
        self.bin_count = len(counts)
        self._counts = counts
        self._max_count = max(counts) if counts else 0
        self._bin_edges = [float(x) for x in edges]
        left_labels: list[str] = []
        right_labels: list[str] = []
        for idx, left in enumerate(bin_left):
            right = bin_right[idx]
            left_txt = _format_edge(left, formatter=self._edge_formatter)
            right_txt = _format_edge(right, formatter=self._edge_formatter)
            closing = "]" if idx == len(bin_left) - 1 else ")"
            left_labels.append(f"[{left_txt}")
            right_labels.append(f"{right_txt}{closing}")
        self._bucket_left_labels = left_labels
        self._bucket_right_labels = right_labels

        self._export_df = pl.DataFrame(
            {
                "bin_left": pl.Series("bin_left", bin_left, dtype=pl.Float64),
                "bin_right": pl.Series("bin_right", bin_right, dtype=pl.Float64),
                "count": counts,
            }
        )
        self._refresh_display_table()

    def _recompute_table_duckdb(self) -> None:
        if self.stats.n <= 0 or self.stats.minimum is None or self.stats.maximum is None:
            self._counts = []
            self._max_count = 0
            self._bin_edges = []
            self._bucket_left_labels = []
            self._bucket_right_labels = []
            self._export_df = pl.DataFrame(
                {
                    "bin_left": pl.Series("bin_left", [], dtype=pl.Float64),
                    "bin_right": pl.Series("bin_right", [], dtype=pl.Float64),
                    "count": pl.Series("count", [], dtype=pl.Int64),
                }
            )
            self._refresh_display_table()
            return

        if self.stats.maximum == self.stats.minimum:
            counts = [self.stats.n]
            edges = [self.stats.minimum, self.stats.maximum]
        else:
            width = self._value_range / self.bin_count
            edges = [self.stats.minimum + i * width for i in range(self.bin_count)]
            edges.append(self.stats.maximum)
            counts = _duckdb_histogram_counts(
                self._duckdb_source,
                self._duckdb_sql or "",
                self._duckdb_params,
                self.source_column,
                min_value=float(self.stats.minimum),
                bin_width=float(width),
                bin_count=self.bin_count,
            )

        bin_left = edges[:-1]
        bin_right = edges[1:]
        self.bin_count = len(counts)
        self._counts = counts
        self._max_count = max(counts) if counts else 0
        self._bin_edges = [float(x) for x in edges]
        left_labels: list[str] = []
        right_labels: list[str] = []
        for idx, left in enumerate(bin_left):
            right = bin_right[idx]
            left_txt = _format_edge(left, formatter=self._edge_formatter)
            right_txt = _format_edge(right, formatter=self._edge_formatter)
            closing = "]" if idx == len(bin_left) - 1 else ")"
            left_labels.append(f"[{left_txt}")
            right_labels.append(f"{right_txt}{closing}")
        self._bucket_left_labels = left_labels
        self._bucket_right_labels = right_labels

        self._export_df = pl.DataFrame(
            {
                "bin_left": pl.Series("bin_left", bin_left, dtype=pl.Float64),
                "bin_right": pl.Series("bin_right", bin_right, dtype=pl.Float64),
                "count": counts,
            }
        )
        self._refresh_display_table()

    def _refresh_display_table(self) -> None:
        view_width = max(20, self._view_width_override or 80)

        if not self._counts:
            self._set_display_df(
                {col: pl.Series(col, [], dtype=self.schema[col]) for col in self.columns}
            )
            self._column_widths = {col: max(len(col) + 4, 6) for col in self.columns}
            return

        widths, inner_widths = self._compute_column_widths(view_width)
        self._column_widths = widths

        left_inner = inner_widths["from"]
        right_inner = inner_widths["to"]
        hist_inner = inner_widths["hist"]

        if self.log_scale:
            scaled = [math.log1p(count) for count in self._counts]
            max_scaled = max(scaled) if scaled else 0.0
            scale_denominator = max_scaled if max_scaled > 0 else 1.0
        else:
            scaled = [float(count) for count in self._counts]
            max_count = max(scaled) if scaled else 0.0
            scale_denominator = max_count if max_count > 0 else 1.0

        hist_strings: list[str] = []
        left_texts: list[str] = []
        right_texts: list[str] = []

        for idx, count in enumerate(self._counts):
            left_label = self._bucket_left_labels[idx]
            right_label = self._bucket_right_labels[idx]
            left_texts.append(_fit_text(left_label, left_inner))
            right_texts.append(_fit_text(right_label, right_inner))

            if hist_inner <= 0:
                hist_strings.append("")
                continue

            raw_value = scaled[idx]
            fraction = raw_value / scale_denominator if scale_denominator > 0 else 0.0
            bar_len = int(round(fraction * hist_inner))
            bar_len = max(0, min(hist_inner, bar_len))

            if count > 0 and bar_len == 0:
                bar = (SPROUT_CHAR + (" " * (hist_inner - 1)))[:hist_inner]
            else:
                filled = FILL_CHAR * bar_len
                padding = " " * max(0, hist_inner - bar_len)
                bar = (filled + padding)[:hist_inner]

            hist_strings.append(bar)

        display_data = {
            "from": left_texts,
            "to": right_texts,
            "hist": [s.ljust(hist_inner) if hist_inner > 0 else s for s in hist_strings],
            "count": self._counts,
        }

        self._set_display_df(display_data)

    def _build_edge_formatter(self) -> callable[[float], str]:
        if not self._is_temporal or self._dtype is None:
            return self._format_numeric_edge

        def _format_temporal_edge(value: float) -> str:
            try:
                series = pl.Series([value]).cast(self._dtype, strict=False)
                return str(series[0])
            except Exception:
                return self._format_numeric_edge(value)

        return _format_temporal_edge

    @staticmethod
    def _format_numeric_edge(value: float) -> str:
        if _is_float_like(value):
            try:
                numeric = float(value)
            except Exception:
                return str(value)
            if math.isnan(numeric):
                return "NaN"
            if math.isinf(numeric):
                return "inf" if numeric > 0 else "-inf"
            return _format_float_two_decimals(numeric)
        return str(value)

    def _compute_column_widths(self, view_width: int) -> tuple[dict[str, int], dict[str, int]]:
        column_count = len(self.columns)
        pad = 1
        border_overhead = column_count + 1

        left_labels = self._bucket_left_labels
        right_labels = self._bucket_right_labels

        desired_left_inner = (
            max([len("from")] + [len(label) for label in left_labels])
            if left_labels
            else len("from")
        )
        desired_right_inner = (
            max([len("to")] + [len(label) for label in right_labels]) if right_labels else len("to")
        )
        count_texts = [_format_number_with_thousands_separator(count) for count in self._counts]
        desired_count_inner = (
            max([len("count")] + [len(text) for text in count_texts])
            if count_texts
            else len("count")
        )

        left_min = 2
        right_min = 2
        hist_min = 2
        count_min = 1

        available_inner = view_width - border_overhead - (2 * pad * column_count)
        available_inner = max(
            left_min + right_min + hist_min + count_min,
            available_inner,
        )

        left_cap = max(left_min, available_inner // 6)
        if desired_left_inner < left_cap:
            left_cap = desired_left_inner
        left_inner = min(
            left_cap,
            available_inner - (right_min + hist_min + count_min),
        )
        left_inner = max(left_min, left_inner)

        remaining_for_right = available_inner - (left_inner + hist_min + count_min)
        right_cap = max(right_min, available_inner // 6)
        if desired_right_inner < right_cap:
            right_cap = desired_right_inner
        right_inner = min(right_cap, remaining_for_right)
        right_inner = max(right_min, right_inner)

        count_inner = min(
            desired_count_inner,
            available_inner - (left_inner + right_inner + hist_min),
        )
        count_inner = max(count_min, count_inner)

        hist_inner = available_inner - left_inner - right_inner - count_inner

        if hist_inner < hist_min:
            deficit = hist_min - hist_inner

            reducible_count = max(0, count_inner - count_min)
            reduce_count = min(deficit, reducible_count)
            count_inner -= reduce_count
            deficit -= reduce_count

            reducible_right = max(0, right_inner - right_min)
            reduce_right = min(deficit, reducible_right)
            right_inner -= reduce_right
            deficit -= reduce_right

            reducible_left = max(0, left_inner - left_min)
            reduce_left = min(deficit, reducible_left)
            left_inner -= reduce_left
            deficit -= reduce_left

            hist_inner = available_inner - left_inner - right_inner - count_inner

        hist_inner = max(hist_min, hist_inner)

        inner_widths = {
            "from": left_inner,
            "to": right_inner,
            "hist": hist_inner,
            "count": count_inner,
        }

        widths = {col: max(inner + 2 * pad, 4) for col, inner in inner_widths.items()}
        return widths, inner_widths

    def _set_display_df(self, data: Mapping[str, Sequence[object] | pl.Series]) -> None:
        self._display_df = pl.DataFrame(data)
        self.lf0 = self._display_df.lazy()
        self.lf = self.lf0
        self.schema = self._display_df.schema
        self.columns = list(self._display_df.columns)
