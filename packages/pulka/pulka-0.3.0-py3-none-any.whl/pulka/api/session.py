"""
Session facade for Pulka.

This module provides the main entry point for embedding Pulka in other applications.
"""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import monotonic_ns
from types import TracebackType
from typing import TYPE_CHECKING

import polars as pl

from ..command.runtime import SessionCommandRuntime
from ..config.load import UserConfig
from ..core.sheet_traits import resolve_display_path, resolve_sheet_traits
from ..core.viewer import Viewer, ViewStack, viewer_public_state
from ..core.viewer.ui_hooks import ViewerUIHooks
from ..core.viewer.ui_state import (
    INSIGHT_ENABLED_FLAG,
    INSIGHT_USER_ENABLED_FLAG,
    inherit_ui_state,
    set_insight_state,
)
from ..data.db import DbSource, is_db_uri, parse_db_uri
from ..logging import Recorder, RecorderConfig
from ..sheets.data_sheet import DataSheet
from ..sheets.db_browser_sheet import DbBrowserSheet
from ..sheets.duckdb_sheet import DuckDBSheet
from ..sheets.file_browser_sheet import FileBrowserSheet, file_browser_status_text
from ..testing import is_test_mode
from ..utils import _boot_trace
from .runtime import Runtime

if TYPE_CHECKING:
    from ..core.sheet import Sheet


@dataclass(slots=True)
class StatusHistoryEntry:
    """Structured status entry captured during a session."""

    timestamp: str
    severity: str
    message: str
    source: str | None
    sheet_id: str | None
    sheet_type: str | None
    stack_depth: int | None
    created_ns: int | None

    def as_row(self) -> dict[str, object]:
        return {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
            "source": self.source,
            "sheet_id": self.sheet_id,
            "sheet_type": self.sheet_type,
            "stack_depth": self.stack_depth,
        }


def _format_status_timestamp() -> str:
    stamp = datetime(1970, 1, 1, 0, 0, 0) if is_test_mode() else datetime.now()
    return stamp.strftime("%Y-%m-%d %H:%M:%S")


def _format_status_elapsed(created_ns: int | None, *, now_ns: int) -> str:
    if created_ns is None:
        return ""
    delta_ns = max(0, now_ns - created_ns)
    seconds = int(delta_ns / 1_000_000_000)
    if seconds < 60:
        return f"{seconds}s ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def _reset_insight_state_if_hidden(viewer: Viewer, sheet: object) -> None:
    if not bool(getattr(sheet, "hide_insight_panel_by_default", False)):
        return
    state = getattr(viewer, "_ui_state", None)
    if not isinstance(state, dict):
        return
    state.pop(INSIGHT_ENABLED_FLAG, None)
    state.pop(INSIGHT_USER_ENABLED_FLAG, None)


def _status_duration_overrides(config: UserConfig) -> dict[str, float | None]:
    status = getattr(config, "status", None)
    duration = getattr(status, "duration", None) if status is not None else None
    if duration is None:
        return {}
    overrides: dict[str, float | None] = {}
    for key in ("debug", "info", "success", "warn", "error"):
        value = getattr(duration, key, None)
        if value is not None:
            overrides[key] = value
    return overrides


def _recorder_config_from_user_config(config: UserConfig) -> RecorderConfig:
    settings = getattr(config, "recorder", None)
    kwargs: dict[str, object] = {}
    if settings is None:
        return RecorderConfig()
    if settings.enabled is not None:
        kwargs["enabled"] = settings.enabled
    if settings.buffer_size is not None:
        kwargs["buffer_size"] = settings.buffer_size
    if settings.output_dir:
        kwargs["output_dir"] = Path(settings.output_dir).expanduser()
    if settings.compression in {"zst", "none"}:
        kwargs["compression"] = settings.compression
    if settings.compression_level is not None:
        kwargs["compression_level"] = settings.compression_level
    if settings.auto_flush_on_exit is not None:
        kwargs["auto_flush_on_exit"] = settings.auto_flush_on_exit
    if settings.cell_redaction in {"none", "hash_strings", "mask_patterns"}:
        kwargs["cell_redaction"] = settings.cell_redaction
    return RecorderConfig(**kwargs)


def _viewer_overrides_from_config(config: UserConfig) -> dict[str, object]:
    viewer_config = getattr(config, "viewer", None)
    overrides: dict[str, object] = {}
    if viewer_config is None:
        return overrides
    if viewer_config.min_col_width is not None:
        overrides["min_col_width"] = viewer_config.min_col_width
    if viewer_config.default_col_width_cap_compact is not None:
        overrides["default_col_width_cap_compact"] = viewer_config.default_col_width_cap_compact
    if viewer_config.default_col_width_cap_wide is not None:
        overrides["default_col_width_cap_wide"] = viewer_config.default_col_width_cap_wide
    if viewer_config.sep_overhead is not None:
        overrides["sep_overhead"] = viewer_config.sep_overhead
    if viewer_config.hscroll_fetch_overscan_cols is not None:
        overrides["hscroll_fetch_overscan_cols"] = viewer_config.hscroll_fetch_overscan_cols
    if viewer_config.status_large_number_threshold is not None:
        overrides["status_large_number_threshold"] = viewer_config.status_large_number_threshold
    column_width = getattr(viewer_config, "column_width", None)
    column_overrides: dict[str, int | float] = {}
    if column_width is not None:
        if column_width.sample_max_rows is not None:
            column_overrides["sample_max_rows"] = column_width.sample_max_rows
        if column_width.sample_batch_rows is not None:
            column_overrides["sample_batch_rows"] = column_width.sample_batch_rows
        if column_width.sample_budget_ms is not None:
            column_overrides["sample_budget_ns"] = int(column_width.sample_budget_ms * 1_000_000)
        if column_width.target_percentile is not None:
            column_overrides["target_percentile"] = column_width.target_percentile
        if column_width.padding is not None:
            column_overrides["padding"] = column_width.padding
    if column_overrides:
        overrides["column_width_settings"] = column_overrides
    tui_config = getattr(config, "tui", None)
    if tui_config is not None and tui_config.max_steps_per_frame is not None:
        overrides["max_steps_per_frame"] = tui_config.max_steps_per_frame
    return overrides


class Session:
    """
    A session represents a single interaction with a data source.

    It manages the viewer state, data access, and provides methods for
    programmatic interaction with the data. The ``command_runtime`` attribute
    exposes a :class:`~pulka.command.runtime.SessionCommandRuntime` that powers
    both the TUI and headless runners.
    """

    def __init__(
        self,
        path: str | Path | None,
        *,
        viewport_rows: int | None = None,
        viewport_cols: int | None = None,
        recorder: Recorder | None = None,
        ui_hooks: ViewerUIHooks | None = None,
        runtime: Runtime | None = None,
        lazyframe: pl.LazyFrame | None = None,
        source_label: str | None = None,
        initial_sheet: Sheet | None = None,
    ):
        """
        Initialize a new Pulka session.

        Args:
            path: Path to the data file to open (required unless ``lazyframe`` is provided)
            lazyframe: Optional ``pl.LazyFrame`` to open directly without scanning a path
            source_label: Display label recorded when ``lazyframe`` is provided
            viewport_rows: Override the number of visible rows (for testing)
            viewport_cols: Override the number of visible columns (for testing)
            recorder: Optional flight recorder instance to reuse
            ui_hooks: Viewer hook bridge used for terminal measurements and redraws
            runtime: Shared :class:`~pulka.api.runtime.Runtime` providing
                configuration, registries, and plugin metadata. When omitted, a
                private runtime will be created for this session.
        """
        if path is None and lazyframe is None and initial_sheet is None:
            msg = "Session requires a source path, lazyframe, or initial sheet"
            raise ValueError(msg)

        db_uri = isinstance(path, str) and is_db_uri(path)
        if db_uri:
            source_label = source_label or path

        self._viewport_rows = viewport_rows
        self._viewport_cols = viewport_cols

        owns_runtime = runtime is None
        self.runtime = runtime or Runtime()
        runtime = self.runtime
        self._owns_runtime = owns_runtime
        self._closed = False
        self.job_runner = runtime.job_runner
        self.config = runtime.config
        self._status_duration_overrides = _status_duration_overrides(self.config)
        self._viewer_overrides = _viewer_overrides_from_config(self.config)
        self.recorder = recorder or Recorder(_recorder_config_from_user_config(self.config))
        self.view_stack = ViewStack(ui_hooks=ui_hooks)
        self.viewer: Viewer | None = None
        self._view_stack_unsubscribe = self.view_stack.add_active_viewer_listener(
            self._on_active_viewer_changed
        )
        self.commands = runtime.commands
        self.sheets = runtime.sheets
        self.scanners = runtime.scanners
        self.plugin_manager = runtime.plugin_manager
        self.plugin_modules = runtime.plugin_modules
        self.loaded_plugins = runtime.loaded_plugins
        self.plugin_failures = runtime.plugin_failures
        self.plugin_metadata = runtime.plugin_metadata
        self.disabled_plugins = runtime.disabled_plugins
        self.disabled_plugins_configured = runtime.disabled_plugins_configured

        self.command_runtime: SessionCommandRuntime = SessionCommandRuntime(self)
        self._command_cwd: Path | None = None
        self._status_history: list[StatusHistoryEntry] = []

        runtime.bootstrap_recorder(self.recorder)

        resolved_path = None if db_uri else (Path(path) if path is not None else None)
        self._source_path = resolved_path or Path("<expr>")
        self._dataset_path: Path | None = resolved_path

        if initial_sheet is not None:
            self._dataset_path = None
            label = source_label or resolve_display_path(initial_sheet) or "<browser>"
            self._install_root_sheet(initial_sheet, source_label=label, source_is_path=False)
        elif lazyframe is not None:
            self.open_lazyframe(lazyframe, label=source_label)
        else:
            if db_uri and isinstance(path, str):
                self.open(path)
            else:
                assert resolved_path is not None  # for mypy
                self.open(resolved_path)
        with suppress(Exception):
            self.command_runtime.prepare_viewer(self.viewer)

    def record_status_event(
        self,
        *,
        message: str,
        severity: str,
        viewer: Viewer | None = None,
        created_ns: int | None = None,
        source: str | None = None,
    ) -> None:
        """Capture a status message for the session history."""

        sheet = getattr(viewer, "sheet", None) if viewer is not None else None
        timestamp = _format_status_timestamp()
        created_at = created_ns if created_ns is not None else monotonic_ns()
        self._status_history.append(
            StatusHistoryEntry(
                timestamp=timestamp,
                severity=severity,
                message=message,
                source=source,
                sheet_id=getattr(sheet, "sheet_id", None),
                sheet_type=type(sheet).__name__ if sheet is not None else None,
                stack_depth=getattr(viewer, "stack_depth", None),
                created_ns=created_at,
            )
        )

    def status_history_records(self) -> list[dict[str, object]]:
        """Return status history rows for sheet rendering."""
        now_ns = monotonic_ns() if not is_test_mode() else 0
        records: list[dict[str, object]] = []
        for entry in self._status_history:
            row = entry.as_row()
            row["elapsed"] = _format_status_elapsed(entry.created_ns, now_ns=now_ns)
            records.append(row)
        return records

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release resources associated with this session."""

        if self._closed:
            return
        self._closed = True

        recorder = getattr(self, "recorder", None)
        if recorder is not None and recorder.enabled:
            metrics_fn = getattr(self.job_runner, "metrics", None)
            if callable(metrics_fn):
                with suppress(Exception):
                    metrics_payload = metrics_fn()
                    if isinstance(metrics_payload, dict):
                        recorder.record("job_runner_metrics", metrics_payload)

        unsubscribe = getattr(self, "_view_stack_unsubscribe", None)
        if unsubscribe is not None:
            with suppress(Exception):
                unsubscribe()
            self._view_stack_unsubscribe = None

        for viewer in tuple(self.view_stack.viewers):
            sheet = getattr(viewer, "sheet", None)
            runner = getattr(viewer, "job_runner", None)
            sheet_id = getattr(sheet, "sheet_id", None)
            close_fn = getattr(sheet, "close", None)
            if callable(close_fn):
                with suppress(Exception):
                    close_fn()
            if runner is not None and sheet_id is not None:
                with suppress(Exception):
                    runner.invalidate_sheet(sheet_id)
        self.viewer = None
        self.view_stack = ViewStack(ui_hooks=self.view_stack.ui_hooks)

        if self._owns_runtime:
            self.runtime.close()

    def __enter__(self) -> Session:
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc: BaseException | None,
        _tb: TracebackType | None,
    ) -> None:
        self.close()

    def __del__(self) -> None:  # pragma: no cover - best-effort cleanup
        with suppress(Exception):
            self.close()

    def push_viewer(self, viewer: Viewer) -> Viewer:
        """Add ``viewer`` to the derived-view stack and make it active."""

        return self.view_stack.push(viewer)

    def _pop_viewer(self) -> None:
        """Pop the active viewer when a derived view finishes."""

        self.view_stack.pop()

    def open_sheet_view(
        self,
        kind: str,
        *,
        base_viewer: Viewer,
        viewer_options: dict[str, object] | None = None,
        **sheet_options: object,
    ) -> Viewer:
        """Instantiate a derived sheet and push its viewer onto the stack."""

        sheet_kwargs = dict(sheet_options)
        if "runner" not in sheet_kwargs:
            sheet_kwargs["runner"] = self.job_runner
        try:
            sheet = self.sheets.create(kind, base_viewer.sheet, **sheet_kwargs)
        except TypeError as exc:
            if (
                "runner" in sheet_kwargs
                and "unexpected keyword" in str(exc)
                and "runner" in str(exc)
            ):
                provider = getattr(self.sheets, "_providers", {}).get(kind, "unknown provider")
                msg = (
                    "Sheet factory for kind "
                    f"'{kind}' provided by {provider} does not accept the 'runner' keyword. "
                    "Update the constructor to accept a `runner` parameter so sessions "
                    "can reuse the runtime job runner."
                )
                raise TypeError(msg) from exc
            raise
        viewer_kwargs: dict[str, object] = {
            "viewport_rows": getattr(base_viewer, "_viewport_rows_override", None),
            "viewport_cols": getattr(base_viewer, "_viewport_cols_override", None),
            "source_path": getattr(base_viewer, "_source_path", None),
            "session": self,
            "ui_hooks": self.view_stack.ui_hooks,
            "status_durations": self._status_duration_overrides,
        }
        viewer_kwargs.update(self._viewer_overrides)
        if viewer_options:
            viewer_kwargs.update(viewer_options)

        derived_viewer = Viewer(sheet, runner=self.job_runner, **viewer_kwargs)
        inherit_ui_state(base_viewer, derived_viewer)
        _reset_insight_state_if_hidden(derived_viewer, sheet)
        if getattr(base_viewer, "_pulka_has_real_source_path", False):
            derived_viewer._pulka_has_real_source_path = True  # type: ignore[attr-defined]

        perf_callback = getattr(base_viewer, "_perf_callback", None)
        if perf_callback is not None and hasattr(derived_viewer, "set_perf_callback"):
            with suppress(Exception):
                derived_viewer.set_perf_callback(perf_callback)

        self.push_viewer(derived_viewer)
        active = self.view_stack.active
        return active if active is not None else derived_viewer

    def set_viewer_ui_hooks(self, hooks: ViewerUIHooks | None) -> None:
        """Install ``hooks`` for every viewer in the stack."""

        self.view_stack.set_ui_hooks(hooks)

    def _on_active_viewer_changed(self, viewer: Viewer) -> None:
        self.viewer = viewer

    def run_script(self, commands: list[str], auto_render: bool = True) -> list[str]:
        """
        Execute a list of script commands.

        Args:
            commands: List of command strings to execute
            auto_render: Whether to render the output after each command

        Returns:
            List of rendered outputs or messages
        """
        from ..headless.runner import run_script_mode

        return run_script_mode(
            self,
            commands,
            auto_render=auto_render,
        )

    def render(self, *, include_status: bool = True) -> str:
        """
        Render the current view of the data.

        Args:
            include_status: Whether to include the status bar in the output

        Returns:
            String representation of the current view
        """
        from ..render.table import render_table

        if self.recorder and self.recorder.enabled:
            with self.recorder.perf_timer(
                "render.table",
                payload={
                    "context": "session",
                    "include_status": bool(include_status),
                },
            ):
                return render_table(self.viewer, include_status=include_status)
        return render_table(self.viewer, include_status=include_status)

    def get_state_json(self) -> dict:
        """
        Get the current state of the session as a JSON-serializable dictionary.

        Returns:
            Dictionary containing cursor and viewport state
        """
        state = viewer_public_state(self.viewer)
        if state is None:  # pragma: no cover - defensive
            msg = "Active viewer does not expose snapshot state"
            raise RuntimeError(msg)

        visible_columns = list(state.visible_columns or state.columns)
        visible_column_count = state.visible_column_count or state.total_columns
        total_rows = state.total_rows if state.total_rows is not None else state.visible_row_count
        return {
            "cursor_row": state.cursor.row,
            "cursor_col": state.cursor.col,
            "top_row": state.viewport.row0,
            "left_col": state.viewport.col0,
            "n_rows": total_rows,
            "n_cols": visible_column_count,
            "col_order": visible_columns,
        }

    @property
    def sheet(self) -> Sheet:
        """Get the current sheet that the session is viewing."""
        return self.viewer.sheet

    @property
    def dataset_path(self) -> Path | None:
        """Return the currently open dataset path when available."""

        active = self.viewer
        if active is not None and getattr(active, "_pulka_has_real_source_path", False):
            source = getattr(active, "_source_path", None)
            candidate = self._coerce_dataset_path(source)
            if candidate is not None:
                return candidate
        return self._dataset_path

    @property
    def command_cwd(self) -> Path | None:
        """Return the working directory set by the :cd command."""

        return self._command_cwd

    @command_cwd.setter
    def command_cwd(self, path: Path | str | None) -> None:
        """Update the working directory used by command helpers."""

        if path is None:
            self._command_cwd = None
            return

        candidate = Path(path)
        with suppress(Exception):
            candidate = candidate.expanduser()
        try:
            candidate = candidate.resolve()
        except Exception:
            candidate = candidate.absolute()
        self._command_cwd = candidate

    def open(self, path: str | Path) -> None:
        """Open ``path`` and update the viewer."""

        _boot_trace("session:open start")
        if isinstance(path, str) and is_db_uri(path):
            source = parse_db_uri(path)
            if source is None:
                raise ValueError("Not a supported database URI")
            sheet = DuckDBSheet(source, runner=self.job_runner)
            self._dataset_path = None
            self._install_root_sheet(sheet, source_label=path, source_is_path=False)
            _boot_trace("session:open db sheet installed")
            return

        resolved = Path(path)
        if self._maybe_open_db_file(resolved):
            _boot_trace("session:open db file installed")
            return
        self._ensure_path_exists(resolved)
        self._dataset_path = resolved
        physical_plan = self.scanners.scan(resolved)
        sheet = DataSheet(physical_plan, runner=self.job_runner)
        self._install_root_sheet(sheet, source_label=str(resolved), source_is_path=True)
        _boot_trace("session:open file sheet installed")

    def open_lazyframe(self, lazyframe: pl.LazyFrame, *, label: str | None = None) -> None:
        """Open a ``LazyFrame`` directly without going through scanners."""

        self._dataset_path = None
        source_label = label or getattr(lazyframe, "_pulka_path", None) or "<expr>"
        sheet = DataSheet(lazyframe, runner=self.job_runner)
        self._install_root_sheet(sheet, source_label=source_label, source_is_path=False)

    def open_file_browser(self, directory: str | Path | None = None) -> None:
        """Open a file-browser sheet rooted at ``directory`` as the stack root."""

        target = self._coerce_browser_directory(directory)
        if target is None:
            raise ValueError("browse requires a directory path or file-backed dataset")
        if not target.is_dir():
            raise ValueError(f"{target} is not a directory")

        sheet = FileBrowserSheet(target, scanners=self.scanners, runner=self.job_runner)
        self._dataset_path = None
        self._install_root_sheet(sheet, source_label=str(target), source_is_path=False)
        new_viewer = self.viewer
        if new_viewer is not None:
            with suppress(Exception):
                self.command_runtime.prepare_viewer(new_viewer)
            with suppress(Exception):
                new_viewer.row_count_tracker.ensure_total_rows()
            new_viewer.status_message = file_browser_status_text(sheet)

    def open_dataset_viewer(
        self,
        path: str | Path,
        *,
        base_viewer: Viewer | None = None,
    ) -> Viewer:
        """Push a new viewer for ``path`` while keeping the current stack."""

        resolved = Path(path)
        self._ensure_path_exists(resolved)
        sheet = DataSheet(self.scanners.scan(resolved), runner=self.job_runner)
        reference_viewer = base_viewer or self.viewer
        viewer_kwargs: dict[str, object] = {
            "viewport_rows": getattr(reference_viewer, "_viewport_rows_override", None),
            "viewport_cols": getattr(reference_viewer, "_viewport_cols_override", None),
            "source_path": str(resolved),
            "session": self,
            "ui_hooks": self.view_stack.ui_hooks,
            "status_durations": self._status_duration_overrides,
        }
        viewer_kwargs.update(self._viewer_overrides)
        child_viewer = Viewer(sheet, runner=self.job_runner, **viewer_kwargs)
        inherit_ui_state(reference_viewer, child_viewer)
        child_viewer._pulka_has_real_source_path = True  # type: ignore[attr-defined]
        self.push_viewer(child_viewer)
        with suppress(Exception):
            self.command_runtime.prepare_viewer(child_viewer)
        if self.recorder.enabled:
            self.recorder.ensure_env_recorded()
            self.recorder.record_dataset_open(
                path=str(resolved),
                schema=getattr(sheet, "schema", {}),
                lazy=True,
            )
        return child_viewer

    def open_db_table_viewer(
        self,
        *,
        scheme: str,
        connection_uri: str,
        table: str,
        db_path: Path | None = None,
        base_viewer: Viewer | None = None,
    ) -> Viewer:
        """Push a new viewer for a database table."""

        if db_path is not None:
            self._ensure_path_exists(db_path)
        uri = f"{connection_uri}#{table}"
        source = DbSource(
            scheme=scheme,
            uri=uri,
            connection_uri=connection_uri,
            table=table,
            path=db_path,
        )
        sheet = DuckDBSheet(source, runner=self.job_runner)
        reference_viewer = base_viewer or self.viewer
        viewer_kwargs: dict[str, object] = {
            "viewport_rows": getattr(reference_viewer, "_viewport_rows_override", None),
            "viewport_cols": getattr(reference_viewer, "_viewport_cols_override", None),
            "source_path": uri,
            "session": self,
            "ui_hooks": self.view_stack.ui_hooks,
            "status_durations": self._status_duration_overrides,
        }
        viewer_kwargs.update(self._viewer_overrides)
        child_viewer = Viewer(sheet, runner=self.job_runner, **viewer_kwargs)
        inherit_ui_state(reference_viewer, child_viewer)
        _reset_insight_state_if_hidden(child_viewer, sheet)
        set_insight_state(child_viewer, enabled=True, user_enabled=True)
        self.push_viewer(child_viewer)
        with suppress(Exception):
            self.command_runtime.prepare_viewer(child_viewer)
        if self.recorder.enabled:
            self.recorder.ensure_env_recorded()
            self.recorder.record_dataset_open(
                path=uri,
                schema=getattr(sheet, "schema", {}),
                lazy=True,
            )
        return child_viewer

    def reload_viewer(self, viewer: Viewer) -> None:
        """Reload ``viewer`` in-place if it is backed by a filesystem path."""

        path = self._coerce_dataset_path(getattr(viewer, "_source_path", None))
        if path is None:
            msg = "viewer cannot be reloaded without a filesystem path"
            raise ValueError(msg)
        self._ensure_path_exists(path)
        sheet = DataSheet(self.scanners.scan(path), runner=self.job_runner)
        viewer.replace_sheet(sheet, source_path=str(path))
        viewer._pulka_has_real_source_path = True  # type: ignore[attr-defined]
        if viewer is self.view_stack.viewers[0]:
            self._dataset_path = path
        if self.recorder.enabled:
            self.recorder.ensure_env_recorded()
            self.recorder.record_dataset_open(
                path=str(path),
                schema=getattr(sheet, "schema", {}),
                lazy=True,
            )

    def _install_root_sheet(
        self,
        sheet: Sheet,
        *,
        source_label: str | Path | None,
        source_is_path: bool = False,
    ) -> None:
        label = str(source_label) if source_label is not None else "<expr>"
        root_viewer = Viewer(
            sheet,
            viewport_rows=self._viewport_rows,
            viewport_cols=self._viewport_cols,
            source_path=label,
            session=self,
            ui_hooks=self.view_stack.ui_hooks,
            status_durations=self._status_duration_overrides,
            runner=self.job_runner,
            **self._viewer_overrides,
        )
        root_viewer._pulka_has_real_source_path = bool(  # type: ignore[attr-defined]
            source_is_path
        )
        self.view_stack.reset(root_viewer)
        self._source_path = Path(label)

        if self.recorder.enabled:
            self.recorder.ensure_env_recorded()
            self.recorder.record_dataset_open(
                path=label,
                schema=getattr(sheet, "schema", {}),
                lazy=True,
            )

        if getattr(self, "plugin_failures", None):
            failed_names = ", ".join(name for name, _ in self.plugin_failures)
            plural = "s" if len(self.plugin_failures) > 1 else ""
            self.viewer.status_message = f"Plugin{plural} {failed_names} failed to load; see logs"

    def _coerce_dataset_path(self, source: str | Path | None) -> Path | None:
        if source is None:
            return None
        if isinstance(source, Path):
            candidate = source
        else:
            if source.startswith("<"):
                return None
            candidate = Path(source)
        return candidate

    def _coerce_browser_directory(self, directory: str | Path | None) -> Path | None:
        if directory is not None:
            try:
                return Path(directory).expanduser()
            except Exception:
                return None
        dataset = self.dataset_path
        if dataset is not None:
            return dataset if dataset.is_dir() else dataset.parent
        viewer = getattr(self, "viewer", None)
        sheet = getattr(viewer, "sheet", None)
        if sheet is not None and resolve_sheet_traits(sheet).is_file_browser:
            active_dir = getattr(sheet, "directory", None)
            if active_dir is not None:
                return Path(active_dir)
        return None

    @staticmethod
    def _ensure_path_exists(path: Path) -> None:
        if path.exists():
            return
        raise FileNotFoundError(path)

    def _maybe_open_db_file(self, path: Path) -> bool:
        scheme = self._db_scheme_for_path(path)
        if scheme is None:
            return False
        self._ensure_path_exists(path)
        sheet = DbBrowserSheet(
            None,
            db_path=path,
            runner=self.job_runner,
        )
        self._dataset_path = None
        self._install_root_sheet(sheet, source_label=str(path), source_is_path=False)
        return True

    @staticmethod
    def _db_scheme_for_path(path: Path) -> str | None:
        suffix = path.suffix.lower()
        if suffix == ".sqlite":
            return "sqlite"
        if suffix == ".duckdb":
            return "duckdb"
        return None


def open(
    path: str | Path | None,
    *,
    viewport_rows: int | None = None,
    viewport_cols: int | None = None,
    recorder: Recorder | None = None,
    ui_hooks: ViewerUIHooks | None = None,
    runtime: Runtime | None = None,
    lazyframe: pl.LazyFrame | None = None,
    source_label: str | None = None,
) -> Session:
    """
    Open a data file or pre-built ``pl.LazyFrame`` in a new Pulka session.

    Args:
        path: Path to the data file to open (required unless ``lazyframe`` is provided)
        viewport_rows: Override the number of visible rows (for testing)
        viewport_cols: Override the number of visible columns (for testing)
        recorder: Optional flight recorder instance to reuse
        ui_hooks: Optional UI bridge passed through to :class:`Viewer`
        runtime: Optional shared :class:`~pulka.api.runtime.Runtime` to reuse
            configuration and plugin state. When omitted, the session creates a
            private runtime.
        lazyframe: Optional ``pl.LazyFrame`` to open directly instead of scanning ``path``
        source_label: Display label recorded when ``lazyframe`` is provided

    Returns:
        A new Session instance
    """
    return Session(
        path,
        viewport_rows=viewport_rows,
        viewport_cols=viewport_cols,
        recorder=recorder,
        ui_hooks=ui_hooks,
        runtime=runtime,
        lazyframe=lazyframe,
        source_label=source_label,
    )
