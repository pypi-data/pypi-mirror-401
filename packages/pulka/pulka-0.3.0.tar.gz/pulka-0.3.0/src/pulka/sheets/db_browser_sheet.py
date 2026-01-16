"""Database browser sheet for inspecting tables in sqlite/duckdb files."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, ClassVar

import polars as pl

from ..core.engine.duckdb_adapter import DuckDBPhysicalPlan, execute_duckdb_query
from ..core.interfaces import JobRunnerProtocol
from ..core.plan import QueryPlan
from ..core.sheet import (
    SHEET_FEATURE_PLAN,
    SHEET_FEATURE_PREVIEW,
    SHEET_FEATURE_ROW_COUNT,
    SHEET_FEATURE_SLICE,
    SHEET_FEATURE_VALUE_AT,
    SheetFeature,
)
from ..core.sheet_actions import SheetEnterAction
from .data_sheet import DataSheet


class DbBrowserSheet:
    """Sheet listing schemas/tables from a DuckDB/SQLite database file."""

    hide_transforms_panel_by_default: ClassVar[bool] = True
    hide_insight_panel_by_default: ClassVar[bool] = True

    _VISIBLE_COLUMNS: ClassVar[tuple[str, ...]] = ("table", "schema", "type")
    _SCHEMA: ClassVar[dict[str, pl.DataType]] = {
        "schema": pl.Utf8,
        "table": pl.Utf8,
        "type": pl.Utf8,
    }
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
        _source_sheet: object,
        *,
        db_path: Path,
        runner: JobRunnerProtocol,
    ) -> None:
        if not isinstance(runner, JobRunnerProtocol):
            msg = "runner must implement JobRunnerProtocol"
            raise TypeError(msg)
        self._db_path = self._normalize_path(db_path)
        self._scheme = self._db_scheme_for_path(self._db_path)
        if self._scheme is None:
            msg = f"unsupported database extension: {self._db_path.suffix}"
            raise ValueError(msg)
        if not self._db_path.exists():
            raise FileNotFoundError(self._db_path)
        self._connection_uri = f"{self._scheme}://{self._db_path}"
        self.sheet_id = f"db-browser:{self._db_path}"
        self._runner = runner

        rows = self._load_rows()
        plan = self._normalize_plan(QueryPlan())
        df = pl.DataFrame(rows, schema=self._SCHEMA)
        self._data_sheet = DataSheet(
            df.lazy(),
            plan=plan,
            columns=self._VISIBLE_COLUMNS,
            sheet_id=self.sheet_id,
            runner=self._runner,
        )

    @property
    def db_path(self) -> Path:
        return self._db_path

    @property
    def columns(self) -> list[str]:
        return list(self._data_sheet.columns)

    @property
    def plan(self) -> QueryPlan:
        return self._data_sheet.plan

    def with_plan(self, plan: QueryPlan) -> DbBrowserSheet:
        normalized = self._normalize_plan(plan)
        if normalized == self._data_sheet.plan:
            return self
        self._data_sheet._update_plan(normalized)
        return self

    def schema_dict(self) -> dict[str, Any]:
        return dict(self._data_sheet.schema)

    def plan_snapshot(self) -> dict[str, object]:
        return {"kind": "db-browser", "path": str(self._db_path)}

    def snapshot_transforms(self) -> QueryPlan:
        return self._data_sheet.snapshot_transforms()

    def restore_transforms(self, snapshot: QueryPlan) -> None:
        normalized = self._normalize_plan(snapshot)
        self._data_sheet.restore_transforms(normalized)

    @property
    def row_provider(self):
        return self._data_sheet.row_provider

    def job_context(self) -> tuple[str, int, str]:
        return self._data_sheet.job_context()

    def fetch_slice(self, row_start: int, row_count: int, columns) -> Any:
        return self._data_sheet.fetch_slice(row_start, row_count, columns)

    def preview(self, rows: int, cols=None) -> Any:
        return self._data_sheet.preview(rows, cols)

    def value_at(self, row: int, col: str) -> Any:
        return self._data_sheet.value_at(row, col)

    def row_count(self) -> int | None:
        return self._data_sheet.row_count()

    def supports(self, feature: SheetFeature, /) -> bool:
        return feature in self._CAPABILITIES

    def __len__(self) -> int:
        return len(self._data_sheet)

    def enter_action(self, viewer: Any) -> SheetEnterAction | None:
        try:
            row = int(getattr(viewer, "cur_row", 0))
        except Exception:
            row = 0
        try:
            schema = self._data_sheet.value_at(row, "schema")
            table = self._data_sheet.value_at(row, "table")
        except Exception:
            return None
        if table is None:
            return None
        schema_text = str(schema) if schema is not None else ""
        table_text = str(table)
        table_ref = f"{schema_text}.{table_text}" if schema_text else table_text
        return SheetEnterAction(
            kind="open-db-table",
            db_scheme=self._scheme,
            db_connection_uri=self._connection_uri,
            db_table=table_ref,
            db_path=self._db_path,
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize_path(path: Path) -> Path:
        try:
            candidate = path.expanduser()
        except Exception:
            candidate = path
        try:
            return candidate.resolve()
        except Exception:
            return candidate.absolute()

    @staticmethod
    def _db_scheme_for_path(path: Path) -> str | None:
        suffix = path.suffix.lower()
        if suffix == ".sqlite":
            return "sqlite"
        if suffix == ".duckdb":
            return "duckdb"
        return None

    def _normalize_plan(self, plan: QueryPlan) -> QueryPlan:
        projection = plan.projection
        if projection:
            projection = tuple(col for col in projection if col in self._VISIBLE_COLUMNS)
            if not projection:
                projection = self._VISIBLE_COLUMNS
        else:
            projection = self._VISIBLE_COLUMNS
        if projection != plan.projection:
            plan = plan.with_projection(projection)

        if not plan.sort:
            plan = replace(plan, sort=(("schema", False), ("table", False)))
        return plan

    def _load_rows(self) -> list[dict[str, Any]]:
        plan = DuckDBPhysicalPlan(
            scheme=self._scheme,
            connection_uri=self._connection_uri,
            table="",
            schema={},
        )
        query = (
            "SELECT table_schema, table_name, table_type "
            "FROM information_schema.tables "
            "ORDER BY table_schema, table_name"
        )
        rows, _schema = execute_duckdb_query(plan, query)
        records: list[dict[str, Any]] = []
        for row in rows:
            if len(row) < 3:
                continue
            schema, table, table_type = row[:3]
            type_label = self._normalize_table_type(table_type)
            records.append(
                {
                    "schema": "" if schema is None else str(schema),
                    "table": "" if table is None else str(table),
                    "type": type_label,
                }
            )
        return records

    @staticmethod
    def _normalize_table_type(value: Any) -> str:
        text = str(value).strip().lower() if value is not None else ""
        if "view" in text:
            return "view"
        if "table" in text:
            return "table"
        return text or "table"


__all__ = ["DbBrowserSheet"]
