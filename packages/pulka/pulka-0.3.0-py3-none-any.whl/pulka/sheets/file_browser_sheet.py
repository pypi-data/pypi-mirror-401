from __future__ import annotations

import itertools
import os
import re
import shutil
import warnings
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Literal

import polars as pl
from polars.exceptions import PerformanceWarning

from ..core.engine.contracts import TableSlice
from ..core.engine.polars_adapter import (
    PlanCompiler,
    PolarsPhysicalPlan,
    make_lazyframe_handle,
    make_physical_plan_handle,
)
from ..core.interfaces import JobRunnerProtocol
from ..core.plan import QueryPlan
from ..core.plan_ops import set_filter as plan_set_filter
from ..core.sheet import (
    SHEET_FEATURE_PLAN,
    SHEET_FEATURE_PREVIEW,
    SHEET_FEATURE_ROW_COUNT,
    SHEET_FEATURE_SLICE,
    SHEET_FEATURE_VALUE_AT,
    SheetFeature,
)
from ..core.sheet_actions import SheetEnterAction
from ..data.scan import detect_scan_kind
from ..data.scanners import ScannerRegistry
from .data_sheet import DataSheet


@dataclass(slots=True, frozen=True)
class FileBrowserAction:
    type: Literal["enter-directory", "open-file"]
    path: Path


@dataclass(slots=True, frozen=True)
class FileDeletionResult:
    deleted: tuple[Path, ...]
    errors: tuple[tuple[Path, str], ...]

    @property
    def changed(self) -> bool:
        return bool(self.deleted)


@dataclass(slots=True)
class _FileBrowserEntry:
    row: dict[str, Any]
    path: Path
    is_dir: bool
    openable: bool


@dataclass(slots=True)
class _FileBrowserSnapshot:
    entries: list[_FileBrowserEntry]
    signature: tuple[tuple[str, str, str, str, bool], ...]
    error: str | None


class FileBrowserSheet:
    """Sheet that lists openable datasets and directories within a folder."""

    _VISIBLE_COLUMNS: ClassVar[tuple[str, ...]] = ("name", "type", "size", "modified")
    _META_COLUMNS: ClassVar[tuple[str, ...]] = ("path", "is_dir", "sort_group")
    _COLUMNS: ClassVar[tuple[str, ...]] = _VISIBLE_COLUMNS + _META_COLUMNS
    _CACHE_EPOCH = itertools.count(1)
    _CAPABILITIES: ClassVar[frozenset[SheetFeature]] = frozenset(
        {
            SHEET_FEATURE_PLAN,
            SHEET_FEATURE_PREVIEW,
            SHEET_FEATURE_SLICE,
            SHEET_FEATURE_VALUE_AT,
            SHEET_FEATURE_ROW_COUNT,
        }
    )

    def __init__(self, directory: Path, *, scanners: ScannerRegistry, runner: JobRunnerProtocol):
        if not isinstance(runner, JobRunnerProtocol):
            msg = "runner must implement JobRunnerProtocol"
            raise TypeError(msg)
        self.is_file_browser = True
        self._scanners = scanners
        self._runner = runner
        self.sheet_id = f"file-browser:{directory}"
        self.directory = self._normalise_path(directory)
        self._schema = {
            "name": pl.Utf8,
            "type": pl.Utf8,
            "size": pl.Utf8,
            "modified": pl.Utf8,
            "path": pl.Utf8,
            "is_dir": pl.Boolean,
            "sort_group": pl.Int8,
        }
        self._entries: list[_FileBrowserEntry] = []
        self._error: str | None = None
        self._entries_signature: tuple[tuple[str, str, str, str, bool], ...] | None = None
        self._cache_version: int = next(self._CACHE_EPOCH)
        self._filter_text: str | None = None
        snapshot = self._capture_directory_snapshot()
        plan = self._normalize_plan(QueryPlan())
        self._data_sheet = self._build_data_sheet(snapshot.entries, plan)
        self._entries = snapshot.entries
        self._entries_signature = snapshot.signature
        self._error = snapshot.error

    @staticmethod
    def _normalise_path(path: Path) -> Path:
        candidate = Path(path).expanduser()
        if not candidate.is_absolute():
            try:
                base_path: Path | None = None
                base = os.environ.get("PWD")
                if base:
                    base_path = Path(base).expanduser()
                    if not base_path.is_absolute():
                        base_path = None
                cwd = Path.cwd()
                if base_path is not None:
                    try:
                        if base_path.samefile(cwd):
                            candidate = base_path / candidate
                        else:
                            candidate = cwd / candidate
                    except OSError:
                        candidate = cwd / candidate
                else:
                    candidate = cwd / candidate
            except OSError:
                candidate = Path.cwd() / candidate
        try:
            return candidate.absolute()
        except OSError:
            return candidate

    @property
    def columns(self) -> list[str]:
        return list(self._data_sheet.columns)

    @property
    def display_path(self) -> str:
        return str(self.directory)

    @property
    def status_message(self) -> str | None:
        return self._error

    @property
    def cache_version(self) -> int:
        return self._cache_version

    def schema_dict(self) -> dict[str, Any]:
        return dict(self._data_sheet.schema)

    def plan_snapshot(self) -> dict[str, object]:
        return {"kind": "file-browser", "path": str(self.directory)}

    @property
    def plan(self) -> QueryPlan:
        return self._data_sheet.plan

    def with_plan(self, plan: QueryPlan) -> FileBrowserSheet:
        normalized = self._normalize_plan(plan)
        if normalized == self._data_sheet.plan:
            return self
        self._data_sheet._update_plan(normalized)
        self._cache_version = next(self._CACHE_EPOCH)
        return self

    def snapshot_transforms(self) -> QueryPlan:
        return self._data_sheet.snapshot_transforms()

    def restore_transforms(self, snapshot: QueryPlan) -> None:
        normalized = self._normalize_plan(snapshot)
        self._data_sheet.restore_transforms(normalized)
        self._cache_version = next(self._CACHE_EPOCH)

    @property
    def row_provider(self):
        return self._data_sheet.row_provider

    def job_context(self) -> tuple[str, int, str]:
        return self._data_sheet.job_context()

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

        if plan.sort:
            sort_entries = [entry for entry in plan.sort if entry[0] != "sort_group"]
            sort_entries.insert(0, ("sort_group", False))
            new_sort = tuple(sort_entries)
            if new_sort != plan.sort:
                plan = replace(plan, sort=new_sort)

        return plan

    def _build_data_sheet(self, entries: Sequence[_FileBrowserEntry], plan: QueryPlan) -> DataSheet:
        rows = [entry.row for entry in entries]
        df = pl.DataFrame(rows, schema=self._schema)
        data_sheet = DataSheet(
            df.lazy(),
            plan=plan,
            columns=self._COLUMNS,
            sheet_id=self.sheet_id,
            runner=self._runner,
        )
        return data_sheet

    def _update_data_sheet_source(self, entries: Sequence[_FileBrowserEntry]) -> None:
        rows = [entry.row for entry in entries]
        df = pl.DataFrame(rows, schema=self._schema)
        lf = df.lazy()
        lf_with_ids, row_id_column = self._data_sheet._attach_row_id_column(lf)
        if row_id_column is not None:
            self._data_sheet._row_id_column = row_id_column

        full_schema = self._collect_schema(lf_with_ids)
        self._data_sheet._full_schema = dict(full_schema)
        schema = dict(full_schema)
        if self._data_sheet._row_id_column and self._data_sheet._row_id_column in schema:
            schema.pop(self._data_sheet._row_id_column, None)
        self._data_sheet.schema = schema

        physical = PolarsPhysicalPlan(
            lf_with_ids,
            source_kind="file-browser",
            source_path=str(self.directory),
        )
        self._data_sheet._physical_source = physical
        self._data_sheet._physical_source_handle = make_physical_plan_handle(physical)
        self._data_sheet.lf0 = make_lazyframe_handle(physical.to_lazyframe())

        compiler_columns = list(self._data_sheet.columns)
        if self._data_sheet._row_id_column and self._data_sheet._row_id_column in full_schema:
            compiler_columns.append(self._data_sheet._row_id_column)
        self._data_sheet._compiler = PlanCompiler(
            lf_with_ids,
            columns=compiler_columns,
            schema=full_schema,
            sql_executor=self._data_sheet._sql_executor,
        )

        self._data_sheet._cached_plan_snapshot = None
        self._data_sheet._generation = self._runner.bump_generation(self._data_sheet.sheet_id)
        self._data_sheet._row_provider.clear()

    @staticmethod
    def _collect_schema(lf: pl.LazyFrame) -> dict[str, pl.DataType]:
        try:
            return dict(lf.collect_schema())
        except Exception:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=PerformanceWarning)
                return dict(lf.schema)

    def _capture_directory_snapshot(self) -> _FileBrowserSnapshot:
        entries: list[_FileBrowserEntry] = []
        fingerprint: list[tuple[str, str, str, str, bool]] = []
        error: str | None = None

        parent = self.directory.parent
        if parent != self.directory:
            entry = self._build_entry(
                name="..",
                path=parent,
                is_dir=True,
                openable=True,
                sort_group=-1,
                type_label="dir",
                size_display="",
                modified_display="",
            )
            entries.append(entry)
            fingerprint.append(self._entry_signature(entry))

        try:
            children = sorted(
                self.directory.iterdir(),
                key=lambda path: (not path.is_dir(), path.name.lower()),
            )
        except OSError as exc:
            error = f"dir error: {exc}"
            return _FileBrowserSnapshot(entries, tuple(fingerprint), error)

        dirs: list[_FileBrowserEntry] = []
        files: list[_FileBrowserEntry] = []
        for child in children:
            is_dir = child.is_dir()
            is_db_file = self._db_scheme_for_path(child) is not None
            is_openable = is_db_file or self._scanners.can_scan(child)
            if is_dir:
                entry = self._format_entry(child, is_dir=True, openable=True, sort_group=0)
                dirs.append(entry)
                continue
            if not child.is_file():
                continue
            if not is_openable:
                continue
            entry = self._format_entry(child, is_dir=False, openable=True, sort_group=1)
            files.append(entry)

        for entry in (*dirs, *files):
            entries.append(entry)
            fingerprint.append(self._entry_signature(entry))

        return _FileBrowserSnapshot(entries, tuple(fingerprint), error)

    def _apply_snapshot(self, snapshot: _FileBrowserSnapshot) -> None:
        self._entries = snapshot.entries
        self._entries_signature = snapshot.signature
        self._error = snapshot.error
        self._cache_version = next(self._CACHE_EPOCH)
        self._update_data_sheet_source(snapshot.entries)

    def refresh_from_disk(self) -> bool:
        snapshot = self._capture_directory_snapshot()
        signature_changed = snapshot.signature != self._entries_signature
        error_changed = snapshot.error != self._error
        if not signature_changed and not error_changed:
            return False
        self._apply_snapshot(snapshot)
        return True

    def set_contains_filter(self, text: str) -> bool:
        cleaned = text.strip()
        if not cleaned:
            return False

        changed = cleaned != self._filter_text
        self._filter_text = cleaned
        if changed:
            clause = self._contains_filter_clause(cleaned)
            plan = plan_set_filter(self._data_sheet.plan, clause, mode="replace")
            normalized = self._normalize_plan(plan)
            self._data_sheet._update_plan(normalized)
            self._cache_version = next(self._CACHE_EPOCH)
        return changed

    def clear_filter(self) -> bool:
        if self._filter_text is None:
            return False
        self._filter_text = None
        plan = plan_set_filter(self._data_sheet.plan, None, mode="replace")
        normalized = self._normalize_plan(plan)
        self._data_sheet._update_plan(normalized)
        self._cache_version = next(self._CACHE_EPOCH)
        return True

    def _contains_filter_clause(self, text: str) -> str:
        pattern = re.escape(text)
        pattern_literal = pattern.replace("\\", "\\\\").replace('"', '\\"')
        base = 'c["name"].cast(pl.Utf8, strict=False).fill_null("")'
        return f'{base}.str.contains("(?i){pattern_literal}", literal=False)'

    def _format_entry(
        self,
        path: Path,
        *,
        is_dir: bool,
        openable: bool,
        sort_group: int,
    ) -> _FileBrowserEntry:
        try:
            stat_result = path.stat()
        except OSError:
            stat_result = None
        size_display = "" if is_dir else self._format_size(stat_result)
        modified_display = self._format_modified(stat_result)
        name = f"{path.name}/" if is_dir else path.name
        type_label = "dir" if is_dir else self._file_type_label(path)
        return self._build_entry(
            name=name or path.as_posix(),
            path=path,
            is_dir=is_dir,
            openable=openable,
            sort_group=sort_group,
            type_label=type_label,
            size_display=size_display,
            modified_display=modified_display,
        )

    def _build_entry(
        self,
        *,
        name: str,
        path: Path,
        is_dir: bool,
        openable: bool,
        sort_group: int,
        type_label: str,
        size_display: str,
        modified_display: str,
    ) -> _FileBrowserEntry:
        row = {
            "name": name,
            "type": type_label,
            "size": size_display,
            "modified": modified_display,
            "path": str(path),
            "is_dir": is_dir,
            "sort_group": sort_group,
        }
        return _FileBrowserEntry(row=row, path=path, is_dir=is_dir, openable=openable)

    @staticmethod
    def _entry_signature(entry: _FileBrowserEntry) -> tuple[str, str, str, str, bool]:
        row = entry.row
        return (
            str(row.get("name", "")),
            str(row.get("type", "")),
            str(row.get("size", "")),
            str(row.get("modified", "")),
            bool(entry.openable),
        )

    def _file_type_label(self, path: Path) -> str:
        db_scheme = self._db_scheme_for_path(path)
        if db_scheme is not None:
            return db_scheme
        kind = detect_scan_kind(str(path))
        if kind:
            return kind

        scanners = self._scanners.list_scanners()
        suffixes = [suffix.lower() for suffix in path.suffixes]
        for suffix in reversed(suffixes):
            if suffix in scanners:
                return suffix.lstrip(".")
            bare = suffix.lstrip(".")
            if bare and bare in scanners:
                return bare
            if bare and f"mime:{bare}" in scanners:
                return bare

        return "file"

    @staticmethod
    def _db_scheme_for_path(path: Path) -> str | None:
        suffix = path.suffix.lower()
        if suffix == ".sqlite":
            return "sqlite"
        if suffix == ".duckdb":
            return "duckdb"
        return None

    @staticmethod
    def _format_size(stat_result: Any | None) -> str:
        if stat_result is None:
            return "?"
        size = getattr(stat_result, "st_size", None)
        if not isinstance(size, int) or size < 0:
            return "?"
        units = ("B", "KB", "MB", "GB", "TB")
        value = float(size)
        for unit in units:
            if value < 1024 or unit == units[-1]:
                return f"{value:.0f}{unit}" if unit == "B" else f"{value:.1f}{unit}"
            value /= 1024
        return f"{size}B"

    @staticmethod
    def _format_modified(stat_result: Any | None) -> str:
        timestamp = getattr(stat_result, "st_mtime", None)
        if not isinstance(timestamp, (int, float)):
            return ""
        try:
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
        except (OverflowError, OSError, ValueError):
            return ""

    def _value_at(self, row: int, col: str) -> Any:
        plan = self._data_sheet.plan
        projection = list(plan.projection or self._data_sheet.columns)
        if col not in projection:
            projection.append(col)
        plan_for_value = plan.with_projection(projection)
        slice_, _status = self._data_sheet.row_provider.get_slice(
            plan_for_value,
            (col,),
            row,
            1,
        )
        if slice_.height == 0:
            return None
        column = slice_.column(col)
        if not column.values:
            return None
        return column.values[0]

    def fetch_slice(
        self,
        row_start: int,
        row_count: int,
        columns: Sequence[str],
    ) -> TableSlice:
        return self._data_sheet.fetch_slice(row_start, row_count, columns)

    def preview(self, rows: int, cols: Sequence[str] | None = None) -> TableSlice:
        return self._data_sheet.preview(rows, cols)

    def value_at(self, row: int, col: str) -> Any:
        return self._value_at(row, col)

    def row_count(self) -> int | None:
        return self._data_sheet.row_count()

    def supports(self, feature: SheetFeature, /) -> bool:
        return feature in self._CAPABILITIES

    def __len__(self) -> int:
        return len(self._data_sheet)

    def action_for_row(self, row: int) -> FileBrowserAction | None:
        entry = self._entry_at(row)
        if entry is None:
            return None
        if entry.is_dir:
            return FileBrowserAction(type="enter-directory", path=entry.path)
        if entry.openable:
            return FileBrowserAction(type="open-file", path=entry.path)
        return None

    def enter_action(self, viewer: Any) -> SheetEnterAction | None:
        try:
            row = int(getattr(viewer, "cur_row", 0))
        except Exception:
            row = 0
        action = self.action_for_row(row)
        if action is None:
            return None
        if action.type == "enter-directory":
            return SheetEnterAction(kind="open-path", path=action.path, open_as="directory")
        if action.type == "open-file":
            if self._db_scheme_for_path(action.path) is not None:
                return SheetEnterAction(kind="open-path", path=action.path, open_as="database")
            return SheetEnterAction(kind="open-path", path=action.path, open_as="dataset")
        return None

    def is_row_selectable(self, row: int) -> bool:
        entry = self._entry_at(row)
        if entry is None:
            return False
        return entry.row.get("name") != ".."

    def selection_block_reason(self, row: int) -> str | None:
        entry = self._entry_at(row)
        if entry is None:
            return None
        if entry.row.get("name") == "..":
            return "parent directory is not selectable"
        return None

    def at_path(self, directory: Path) -> FileBrowserSheet:
        return FileBrowserSheet(directory, scanners=self._scanners, runner=self._runner)

    def _entry_at(self, row: int) -> _FileBrowserEntry | None:
        if row < 0:
            return None
        try:
            name = self._value_at(row, "name")
            path_value = self._value_at(row, "path")
            is_dir = self._value_at(row, "is_dir")
        except Exception:
            return None
        if name is None or path_value is None:
            return None
        return _FileBrowserEntry(
            row={"name": str(name)},
            path=Path(str(path_value)),
            is_dir=bool(is_dir),
            openable=True,
        )

    def deletable_entries_for_rows(self, rows: Sequence[int]) -> list[_FileBrowserEntry]:
        seen: set[Path] = set()
        entries: list[_FileBrowserEntry] = []
        for raw_row in rows:
            try:
                row = int(raw_row)
            except Exception:
                continue
            entry = self._entry_at(row)
            if entry is None:
                continue
            if entry.row.get("name") == "..":
                continue
            if entry.path in seen:
                continue
            seen.add(entry.path)
            entries.append(entry)
        return entries

    def entries_for_rows(self, rows: Sequence[int]) -> list[_FileBrowserEntry]:
        seen: set[Path] = set()
        entries: list[_FileBrowserEntry] = []
        for raw_row in rows:
            try:
                row = int(raw_row)
            except Exception:
                continue
            entry = self._entry_at(row)
            if entry is None:
                continue
            if entry.row.get("name") == "..":
                continue
            if entry.path in seen:
                continue
            seen.add(entry.path)
            entries.append(entry)
        return entries

    def _count_files(
        self, entries: Sequence[_FileBrowserEntry]
    ) -> tuple[int, list[tuple[Path, str]]]:
        files = 0
        errors: list[tuple[Path, str]] = []
        seen: set[Path] = set()
        for entry in entries:
            path = entry.path
            if path in seen:
                continue
            seen.add(path)
            if entry.is_dir:
                try:
                    for _root, _dirs, filenames in os.walk(path):
                        files += len(filenames)
                except OSError as exc:
                    errors.append((path, f"count error: {exc}"))
            else:
                files += 1
        return files, errors

    def deletion_impact(
        self, entries: Sequence[_FileBrowserEntry]
    ) -> tuple[int, list[tuple[Path, str]]]:
        """Return the number of files that would be deleted (recursively) for ``entries``."""

        return self._count_files(entries)

    def delete_entries(self, entries: Sequence[_FileBrowserEntry]) -> FileDeletionResult:
        deleted: list[Path] = []
        errors: list[tuple[Path, str]] = []
        seen: set[Path] = set()
        for entry in entries:
            path = entry.path
            if path in seen:
                continue
            seen.add(path)
            if entry.is_dir:
                try:
                    shutil.rmtree(path)
                except FileNotFoundError:
                    deleted.append(path)
                except OSError as exc:  # pragma: no cover - filesystem specific
                    errors.append((path, str(exc)))
                    continue
                else:
                    deleted.append(path)
                continue
            try:
                path.unlink(missing_ok=True)
            except IsADirectoryError:
                try:
                    shutil.rmtree(path)
                except OSError as exc:  # pragma: no cover - filesystem specific
                    errors.append((path, str(exc)))
                    continue
                deleted.append(path)
            except OSError as exc:  # pragma: no cover - filesystem specific
                errors.append((path, str(exc)))
                continue
            else:
                deleted.append(path)

        if deleted or errors:
            snapshot = self._capture_directory_snapshot()
            self._apply_snapshot(snapshot)

        return FileDeletionResult(tuple(deleted), tuple(errors))

    # Layout hints ----------------------------------------------------

    @property
    def compact_width_layout(self) -> bool:
        return False

    @property
    def preferred_fill_column(self) -> str:
        return "name"


def file_browser_status_text(sheet: FileBrowserSheet) -> str:
    message = getattr(sheet, "status_message", None)
    if message:
        return message
    count = sheet.row_count() or 0
    return f"{count} entries"


__all__ = [
    "FileBrowserAction",
    "FileBrowserSheet",
    "FileDeletionResult",
    "file_browser_status_text",
]
