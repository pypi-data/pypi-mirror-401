"""DuckDB-backed column insight job helpers."""

from __future__ import annotations

import contextlib
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import timedelta
from time import perf_counter_ns
from typing import Any

from ..column_insight import (
    LOW_CARDINALITY_NUMERIC_LIMIT,
    ColumnInsight,
    InsightHistogram,
    TopValue,
    summarize_value_preview,
)
from ..engine.duckdb_adapter import (
    DuckDBPhysicalPlan,
    compile_duckdb_plan_sql,
    duckdb_dtype_category,
    duckdb_dtype_label,
    execute_duckdb_query,
    quote_duckdb_identifier,
)
from ..plan import QueryPlan
from .column_insight_job import ColumnInsightJobConfig

_HISTOGRAM_BIN_COUNT = 48


@dataclass(frozen=True, slots=True)
class DuckDBColumnInsightSource:
    source: DuckDBPhysicalPlan
    sql: str
    params: tuple[Any, ...]


def build_duckdb_column_insight_source(
    source: DuckDBPhysicalPlan,
    plan: QueryPlan,
) -> DuckDBColumnInsightSource:
    sql, params = compile_duckdb_plan_sql(plan, source)
    return DuckDBColumnInsightSource(source=source, sql=sql, params=params)


def compute_duckdb_column_insight(
    *,
    insight_source: DuckDBColumnInsightSource,
    config: ColumnInsightJobConfig,
    schema: Mapping[str, Any] | None = None,
) -> ColumnInsight:
    """Compute column insight data using DuckDB SQL."""

    start_ns = perf_counter_ns()
    column_name = config.column_name
    if schema is not None and column_name not in schema:
        duration = perf_counter_ns() - start_ns
        return ColumnInsight(
            config.sheet_id,
            config.plan_hash,
            column_name,
            None,
            None,
            None,
            None,
            None,
            None,
            {},
            (),
            None,
            source_path=config.source_path,
            duration_ns=duration,
            error=f"unknown column: {column_name}",
        )

    dtype = schema.get(column_name) if schema is not None else None
    dtype_label = duckdb_dtype_label(dtype)
    category = duckdb_dtype_category(dtype)

    try:
        stats_row = _collect_stats(
            insight_source,
            column_name,
            category=category,
        )
    except Exception as exc:
        duration = perf_counter_ns() - start_ns
        return ColumnInsight(
            config.sheet_id,
            config.plan_hash,
            column_name,
            dtype_label,
            None,
            None,
            None,
            None,
            None,
            {},
            (),
            None,
            source_path=config.source_path,
            duration_ns=duration,
            error=str(exc),
        )

    row_count = _to_int(stats_row.get("row_count"))
    non_null_count = _to_int(stats_row.get("non_null_count"))
    null_count = _to_int(stats_row.get("null_count"))
    distinct_count = _to_int(stats_row.get("distinct_count"))
    null_fraction = _fraction(null_count, row_count)
    low_cardinality_numeric = _is_low_cardinality_numeric(category, distinct_count)

    stats_payload = _filter_stats(stats_row)
    if category == "temporal":
        stats_payload = _normalize_temporal_stats(stats_payload, stats_row)

    top_value_limit = (
        max(0, config.top_values)
        if _supports_top_value_summary(category) or low_cardinality_numeric
        else 0
    )
    top_values = _collect_top_values(
        insight_source,
        column_name,
        limit=top_value_limit,
        non_null_count=non_null_count,
    )
    histogram = None
    if not low_cardinality_numeric:
        histogram = _collect_histogram(
            insight_source,
            column_name,
            category=category,
            stats_row=stats_row,
            non_null_count=non_null_count,
        )

    duration = perf_counter_ns() - start_ns
    return ColumnInsight(
        config.sheet_id,
        config.plan_hash,
        column_name,
        dtype_label,
        row_count,
        non_null_count,
        null_count,
        null_fraction,
        distinct_count,
        stats_payload,
        top_values,
        histogram,
        source_path=config.source_path,
        duration_ns=duration,
    )


def _collect_stats(
    insight_source: DuckDBColumnInsightSource,
    column: str,
    *,
    category: str | None,
) -> dict[str, Any]:
    try:
        return _execute_stats_query(insight_source, column, category=category)
    except Exception:
        if category is None:
            raise
    return _execute_stats_query(insight_source, column, category=None)


def _execute_stats_query(
    insight_source: DuckDBColumnInsightSource,
    column: str,
    *,
    category: str | None,
) -> dict[str, Any]:
    quoted = quote_duckdb_identifier(column)
    base = f"({insight_source.sql}) AS pulka_base"
    stats_exprs = [
        "COUNT(*) AS row_count",
        f"SUM(CASE WHEN {quoted} IS NOT NULL THEN 1 ELSE 0 END) AS non_null_count",
        f"SUM(CASE WHEN {quoted} IS NULL THEN 1 ELSE 0 END) AS null_count",
        f"COUNT(DISTINCT {quoted}) AS distinct_count",
    ]
    if _supports_min_max(category):
        stats_exprs.extend(
            [
                f"MIN({quoted}) AS min",
                f"MAX({quoted}) AS max",
            ]
        )
    if category == "numeric":
        stats_exprs.extend(
            [
                f"AVG({quoted}) AS mean",
                f"MEDIAN({quoted}) AS median",
                f"QUANTILE_CONT({quoted}, 0.95) AS p95",
                f"QUANTILE_CONT({quoted}, 0.05) AS p05",
                f"STDDEV_SAMP({quoted}) AS std",
            ]
        )
    elif category == "temporal":
        stats_exprs.extend(
            [
                f"MIN(epoch_ms({quoted})) AS min_epoch_ms",
                f"MAX(epoch_ms({quoted})) AS max_epoch_ms",
                f"to_timestamp(AVG(epoch_ms({quoted})) / 1000.0) AS mean",
                f"to_timestamp(QUANTILE_CONT(epoch_ms({quoted}), 0.5) / 1000.0) AS median",
                f"to_timestamp(QUANTILE_CONT(epoch_ms({quoted}), 0.95) / 1000.0) AS p95",
                f"to_timestamp(QUANTILE_CONT(epoch_ms({quoted}), 0.05) / 1000.0) AS p05",
                f"STDDEV_SAMP(epoch_ms({quoted})) AS std_epoch_ms",
            ]
        )
    query = f"SELECT {', '.join(stats_exprs)} FROM {base}"
    rows, schema = execute_duckdb_query(insight_source.source, query, params=insight_source.params)
    if not rows:
        return {}
    return _row_to_dict(rows[0], schema)


def _collect_top_values(
    insight_source: DuckDBColumnInsightSource,
    column: str,
    *,
    limit: int,
    non_null_count: int | None,
) -> tuple[TopValue, ...]:
    if limit <= 0 or not non_null_count:
        return ()
    quoted = quote_duckdb_identifier(column)
    base = f"({insight_source.sql}) AS pulka_base"
    query = (
        f"SELECT {quoted} AS value, COUNT(*) AS count "
        f"FROM {base} "
        f"WHERE {quoted} IS NOT NULL "
        f"GROUP BY {quoted} "
        "ORDER BY count DESC, value ASC "
        f"LIMIT {int(limit)}"
    )
    try:
        rows, schema = execute_duckdb_query(
            insight_source.source, query, params=insight_source.params
        )
    except Exception:
        return ()
    value_key = _resolve_column_key(schema, "value")
    count_key = _resolve_column_key(schema, "count")
    values: list[TopValue] = []
    for row in rows:
        payload = _row_to_dict(row, schema)
        raw_value = payload.get(value_key)
        count = _to_int(payload.get(count_key)) or 0
        display, truncated = summarize_value_preview(raw_value, max_chars=48)
        fraction = _fraction(count, non_null_count)
        values.append(TopValue(raw_value, display, count, fraction, truncated))
    return tuple(values)


def _collect_histogram(
    insight_source: DuckDBColumnInsightSource,
    column: str,
    *,
    category: str | None,
    stats_row: Mapping[str, Any],
    non_null_count: int | None,
) -> InsightHistogram | None:
    if category not in {"numeric", "temporal"}:
        return None
    if non_null_count in (None, 0):
        return None
    bounds = _histogram_bounds(category, stats_row)
    if bounds is None:
        return None
    min_value, max_value = bounds
    bin_width: float
    if category == "temporal":
        if max_value < min_value:
            min_value, max_value = max_value, min_value
        if max_value == min_value:
            bins = tuple(1.0 if idx == 0 else 0.0 for idx in range(_HISTOGRAM_BIN_COUNT))
            return InsightHistogram(bins)
        value_range = max_value - min_value
        bin_count = int(max(1, min(_HISTOGRAM_BIN_COUNT, value_range + 1)))
        bin_width = float(max(1, math.ceil(value_range / bin_count)))
    else:
        if not (math.isfinite(min_value) and math.isfinite(max_value)):
            return None
        if max_value < min_value:
            min_value, max_value = max_value, min_value
        if math.isclose(max_value, min_value):
            bins = tuple(1.0 if idx == 0 else 0.0 for idx in range(_HISTOGRAM_BIN_COUNT))
            return InsightHistogram(bins)
        bin_count = int(_HISTOGRAM_BIN_COUNT)
        bin_width = (max_value - min_value) / bin_count
        if bin_width <= 0 or not math.isfinite(bin_width):
            return None

    quoted = quote_duckdb_identifier(column)
    value_expr = f"epoch_ms({quoted})" if category == "temporal" else quoted
    base = f"({insight_source.sql}) AS pulka_base"
    bucket_expr = f"CAST(FLOOR(({value_expr} - ?) / ?) AS INTEGER) + 1"
    query = (
        "WITH buckets AS ("
        " SELECT"
        f" CASE WHEN {value_expr} IS NULL THEN NULL ELSE {bucket_expr} END AS bucket"
        f" FROM {base}"
        ")"
        " SELECT"
        f" CASE WHEN bucket < 1 THEN 1 WHEN bucket > {bin_count} THEN {bin_count}"
        " ELSE bucket END AS bucket,"
        " COUNT(*) AS count"
        " FROM buckets"
        " WHERE bucket IS NOT NULL"
        " GROUP BY bucket"
        " ORDER BY bucket"
    )
    params = (*insight_source.params, min_value, bin_width)
    try:
        rows, schema = execute_duckdb_query(
            insight_source.source,
            query,
            params=params,
        )
    except Exception:
        return None
    bucket_key = _resolve_column_key(schema, "bucket")
    count_key = _resolve_column_key(schema, "count")
    counts = [0] * bin_count
    for row in rows:
        payload = _row_to_dict(row, schema)
        bucket = _to_int(payload.get(bucket_key))
        count = _to_int(payload.get(count_key)) or 0
        if bucket is None:
            continue
        idx = bucket - 1
        if 0 <= idx < bin_count:
            counts[idx] = count
    max_count = max(counts) if counts else 0
    if max_count <= 0:
        return None
    normalized = tuple(count / max_count for count in counts)
    return InsightHistogram(normalized)


def _histogram_bounds(
    category: str,
    stats_row: Mapping[str, Any],
) -> tuple[int | float, int | float] | None:
    if category == "temporal":
        min_value = _to_int(stats_row.get("min_epoch_ms"))
        max_value = _to_int(stats_row.get("max_epoch_ms"))
        if min_value is None or max_value is None:
            return None
        return min_value, max_value
    minimum = stats_row.get("min")
    maximum = stats_row.get("max")
    if minimum is None or maximum is None:
        return None
    try:
        return float(minimum), float(maximum)
    except Exception:
        return None


def _normalize_temporal_stats(
    stats: dict[str, Any],
    stats_row: Mapping[str, Any],
) -> dict[str, Any]:
    normalized = dict(stats)
    std_epoch_ms = stats_row.get("std_epoch_ms")
    if std_epoch_ms is not None:
        with contextlib.suppress(Exception):
            normalized["std"] = timedelta(milliseconds=float(std_epoch_ms))
    normalized.pop("min_epoch_ms", None)
    normalized.pop("max_epoch_ms", None)
    normalized.pop("std_epoch_ms", None)
    return normalized


def _supports_min_max(category: str | None) -> bool:
    return category in {"numeric", "temporal", "string", "boolean"}


def _supports_top_value_summary(category: str | None) -> bool:
    return category == "string"


def _is_low_cardinality_numeric(category: str | None, distinct_count: int | None) -> bool:
    if category not in {"numeric", "temporal"}:
        return False
    if distinct_count is None or distinct_count < 0:
        return False
    return distinct_count <= LOW_CARDINALITY_NUMERIC_LIMIT


def _filter_stats(row: Mapping[str, Any]) -> dict[str, Any]:
    skip = {
        "row_count",
        "non_null_count",
        "null_count",
        "distinct_count",
        "min_epoch_ms",
        "max_epoch_ms",
        "std_epoch_ms",
    }
    return {key: row.get(key) for key in row if key not in skip}


def _fraction(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    try:
        assert denominator is not None
        return float(numerator) / float(denominator)
    except Exception:
        return None


def _to_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


def _resolve_column_key(schema: Mapping[str, Any], key: str) -> str:
    if key in schema:
        return key
    lowered = key.lower()
    for name in schema:
        if name.lower() == lowered:
            return name
    return key


def _row_to_dict(row: Sequence[Any], schema: Mapping[str, Any]) -> dict[str, Any]:
    columns = list(schema.keys())
    payload: dict[str, Any] = {}
    for idx, name in enumerate(columns):
        payload[name] = row[idx] if idx < len(row) else None
    return payload


__all__ = [
    "DuckDBColumnInsightSource",
    "build_duckdb_column_insight_source",
    "compute_duckdb_column_insight",
]
