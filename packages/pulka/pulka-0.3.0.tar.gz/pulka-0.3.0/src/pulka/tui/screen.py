"""
TUI screen management for Pulka.

This module manages the sheet stack, viewer state, and dialog handling
within the terminal user interface.
"""

from __future__ import annotations

import os
import threading
from collections.abc import Callable, Iterator, Sequence
from contextlib import suppress
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from time import perf_counter_ns
from types import MethodType, SimpleNamespace
from typing import TYPE_CHECKING, Any

import polars as pl
from prompt_toolkit import Application
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.application.current import get_app_or_none
from prompt_toolkit.formatted_text import ANSI, StyleAndTextTuples
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.widgets import Box, Button, Dialog, TextArea
from rich.console import Console
from rich.pretty import Pretty

from .. import __version__ as pulka_version
from .. import theme
from ..clipboard import copy_to_clipboard
from ..command.parser import CommandDispatchResult
from ..command.registry import CommandContext
from ..command.runtime import CommandRuntimeResult
from ..config import use_prompt_toolkit_table
from ..core.engine.contracts import TableSlice
from ..core.engine.polars_adapter import table_slice_from_dataframe
from ..core.predicate import render_predicate_text
from ..core.sheet_actions import SheetEnterAction, resolve_enter_action
from ..core.viewer import Viewer, build_filter_predicate_for_values, viewer_public_state
from ..core.viewer.ui_hooks import NullViewerUIHooks
from ..core.viewer.ui_state import (
    INSIGHT_ENABLED_FLAG,
    get_ui_state,
    resolve_insight_state,
    set_insight_state,
)
from ..data.filter_lang import compile_filter_predicate
from ..logging import Recorder, frame_hash, viewer_state_snapshot
from ..utils import _boot_trace_silenced

if TYPE_CHECKING:  # pragma: no cover - import for type checking only
    from ..api.session import Session

from . import modals as tui_modals
from .controllers.column_insight import ColumnInsightController
from .controllers.dataset_reload import DatasetReloadController
from .controllers.file_browser import FileBrowserController
from .controllers.file_ops import FileOpsController
from .controllers.file_watch import FileSnapshot, FileWatchController
from .job_pump import JobPump
from .keymap import build_key_bindings
from .screen_clipboard import ClipboardRegionController
from .screen_commands import CommandDispatcher
from .screen_files import ScreenFileController
from .screen_search import ScreenSearchController

_CLIPBOARD_RUN_IN_TERMINAL_THRESHOLD = 70 * 1024
from .modal_manager import ModalManager
from .presenters import StatusPresenter
from .screen_layout import build_screen_layout
from .ui_hooks import PromptToolkitViewerUIHooks

# Constants
_STACK_MIN_SIZE = 2  # Minimum stack size for frequency view filters
_HISTORY_MAX_SIZE = 20  # Maximum size for search/filter history
_CELL_MODAL_CHROME_HEIGHT = 8  # Non-text area rows needed by the cell modal
_INSIGHT_MIN_COLS_DEFAULT = 120  # Hide insight when the terminal is narrower than this
_TRANSFORM_IDENTIFIERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _build_transform_identifiers(count: int) -> tuple[str, ...]:
    if count <= 0:
        return ()
    if count > len(_TRANSFORM_IDENTIFIERS):
        return tuple(_TRANSFORM_IDENTIFIERS)
    return tuple(_TRANSFORM_IDENTIFIERS[:count])


def _format_expr_filters_for_modal(filter_clauses: Sequence[object]) -> str:
    """Return a joined expression filter string for the expression modal."""

    expr_texts: list[str] = []
    for clause in filter_clauses:
        kind = getattr(clause, "kind", None)
        text = getattr(clause, "text", None)
        if kind != "expr" or not text:
            continue
        expr_texts.append(text.strip())

    if not expr_texts:
        return ""

    wrapped = [f"({text})" for text in expr_texts]
    return " & ".join(wrapped)


def _ordered_freq_values(freq_viewer: Viewer, selected_ids: set[object]) -> list[object]:
    """Return selected frequency values ordered by current display rows."""

    if not selected_ids:
        return []

    freq_column = getattr(freq_viewer, "freq_source_col", None)
    if not freq_column:
        freq_column = freq_viewer.columns[0] if freq_viewer.columns else None

    ordered: list[object] = []
    display_df = getattr(getattr(freq_viewer, "sheet", None), "_display_df", None)
    if display_df is not None and freq_column in getattr(display_df, "columns", ()):
        with suppress(Exception):
            for value in display_df.get_column(freq_column).to_list():
                if value in selected_ids and value not in ordered:
                    ordered.append(value)

    for value in selected_ids:
        if value not in ordered:
            ordered.append(value)

    return ordered


def _resolve_full_path(path: Path) -> Path:
    try:
        candidate = path.expanduser()
    except Exception:
        candidate = path
    try:
        return candidate.resolve()
    except Exception:
        return candidate.absolute()


def _last_open_dataset_path(session: Session | None) -> str | None:
    if session is None:
        return None
    path = session.dataset_path
    if path is None:
        return None
    return str(_resolve_full_path(path))


@dataclass
class _ColumnSearchState:
    """Mutable state tracked while the column search feature is active."""

    query: str | None = None
    matches: list[int] = field(default_factory=list)
    position: int | None = None

    def clear(self) -> None:
        """Reset the stored query and matches."""

        self.query = None
        self.matches.clear()
        self.position = None

    def set(self, query: str, matches: list[int], *, current_col: int) -> None:
        """Store a fresh query and its matches."""

        self.query = query
        self._apply_matches(matches, current_col=current_col, preserve_position=False)

    def recompute(self, matches: list[int], *, current_col: int) -> None:
        """Refresh matches for an existing query while keeping position when possible."""

        self._apply_matches(matches, current_col=current_col, preserve_position=True)

    def _apply_matches(
        self, matches: list[int], *, current_col: int, preserve_position: bool
    ) -> None:
        previous_position = self.position if preserve_position else None
        self.matches = list(matches)
        if not self.matches:
            self.position = None
            return

        if current_col in self.matches:
            self.position = self.matches.index(current_col)
        elif previous_position is not None and previous_position < len(self.matches):
            self.position = previous_position
        else:
            self.position = 0


class Screen:
    def __init__(
        self,
        viewer: Viewer,
        recorder: Recorder | None = None,
        *,
        on_shutdown: Callable[[Session], None] | None = None,
    ):
        self.viewer = viewer
        self.session = viewer.session
        if self.session is None:
            raise RuntimeError("Screen requires a session-bound viewer")
        self._last_terminal_size: tuple[int, int] | None = None
        self._terminal_resize_handler_installed = False
        self._on_shutdown = on_shutdown
        self.commands = self.session.commands
        self._runtime = self.session.command_runtime
        self._recorder = recorder or self.session.recorder
        self._runtime.prepare_viewer(self.viewer)
        self.view_stack = self.session.view_stack
        self._command_dispatcher = CommandDispatcher(
            screen=self,
            runtime=self._runtime,
            get_recorder=lambda: self._recorder,
            get_viewer=lambda: self.viewer,
            apply_insight_state=lambda: self._apply_insight_state(refresh=self._insight_enabled),
            clear_column_search=self._clear_column_search,
        )
        self._insight_controller: ColumnInsightController | None = None
        self._insight_base_default = self._initial_insight_enabled()
        initial_fallback = self._insight_fallback_enabled(self.viewer, self._insight_base_default)
        initial_insight_state = resolve_insight_state(
            self.viewer, fallback_enabled=initial_fallback
        )
        self._insight_enabled = initial_insight_state.enabled
        self._insight_user_enabled = initial_insight_state.user_enabled
        self._insight_allowed = initial_insight_state.allowed
        self._insight_terminal_allowed = True
        self._transform_signature: tuple[object, ...] | None = None
        self._transform_identifiers: tuple[str, ...] = ()
        self._transform_identifier_map: dict[str, int] = {}
        self._transforms_active = False
        self._return_to_column_after_transforms = False
        self._insight_mode_user_set = False
        self._transform_autoclose_timer: threading.Timer | None = None
        self._transforms_insight_panel = None
        self._jobs: dict[Viewer, object] = {}  # Jobs for background processing
        self._job_pump = JobPump(
            jobs=self._jobs,
            check_dataset_file_changes=self._check_dataset_file_changes,
            check_file_browser_changes=self._check_file_browser_changes,
        )
        self._file_browser_controller = FileBrowserController(
            session=self.session, get_viewer=lambda: self.viewer
        )
        self._file_watch: FileWatchController | None = None
        # Use a getter that applies queued moves per frame (capped)
        self._pending_row_delta = 0
        self._pending_col_delta = 0
        self._count_buf: int | None = None
        self._clipboard = ClipboardRegionController(
            get_viewer=lambda: self.viewer,
            refresh=self.refresh,
            reset_pending_moves=self._reset_pending_moves,
            copy_to_clipboard=self._copy_to_clipboard,
        )
        # Allow tuning via env; default to 3 steps/frame
        try:
            from ..utils import _get_int_env

            env_value = os.environ.get("PULKA_MAX_STEPS_PER_FRAME")
            override = getattr(viewer, "_max_steps_per_frame_override", None)
            if env_value is not None:
                self._max_steps_per_frame = max(
                    1, _get_int_env("PULKA_MAX_STEPS_PER_FRAME", None, 3)
                )
            elif isinstance(override, int) and override > 0:
                self._max_steps_per_frame = override
            else:
                self._max_steps_per_frame = 3
        except Exception:
            self._max_steps_per_frame = 3
        self._base_max_steps_per_frame = self._max_steps_per_frame
        use_ptk_table = self._should_use_ptk_table()
        self._last_status_fragments: StyleAndTextTuples | None = None
        self._last_status_plain: str | None = None
        layout_parts = build_screen_layout(
            viewer=self.viewer,
            use_ptk_table=use_ptk_table,
            build_ptk_table_control=self._build_table_control,
            get_table_text=self._get_table_text,
            get_status_text=self._get_status_text,
            insight_enabled=lambda: self._insight_enabled,
            insight_allowed=self._insight_is_allowed,
        )
        self._use_ptk_table = layout_parts.use_ptk_table
        self._table_control = layout_parts.table_control
        self._status_control = layout_parts.status_control
        self._table_window = layout_parts.table_window
        self._status_window = layout_parts.status_window
        self._column_insight_panel = layout_parts.column_insight_panel
        self._transforms_insight_panel = layout_parts.transforms_insight_panel
        self._insight_panel = layout_parts.insight_panel
        self._insight_control = layout_parts.insight_control
        self._insight_window = layout_parts.insight_window
        self._insight_border = layout_parts.insight_border
        self._insight_border_padding = layout_parts.insight_border_padding
        self._insight_container = layout_parts.insight_container
        self.window = layout_parts.window
        self._view_stack_unsubscribe = self.view_stack.add_active_viewer_listener(
            self._on_active_viewer_changed
        )
        self._modal_manager = ModalManager(window=self.window, table_window=self._table_window)
        self._presenter = StatusPresenter(
            get_viewer=lambda: self.viewer,
            refresh=self.refresh,
            modals=self._modal_manager,
            get_app=lambda: self.app,
        )
        self._file_ops = FileOpsController(
            file_browser=self._file_browser_controller,
            presenter=self._presenter,
            get_viewer=lambda: self.viewer,
            refresh=self.refresh,
            handle_file_browser_refresh=self._handle_file_browser_refresh,
            invalidate=self._invalidate_app,
        )
        self._dataset_reload = DatasetReloadController(
            session=self.session,
            get_viewer=lambda: self.viewer,
            get_file_watch=lambda: self._file_watch,
            refresh=self.refresh,
            recorder_getter=lambda: getattr(self, "_recorder", None),
            open_reload_error_modal=lambda error_text: self._open_reload_error_modal(
                error_text=error_text
            ),
        )
        self._file_controller = ScreenFileController(
            get_viewer=lambda: self.viewer,
            get_session=lambda: self.session,
            get_file_watch=lambda: self._file_watch,
            get_hooks=lambda: getattr(self, "_viewer_ui_hooks", None),
            get_app=lambda: getattr(self, "app", None),
            file_browser=self._file_browser_controller,
            file_ops=self._file_ops,
            dataset_reload=self._dataset_reload,
            refresh=self.refresh,
            invalidate=self._invalidate_app,
            apply_insight_state=lambda: self._apply_insight_state(refresh=True),
            display_modal=self._display_modal,
            remove_modal=self._remove_modal,
            open_missing_dataset_modal=self._open_missing_dataset_modal,
        )
        self._search_controller = ScreenSearchController(
            screen=self,
            history_max_size=_HISTORY_MAX_SIZE,
            format_expr_filters=_format_expr_filters_for_modal,
        )
        self._col_search_state = _ColumnSearchState()

        kb = build_key_bindings(self)

        self.app = Application(
            layout=Layout(self.window, focused_element=self._table_window),
            key_bindings=kb,
            full_screen=True,
            mouse_support=self._use_ptk_table,
            style=theme.APP_STYLE,
        )
        self._install_prompt_toolkit_perf_hooks()

        self._viewer_ui_hooks = PromptToolkitViewerUIHooks(self.app)
        self._install_terminal_resize_handler()
        attach_hooks = getattr(self._table_control, "attach_ui_hooks", None)
        if callable(attach_hooks):
            hooks = attach_hooks(self._viewer_ui_hooks)
            if hooks is not None:
                self._viewer_ui_hooks = hooks
        self.session.set_viewer_ui_hooks(self._viewer_ui_hooks)
        self._file_watch = FileWatchController(
            dataset_path_getter=lambda: getattr(self.session, "dataset_path", None),
            viewer_getter=lambda: self.viewer,
            hooks_getter=lambda: getattr(self, "_viewer_ui_hooks", None),
            on_dataset_change=lambda path, snapshot: self._schedule_file_change_prompt(
                path, snapshot
            ),
            on_file_browser_refresh=lambda sheet: self._handle_file_browser_refresh(sheet),
            on_file_browser_error=lambda exc: self._handle_file_browser_error(exc),
        )

        self._insight_controller = ColumnInsightController(
            viewer=self.viewer,
            panel=self._column_insight_panel,
            recorder=self._recorder,
            invalidate=self.app.invalidate,
            call_soon=self._viewer_ui_hooks.call_soon,
        )
        self._apply_insight_state(refresh=True)
        self._file_watch.sync(force=True)
        self._file_watch.check(force=True)
        self._refresh_transform_insight()

    def _handle_before_render(self, app: Application) -> None:
        _ = app
        self._sync_terminal_metrics_if_needed()

    def _install_prompt_toolkit_perf_hooks(self) -> None:
        renderer = getattr(self.app, "renderer", None)
        if renderer is None:
            return
        if getattr(renderer, "_pulka_perf_wrapped", False):
            return

        original_render = renderer.render

        def _wrapped_render(_self_renderer: Any, *args: Any, **kwargs: Any) -> Any:
            recorder = self._recorder if self._recorder and self._recorder.enabled else None
            if recorder is None:
                return original_render(*args, **kwargs)

            layout = args[0] if args else kwargs.get("layout")
            original_layout_render = None
            build_ns = 0

            if layout is not None:
                original_layout_render = getattr(layout, "render", None)
                if callable(original_layout_render):

                    def _timed_layout_render(*render_args: Any, **render_kwargs: Any) -> Any:
                        nonlocal build_ns
                        start_ns = perf_counter_ns()
                        try:
                            return original_layout_render(*render_args, **render_kwargs)
                        finally:
                            build_ns += perf_counter_ns() - start_ns

                    layout.render = _timed_layout_render

            total_start_ns = perf_counter_ns()
            try:
                return original_render(*args, **kwargs)
            finally:
                total_ns = perf_counter_ns() - total_start_ns
                if layout is not None and original_layout_render is not None:
                    layout.render = original_layout_render
                if build_ns:
                    recorder.record_perf(
                        phase="render.ptk.screen_build",
                        duration_ms=build_ns / 1_000_000,
                        payload={"context": "tui"},
                    )
                    diff_ns = max(0, total_ns - build_ns)
                    recorder.record_perf(
                        phase="render.ptk.diff_output",
                        duration_ms=diff_ns / 1_000_000,
                        payload={"context": "tui"},
                    )

        renderer.render = MethodType(_wrapped_render, renderer)
        with suppress(Exception):
            renderer._pulka_perf_wrapped = True

    def _install_terminal_resize_handler(self) -> None:
        if self._terminal_resize_handler_installed:
            return
        existing = getattr(self.app, "__dict__", {}).get("_on_resize")
        if callable(existing) and getattr(existing, "_pulka_wrapped", False):
            self._terminal_resize_handler_installed = True
            return

        on_resize = getattr(self.app, "_on_resize", None)
        if callable(on_resize):
            original_on_resize = on_resize

            def _wrapped_on_resize() -> None:
                self._sync_terminal_metrics_if_needed()
                original_on_resize()

            with suppress(Exception):
                _wrapped_on_resize._pulka_wrapped = True
            self.app._on_resize = _wrapped_on_resize  # type: ignore[method-assign]
            self._terminal_resize_handler_installed = True
            return

        with suppress(Exception):
            self.app.before_render.add_handler(self._handle_before_render)

    def _sync_terminal_metrics_if_needed(self) -> None:
        try:
            size = self.app.output.get_size()
        except Exception:
            return
        size_tuple = (size.columns, size.rows)
        if size_tuple == self._last_terminal_size:
            return
        self._last_terminal_size = size_tuple
        previous_terminal_allowed = self._insight_terminal_allowed
        with suppress(Exception):
            self._update_viewer_metrics()
        with suppress(Exception):
            self.viewer.clamp()
        if self._insight_terminal_allowed != previous_terminal_allowed:
            self._apply_insight_visibility(refresh=self._insight_enabled)

    def _should_use_ptk_table(self) -> bool:
        return use_prompt_toolkit_table()

    def _initial_insight_enabled(self) -> bool:
        env_value = os.getenv("PULKA_INSIGHT_PANEL")
        if env_value is None:
            try:
                from shutil import get_terminal_size

                cols = get_terminal_size(fallback=(0, 0)).columns
            except Exception:
                cols = 0
            if cols:
                return cols >= _INSIGHT_MIN_COLS_DEFAULT
            return True
        normalized = env_value.strip().lower()
        if normalized in {"0", "false", "off", "no"}:
            return False
        if normalized in {"1", "true", "on", "yes"}:
            return True
        return True

    def _insight_has_room(self, cols: int) -> bool:
        if cols <= 0:
            return True
        return cols >= _INSIGHT_MIN_COLS_DEFAULT

    def _update_insight_terminal_allowed(self, cols: int) -> bool:
        allowed = self._insight_has_room(cols)
        if allowed == self._insight_terminal_allowed:
            return False
        self._insight_terminal_allowed = allowed
        return True

    def _insight_is_allowed(self) -> bool:
        return self._insight_allowed and self._insight_terminal_allowed

    def _insight_is_effective(self) -> bool:
        return self._insight_enabled and self._insight_is_allowed()

    def _apply_budget_plan(self, plan) -> None:
        multiplier = float(getattr(plan, "coalesce_multiplier", 1.0) or 1.0)
        base = getattr(self, "_base_max_steps_per_frame", self._max_steps_per_frame)
        if multiplier > 1.0:
            boosted = max(base, int(round(base * multiplier)))
            self._max_steps_per_frame = max(base, min(12, boosted))
        else:
            self._max_steps_per_frame = base

    def _build_table_control(self):
        from .controls.table_control import TableControl

        return TableControl(
            self.viewer,
            apply_pending_moves=self._apply_pending_moves,
            poll_background_jobs=self._poll_background_jobs,
            set_status=self._set_status_from_table,
            apply_budget_plan=self._apply_budget_plan,
            on_cell_click=self._clipboard.on_cell_click,
            recorder=self._recorder,
        )

    def _clear_g_buf(self) -> None:
        """Reset the pending g-command and count state."""
        if hasattr(self, "_g_buf"):
            self._g_buf = 0
        self._clear_count_buf()

    def _clear_count_buf(self) -> None:
        self._count_buf = None

    def _append_count_digit(self, digit: int) -> bool:
        if digit == 0 and self._count_buf is None:
            return False
        next_value = (self._count_buf or 0) * 10 + digit
        self._count_buf = min(next_value, 999)
        return True

    def _consume_count(self, default: int = 1) -> int:
        count = self._count_buf if self._count_buf is not None else default
        self._count_buf = None
        return max(1, count)

    def _reset_pending_moves(self) -> None:
        self._pending_row_delta = 0
        self._pending_col_delta = 0

    def _start_clipboard_region(self, *, format_name: str = "tsv") -> None:
        self._clipboard.start(format_name=format_name)

    def _start_clipboard_region_markdown(self) -> None:
        self._clipboard.start_markdown()

    def _start_clipboard_region_ascii(self) -> None:
        self._clipboard.start_ascii()

    def _start_clipboard_region_unicode(self) -> None:
        self._clipboard.start_unicode()

    def _cancel_clipboard_region(self) -> None:
        self._clipboard.cancel()

    def _on_active_viewer_changed(self, viewer: Viewer) -> None:
        previous = getattr(self, "viewer", None)
        self.viewer = viewer
        self._runtime.prepare_viewer(viewer)
        controller = getattr(self, "_file_browser_controller", None)
        if controller is not None:
            with suppress(Exception):
                controller.on_viewer_changed(viewer)
        table_control = getattr(self, "_table_control", None)
        update_viewer = getattr(table_control, "update_viewer", None)
        if callable(update_viewer):
            update_viewer(viewer)
        if previous is not None and previous is not viewer:
            self._clear_column_search()
        controller = getattr(self, "_insight_controller", None)
        if controller is not None:
            controller.on_viewer_changed(viewer)
        fallback_enabled = getattr(self, "_insight_enabled", self._insight_base_default)
        fallback_enabled = self._insight_fallback_enabled(viewer, fallback_enabled)
        insight_state = resolve_insight_state(viewer, fallback_enabled=fallback_enabled)
        allowed_changed = insight_state.allowed != self._insight_allowed
        enabled_changed = insight_state.enabled != self._insight_enabled
        self._insight_enabled = insight_state.enabled
        self._insight_user_enabled = insight_state.user_enabled
        self._insight_allowed = insight_state.allowed
        if allowed_changed or enabled_changed or insight_state.effective:
            self._apply_insight_state(refresh=insight_state.effective)
        self._insight_mode_user_set = False
        if self._transforms_panel_default_hidden() and self._insight_panel.mode == "transform":
            self._insight_panel.set_mode("column")
        self._transform_signature = None
        self._transforms_active = False
        self._return_to_column_after_transforms = False
        self._cancel_transform_autoclose()
        self._refresh_transform_insight()
        self._prune_stale_jobs()
        file_watch = getattr(self, "_file_watch", None)
        if file_watch is not None:
            file_watch.sync(force=True)

    def _prune_stale_jobs(self) -> None:
        active = set(self.view_stack.viewers)
        for stale_viewer in list(self._jobs):
            if stale_viewer not in active:
                self.cancel_job(stale_viewer)

    def register_job(self, viewer: Viewer, job: object | None) -> None:
        """Register a background job handle for a viewer."""

        if job is None:
            self.cancel_job(viewer)
            return
        previous = self._jobs.get(viewer)
        if previous is job:
            return
        if previous is not None and hasattr(previous, "cancel"):
            with suppress(Exception):
                previous.cancel()
        self._jobs[viewer] = job

    def cancel_job(self, viewer: Viewer) -> None:
        """Cancel and remove the background job for a viewer, if any."""

        job = self._jobs.pop(viewer, None)
        if job is not None and hasattr(job, "cancel"):
            with suppress(Exception):
                job.cancel()

    def _mutate_context(self, context: CommandContext) -> None:
        self._command_dispatcher.mutate_context(context)

    def commands_help_entries(self) -> Sequence[object]:
        return getattr(self, "_key_only_help_entries", ())

    def _finalise_runtime_result(
        self, result: CommandRuntimeResult
    ) -> CommandDispatchResult | None:
        return self._command_dispatcher.finalise_runtime_result(result)

    def _execute_command(
        self, name: str, args: list[str] | None = None, *, repeat: int = 1
    ) -> CommandDispatchResult | None:
        """Execute a command through the session command runtime."""

        return self._command_dispatcher.execute_command(name, args=args, repeat=repeat)

    def _queue_move(self, dr: int = 0, dc: int = 0) -> None:
        # Accumulate deltas; they'll be applied (capped) during next paint
        if dr != 0:
            self._pending_row_delta += dr
            # prevent runaway accumulation while still allowing page-sized deltas
            row_limit = max(100, abs(dr))
            self._pending_row_delta = max(-row_limit, min(row_limit, self._pending_row_delta))
        if dc != 0:
            self._pending_col_delta += dc
            col_limit = max(100, abs(dc))
            self._pending_col_delta = max(-col_limit, min(col_limit, self._pending_col_delta))

    def _record_key_event(self, event) -> None:
        # Record with structured recorder if available
        if self._count_buf is not None:
            try:
                first_key = event.key_sequence[0].key if event.key_sequence else None
            except Exception:
                first_key = None
            if not (isinstance(first_key, str) and first_key.isdigit()):
                self._clear_count_buf()
        if self._recorder and self._recorder.enabled:
            try:
                sequence = [kp.key for kp in event.key_sequence]
                data = [kp.data for kp in event.key_sequence]
            except Exception:
                sequence = []
                data = []
            payload = {"sequence": sequence, "data": data}
            payload["repeat"] = bool(getattr(event, "is_repeat", False))
            self._recorder.record("key", payload)

    def _toggle_recorder(self, event) -> None:
        """Toggle the structured recorder on/off from the TUI."""
        recorder = self._recorder
        if recorder is None:
            self.viewer.status_message = "recorder unavailable"
            self.refresh()
            return

        self._record_key_event(event)

        try:
            user_command = event.key_sequence[0].key if event.key_sequence else "@"
        except Exception:
            user_command = "@"

        if recorder.enabled:
            recorder.record(
                "control", {"action": "record_off", "source": "tui", "key": user_command}
            )
            path = recorder.flush_and_clear(reason="tui-toggle")
            recorder.disable()
            if path is not None:
                pending_message = f"flight recorder stopped - saved to {path.name}"
                self.viewer.status_message = pending_message
                self._copy_to_clipboard(
                    str(path),
                    success_message=(
                        f"flight recorder stopped - {path.name} (path copied to clipboard)"
                    ),
                    failure_message=pending_message,
                )
            else:
                self.viewer.status_message = "flight recorder disabled"
            self.refresh()
            return

        recorder.enable()
        recorder.ensure_env_recorded()
        source_path = getattr(self.viewer, "_source_path", None)
        schema = getattr(self.viewer.sheet, "schema", {})
        if source_path is not None:
            recorder.record_dataset_open(path=source_path, schema=schema, lazy=True)
        recorder.record("control", {"action": "record_on", "source": "tui", "key": user_command})
        self.viewer.status_message = "flight recorder started"
        self.refresh()

    def _handle_enter(self, event) -> None:
        if self._clipboard.is_active():
            if self._clipboard.awaiting_start():
                self._clipboard.set_start()
            else:
                self._clipboard.finalize()
            return
        action = resolve_enter_action(self.viewer)
        if action is None:
            self._open_cell_value_modal(event)
            return
        if action.kind == "open-path":
            if action.open_as == "database":
                self._open_database_browser(event, action.path)
                return
            self._handle_open_path_action(action)
            return
        if action.kind == "open-db-table":
            self._open_db_table_action(event, action)
            return
        if action.kind == "apply-selection":
            self._apply_selection_action(action)
            return
        self._open_cell_value_modal(event)

    def _handle_open_path_action(self, action: SheetEnterAction) -> None:
        self._file_controller.handle_open_path_action(action)

    def _open_database_browser(self, event, target: Path | None) -> None:
        viewer = self.viewer
        if target is None:
            viewer.status_message = "entry is not openable"
            self.refresh()
            return
        try:
            with _boot_trace_silenced():
                new_viewer = self.session.open_sheet_view(
                    "db_browser",
                    base_viewer=viewer,
                    viewer_options={"source_path": str(target)},
                    db_path=target,
                )
        except Exception as exc:
            self._open_error_modal(event, "Open database", str(exc))
            return
        count = new_viewer.sheet.row_count() or 0
        new_viewer.status_message = f"{count} tables"
        self.refresh()

    def _open_db_table_action(self, event, action: SheetEnterAction) -> None:
        if not action.db_table or not action.db_connection_uri or not action.db_scheme:
            self._open_error_modal(event, "Open table", "missing database table details")
            return
        try:
            with _boot_trace_silenced():
                self.session.open_db_table_viewer(
                    scheme=action.db_scheme,
                    connection_uri=action.db_connection_uri,
                    table=action.db_table,
                    db_path=action.db_path,
                    base_viewer=self.viewer,
                )
        except Exception as exc:
            self._open_error_modal(event, "Open table", str(exc))
            return
        self.viewer.status_message = f"opened {action.db_table}"
        self.refresh()

    def _enter_browser_directory(self, target: Path | None) -> None:
        self._file_controller.enter_browser_directory(target)

    def _open_dataset_from_action(self, target: Path | None) -> None:
        self._file_controller.open_dataset_from_action(target)

    def _after_file_browser_directory_change(self) -> None:
        self._file_controller.after_file_browser_directory_change()

    def _path_completion_base_dir(self) -> Path:
        return self._file_controller.path_completion_base_dir()

    def _open_file_from_browser(self, target: Path) -> None:
        self._file_controller.open_file_from_browser(target)

    def _file_browser_delete_targets(self, sheet) -> list[object]:
        return self._file_controller.file_browser_delete_targets(sheet)

    def _file_browser_entries(self, sheet) -> list[object]:
        return self._file_controller.file_browser_entries(sheet)

    def _open_file_delete_modal(self, event) -> None:
        self._file_controller.open_file_delete_modal(event)

    def _delete_file_browser_entries(self, sheet, entries: Sequence[object]) -> None:
        self._file_controller.delete_file_browser_entries(sheet, entries)

    def _open_confirmation_modal(
        self,
        *,
        title: str,
        message_lines: Sequence[str],
        on_confirm: Callable[[], None],
        context_type: str | None = None,
        payload: dict[str, object] | None = None,
    ) -> None:
        self._presenter.open_confirmation_modal(
            title=title,
            message_lines=message_lines,
            on_confirm=on_confirm,
            context_type=context_type,
            payload=payload,
        )

    def _open_simple_status_modal(self, title: str, lines: Sequence[str]) -> None:
        self._presenter.open_status_modal(title=title, lines=lines)

    def _request_file_transfer(
        self, operation: str, dest: str, *, source_paths: Sequence[Path] | None = None
    ) -> None:
        self._file_controller.request_file_transfer(operation, dest, source_paths=source_paths)

    def _request_file_rename(self, new_name: str) -> None:
        self._file_controller.request_file_rename(new_name)

    def _request_file_mkdir(self, path: str) -> None:
        self._file_controller.request_file_mkdir(path)

    def _perform_file_transfer(
        self, operation: str, targets: list[tuple[Path, Path]], *, allow_overwrite: bool = False
    ) -> None:
        self._file_controller.perform_file_transfer(
            operation, targets, allow_overwrite=allow_overwrite
        )

    def _reload_dataset(self) -> None:
        """Reload the currently open dataset if it originated from a path."""
        self._file_controller.reload_dataset()

    @staticmethod
    def _is_missing_error(exc: Exception) -> bool:
        return ScreenFileController.is_missing_error(exc)

    def _handle_missing_dataset(self, dataset_path: Path) -> None:
        """Switch to file browser when the backing file disappears."""
        self._file_controller.handle_missing_dataset(dataset_path)

    def _handle_reload_error(self, exc: Exception, dataset_path: Path) -> None:
        self._file_controller.handle_reload_error(exc, dataset_path)

    def _apply_insight_state(self, *, refresh: bool = False) -> None:
        viewer = getattr(self, "viewer", None)
        if viewer is not None:
            insight_state = set_insight_state(
                viewer,
                enabled=self._insight_enabled,
                user_enabled=self._insight_user_enabled,
            )
            self._insight_enabled = insight_state.enabled
            self._insight_user_enabled = insight_state.user_enabled
            self._insight_allowed = insight_state.allowed
        with suppress(Exception):
            self._update_viewer_metrics()
        self._apply_insight_visibility(refresh=refresh)

    def _apply_insight_visibility(self, *, refresh: bool = False) -> None:
        controller = getattr(self, "_insight_controller", None)
        effective = self._insight_is_effective()
        if controller is not None:
            controller.set_enabled(effective)
            if effective and refresh:
                with suppress(Exception):
                    controller.on_refresh()
        if not effective:
            if not self._insight_allowed:
                self._column_insight_panel.set_unavailable("Insight unavailable for this view.")
                self._transforms_insight_panel.set_unavailable("Insight unavailable for this view.")
            else:
                self._transforms_insight_panel.set_transforms(
                    filters=(),
                    predicates=(),
                    sorts=(),
                    identifiers=(),
                )
                self._transform_identifiers = ()
                self._transform_identifier_map = {}
        app = getattr(self, "app", None)
        if app is not None:
            app.invalidate()

    def set_insight_panel(self, enabled: bool | None = None) -> bool:
        """Toggle or explicitly set the insight sidecar visibility."""

        if enabled is None:
            enabled = not self._insight_enabled
        if enabled:
            if self._transforms_active and not self._transforms_panel_default_hidden():
                target_mode = "transform"
            else:
                target_mode = "column"
            self._insight_panel.set_mode(target_mode)
            self._cancel_transform_autoclose()
        self._insight_enabled = bool(enabled)
        self._insight_user_enabled = True
        self._apply_insight_state(refresh=self._insight_enabled)
        return self._insight_enabled

    def set_insight_panel_mode(self, mode: str | None = None) -> str:
        """Set or toggle the insight panel mode, ensuring it is visible."""

        if mode is None:
            self._insight_panel.toggle_mode()
        elif mode in {"column", "transform"}:
            self._insight_panel.set_mode(mode)
        self._insight_mode_user_set = True
        self._cancel_transform_autoclose()
        self._insight_enabled = True
        self._insight_user_enabled = True
        self._apply_insight_state(refresh=True)
        return self._insight_panel.mode

    def _refresh_transform_insight(self) -> None:
        viewer = getattr(self, "viewer", None)
        if viewer is None or self._transforms_insight_panel is None:
            return
        plan_controller = getattr(viewer, "plan_controller", None)
        plan = plan_controller.current_plan() if plan_controller is not None else None
        if plan is None:
            self._transforms_insight_panel.set_unavailable(
                "Transforms require a plan-backed sheet."
            )
            self._transform_identifiers = ()
            self._transform_identifier_map = {}
            self._apply_transform_state(has_transforms=False, signature_changed=False)
            return
        filters = plan.filter_clauses
        predicates = plan.predicates
        sorts = plan.sort
        columns = getattr(viewer, "columns", ())
        rendered_filters: list[str] = []
        for clause in filters:
            text = clause.text
            if clause.kind == "expr":
                try:
                    predicate = compile_filter_predicate(text, columns)
                except Exception:
                    predicate = None
                if predicate is not None:
                    text = render_predicate_text(predicate)
            rendered_filters.append(text)
        rendered_predicates = [render_predicate_text(predicate) for predicate in predicates]
        rendered_sorts = [f"{column} {'desc' if desc else 'asc'}" for column, desc in sorts]
        identifiers = _build_transform_identifiers(len(filters) + len(predicates) + len(sorts))
        self._transform_identifiers = identifiers
        self._transform_identifier_map = {
            identifier: index for index, identifier in enumerate(identifiers)
        }
        signature = (filters, predicates, sorts)
        signature_changed = signature != self._transform_signature
        self._transform_signature = signature
        self._transforms_insight_panel.set_transforms(
            filters=filters,
            predicates=predicates,
            sorts=sorts,
            identifiers=identifiers,
            rendered_filters=tuple(rendered_filters),
            rendered_predicates=tuple(rendered_predicates),
            rendered_sorts=tuple(rendered_sorts),
        )
        if (
            self._transforms_panel_default_hidden()
            and not self._insight_mode_user_set
            and self._insight_panel.mode == "transform"
        ):
            self._insight_panel.set_mode("column")
            self._invalidate_app()
        self._apply_transform_state(
            has_transforms=bool(filters or predicates or sorts),
            signature_changed=signature_changed,
        )

    def _remove_transform_by_identifier(self, identifier: str) -> None:
        viewer = getattr(self, "viewer", None)
        if viewer is None:
            return
        index = self._transform_identifier_map.get(identifier)
        if index is None:
            viewer.status_message = f"unknown transform id: {identifier}"
            return
        viewer.remove_transform_at(index)
        self._refresh_transform_insight()

    def _apply_transform_state(self, *, has_transforms: bool, signature_changed: bool) -> None:
        auto_show = not self._transforms_panel_default_hidden()
        if has_transforms:
            if not self._transforms_active:
                if auto_show:
                    self._return_to_column_after_transforms = (
                        self._insight_is_effective() and self._insight_panel.mode == "column"
                    )
                else:
                    self._return_to_column_after_transforms = False
            self._transforms_active = True
            if auto_show:
                if signature_changed or not self._insight_is_effective():
                    self._insight_panel.set_mode("transform")
                    self._invalidate_app()
                self._cancel_transform_autoclose()
                if not self._insight_is_effective() and self._insight_is_allowed():
                    self._insight_enabled = True
                    self._apply_insight_state(refresh=True)
                return
            if not self._insight_mode_user_set and self._insight_panel.mode != "column":
                self._insight_panel.set_mode("column")
                self._invalidate_app()
            return

        if not self._transforms_active:
            return

        self._transforms_active = False
        if not auto_show:
            self._cancel_transform_autoclose()
            return
        if self._return_to_column_after_transforms:
            self._return_to_column_after_transforms = False
            self._insight_panel.set_mode("column")
            if not self._insight_is_effective() and self._insight_is_allowed():
                self._insight_enabled = True
                self._apply_insight_state(refresh=True)
            else:
                self._invalidate_app()
            return

        self._insight_panel.set_mode("transform")
        self._schedule_transform_autoclose()
        self._invalidate_app()

    def _transforms_panel_default_hidden(self) -> bool:
        viewer = getattr(self, "viewer", None)
        sheet = getattr(viewer, "sheet", None) if viewer is not None else None
        return bool(getattr(sheet, "hide_transforms_panel_by_default", False))

    def _insight_fallback_enabled(self, viewer: Viewer, fallback_enabled: bool) -> bool:
        state = get_ui_state(viewer)
        if INSIGHT_ENABLED_FLAG not in state and self._insight_panel_default_hidden(viewer):
            return False
        return fallback_enabled

    @staticmethod
    def _insight_panel_default_hidden(viewer: Viewer) -> bool:
        sheet = getattr(viewer, "sheet", None)
        return bool(getattr(sheet, "hide_insight_panel_by_default", False))

    def _schedule_transform_autoclose(self) -> None:
        if not self._insight_is_allowed():
            return
        self._cancel_transform_autoclose()

        def _dispatch() -> None:
            hooks = getattr(self, "_viewer_ui_hooks", None)
            if hooks is None:
                return
            hooks.call_soon(self._finalize_transform_autoclose)

        timer = threading.Timer(3.0, _dispatch)
        timer.daemon = True
        self._transform_autoclose_timer = timer
        timer.start()

    def _cancel_transform_autoclose(self) -> None:
        timer = self._transform_autoclose_timer
        if timer is None:
            return
        timer.cancel()
        self._transform_autoclose_timer = None

    def _finalize_transform_autoclose(self) -> None:
        self._transform_autoclose_timer = None
        if self._transforms_active or self._return_to_column_after_transforms:
            return
        if self._insight_panel.mode != "transform":
            return
        if not self._insight_is_allowed():
            return
        if not self._insight_enabled:
            return
        self._insight_enabled = False
        self._apply_insight_state(refresh=False)

    def _copy_to_clipboard(
        self,
        payload: str,
        *,
        success_message: str | None = None,
        failure_message: str | None = None,
    ) -> bool:
        """Copy text without letting clipboard output corrupt the TUI layout."""

        app = get_app_or_none()
        if app is None or not app.is_running:
            success = copy_to_clipboard(
                payload,
                max_osc52_bytes=_CLIPBOARD_RUN_IN_TERMINAL_THRESHOLD,
            )
            if success_message is not None or failure_message is not None:
                self.viewer.status_message = success_message if success else failure_message
            return success

        payload_bytes = len(payload.encode("utf-8", "replace"))
        if payload_bytes <= _CLIPBOARD_RUN_IN_TERMINAL_THRESHOLD:
            success = copy_to_clipboard(
                payload,
                max_osc52_bytes=_CLIPBOARD_RUN_IN_TERMINAL_THRESHOLD,
            )
            if success_message is not None or failure_message is not None:
                self.viewer.status_message = success_message if success else failure_message
            return success

        async def _copy_async() -> None:
            try:
                success = await run_in_terminal(
                    lambda: copy_to_clipboard(
                        payload,
                        max_osc52_bytes=_CLIPBOARD_RUN_IN_TERMINAL_THRESHOLD,
                    ),
                    in_executor=True,
                )
            except Exception:
                success = False
            if success_message is not None or failure_message is not None:
                self.viewer.status_message = success_message if success else failure_message
                app.invalidate()

        app.create_background_task(_copy_async())
        return True

    def _apply_pending_moves(self) -> None:
        # Apply up to N moves per axis this frame, for smoother scrolling
        steps = min(self._max_steps_per_frame, abs(self._pending_row_delta))
        if steps:
            if self._pending_row_delta > 0:
                self.viewer.move_rows(steps)
                self._pending_row_delta -= steps
            else:
                self.viewer.move_rows(-steps)
                self._pending_row_delta += steps
        steps = min(self._max_steps_per_frame, abs(self._pending_col_delta))
        if steps:
            if self._pending_col_delta > 0:
                for _ in range(steps):
                    self.viewer.move_right()
                self._pending_col_delta -= steps
            else:
                for _ in range(steps):
                    self.viewer.move_left()
                self._pending_col_delta += steps

    def _get_table_text(self):
        # Coalesce rapid key repeats by applying pending deltas here
        self._apply_pending_moves()
        self._poll_background_jobs()
        # Import the render table function here to avoid circular imports
        from ..render.table import render_table

        recorder = self._recorder if getattr(self, "_recorder", None) else None
        try:
            if recorder and recorder.enabled:
                with recorder.perf_timer(
                    "render.table",
                    payload={"context": "tui", "trigger": "refresh"},
                ):
                    body = render_table(self.viewer)
            else:
                body = render_table(self.viewer)
        except Exception as exc:  # pragma: no cover - safety net
            self.viewer.set_status(f"render error: {exc}"[:120], severity="error")
            return ANSI("").__pt_formatted_text__()

        # Precompute status text so the footer stays in sync with the latest render
        from ..render.status_bar import render_status_line

        status_fragments: StyleAndTextTuples = []
        try:
            if recorder and recorder.enabled:
                with recorder.perf_timer(
                    "render.status",
                    payload={"context": "tui", "trigger": "refresh"},
                ):
                    status_fragments = render_status_line(self.viewer)
            else:
                status_fragments = render_status_line(self.viewer)
        except Exception as exc:  # pragma: no cover - safety net
            self.viewer.set_status(f"render status error: {exc}"[:120], severity="error")
            status_fragments = []
        self._set_status_from_table(status_fragments)
        self.viewer.acknowledge_status_rendered()
        status_text = self._last_status_plain or ""
        if self._recorder and self._recorder.enabled:
            state_snapshot = viewer_state_snapshot(self.viewer)
            self._recorder.record_state(state_snapshot)
            if status_text:
                self._recorder.record_status(status_text)
            frame_capture = f"{body}\n{status_text}" if status_text else body
            if self._insight_is_effective():
                panel_block = self._insight_panel.render_for_recorder()
                if panel_block:
                    frame_capture = f"{frame_capture}\n\n{panel_block}"
            self._recorder.record_frame(
                frame_text=frame_capture,
                frame_hash=frame_hash(frame_capture),
            )
        return ANSI(body).__pt_formatted_text__()

    def _get_status_text(self):
        viewer = self.viewer
        status_dirty = bool(viewer.is_status_dirty())
        if status_dirty:
            # Import lazily to avoid circular dependency at module import time
            from ..render.status_bar import render_status_line

            self._set_status_from_table(render_status_line(viewer))
            viewer.acknowledge_status_rendered()
        elif self._last_status_fragments is None:
            from ..render.status_bar import render_status_line

            self._set_status_from_table(render_status_line(viewer))
            viewer.acknowledge_status_rendered()
        return self._last_status_fragments or [("", "")]

    def _set_status_from_table(self, fragments: StyleAndTextTuples) -> None:
        stored = list(fragments)
        self._last_status_fragments = stored
        self._last_status_plain = "".join(part for _, part in stored)

    def _insight_sidecar_width(self) -> int:
        if not self._insight_is_effective():
            return 0
        # Insight column, plus border and padding containers.
        return self._insight_panel.width + 2

    def _update_viewer_metrics(self) -> None:
        hooks = getattr(self, "_viewer_ui_hooks", None)
        cols, _rows = NullViewerUIHooks().get_terminal_size((100, 30))
        if hooks is not None:
            with suppress(Exception):
                cols, _rows = hooks.get_terminal_size((cols, _rows))
        self._update_insight_terminal_allowed(cols)
        insight_width = self._insight_sidecar_width()
        if insight_width:
            width_override = max(20, cols - insight_width)
            self.viewer.set_view_width_override(width_override)
        else:
            self.viewer.set_view_width_override(None)
        self.viewer.update_terminal_metrics()

    def _pop_viewer(self) -> None:
        removed = self.view_stack.pop()
        if removed is None:
            return
        self.cancel_job(removed)

    def refresh(self, *, skip_metrics: bool = False):
        if not skip_metrics:
            previous_terminal_allowed = self._insight_terminal_allowed
            self._update_viewer_metrics()
            if self._insight_terminal_allowed != previous_terminal_allowed:
                self._apply_insight_visibility(refresh=self._insight_enabled)
        self.viewer.clamp()
        self._check_dataset_file_changes(force=True)
        self._check_file_browser_changes(force=True)
        self._refresh_transform_insight()
        controller = getattr(self, "_insight_controller", None)
        if controller is not None:
            if self._file_watch.dataset_prompt_active:
                self._column_insight_panel.set_unavailable(
                    "File changed; reload to resume insight."
                )
                self._transforms_insight_panel.set_unavailable(
                    "File changed; reload to resume insight."
                )
            else:
                controller.on_refresh()
        with suppress(Exception):
            self._viewer_ui_hooks.invalidate()

    def _invalidate_app(self) -> None:
        hooks = getattr(self, "_viewer_ui_hooks", None)
        if hooks is not None:
            with suppress(Exception):
                hooks.invalidate()
            return
        with suppress(Exception):
            self.app.invalidate()

    def _poll_background_jobs(self) -> None:
        self._job_pump.poll()

    def _handle_file_browser_refresh(self, sheet) -> None:
        self._file_controller.handle_file_browser_refresh(sheet)

    def _handle_file_browser_error(self, exc: Exception) -> None:
        self._file_controller.handle_file_browser_error(exc)

    def _check_dataset_file_changes(self, *, force: bool = False) -> None:
        self._file_controller.check_dataset_file_changes(force=force)

    def _check_file_browser_changes(self, *, force: bool = False) -> None:
        self._file_controller.check_file_browser_changes(force=force)

    @property
    def _file_watch_prompt_active(self) -> bool:
        return self._file_controller.file_watch_prompt_active()

    @_file_watch_prompt_active.setter
    def _file_watch_prompt_active(self, active: bool) -> None:
        self._file_controller.set_file_watch_prompt_active(active)

    def _schedule_file_change_prompt(
        self,
        path: Path,
        snapshot: FileSnapshot | None,
    ) -> None:
        self._file_controller.schedule_file_change_prompt(path=path, snapshot=snapshot)

    def _open_dataset_file_change_modal(
        self,
        *,
        path: Path,
        snapshot: FileSnapshot | None,
    ) -> None:
        self._file_controller.open_dataset_file_change_modal(path=path, snapshot=snapshot)

    def _complete_file_change_prompt(self, *, reload_file: bool) -> None:
        self._file_controller.complete_file_change_prompt(reload_file=reload_file)

    def run(self):
        try:
            self.app.run()
        finally:
            unsubscribe = getattr(self, "_view_stack_unsubscribe", None)
            if unsubscribe is not None:
                unsubscribe()
            self._file_watch.stop()
            session = self.session
            last_path = _last_open_dataset_path(session)
            if session is not None and self._on_shutdown is not None:
                with suppress(Exception):
                    self._on_shutdown(session)
            if session is not None:
                with suppress(Exception):
                    session.close()
                recorder = getattr(session, "recorder", None)
                if recorder is not None and recorder.enabled:
                    with suppress(Exception):
                        recorder.on_process_exit(reason="tui")
            if last_path is not None:
                print(f"Pulka {pulka_version}")
                print(last_path)

    def _display_modal(
        self,
        app,
        container,
        *,
        focus=None,
        context_type: str | None = None,
        payload: dict[str, object] | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        self._modal_manager.display(
            app,
            container,
            focus=focus,
            context_type=context_type,
            payload=payload,
            width=width,
            height=height,
        )

    def _calculate_modal_dimensions(
        self,
        app,
        *,
        target_width: int,
        target_height: int,
    ) -> tuple[int, int]:
        """Determine modal dimensions respecting terminal size constraints."""

        return self._modal_manager.calculate_dimensions(
            app,
            target_width=target_width,
            target_height=target_height,
            chrome_height=_CELL_MODAL_CHROME_HEIGHT,
        )

    def _remove_modal(self, app, *, restore_focus: bool = True) -> None:
        self._modal_manager.remove(app, restore_focus=restore_focus)

    def _build_read_only_modal_dialog(
        self,
        *,
        app,
        title: str,
        text_area: TextArea,
        extra_buttons: Sequence[Button] | None = None,
        ok_on_right: bool = False,
    ) -> tuple[Dialog, Button]:
        """Create a dialog with a read-only text area and shared controls."""

        def _close_modal(target_app) -> None:
            self._remove_modal(target_app)
            self.refresh()

        tui_modals.bind_close_keys(text_area, on_close=_close_modal)

        body = Box(body=HSplit([text_area], padding=1), padding=1)

        ok_button = Button(text="OK", handler=lambda: _close_modal(app))

        if ok_on_right:
            buttons = list(extra_buttons or [])
            buttons.append(ok_button)
        else:
            buttons = [ok_button]
            if extra_buttons:
                buttons.extend(extra_buttons)
        dialog = Dialog(title=title, body=body, buttons=buttons)
        return dialog, ok_button

    def _open_missing_dataset_modal(
        self,
        *,
        path: Path,
        snapshot: FileSnapshot,
    ) -> None:
        app = self.app
        message_lines = [
            f"{path} is no longer available.",
        ]
        if snapshot.error:
            message_lines.append(snapshot.error)
        message_lines.append("You will be redirected to the file browser sheet.")

        body = tui_modals.build_lines_body(message_lines)

        def _confirm() -> None:
            self._remove_modal(app)
            self._handle_missing_dataset(path)

        ok_button = Button(text="OK", handler=_confirm)

        dialog = Dialog(
            title="File missing",
            body=body,
            buttons=[ok_button],
        )

        self._display_modal(
            app,
            dialog,
            focus=ok_button,
            context_type="missing_dataset",
            payload={"path": str(path)},
            width=80,
        )

    def _open_reload_error_modal(self, *, error_text: str) -> None:
        app = self.app
        target_width = 80
        target_height = 40
        width, height = self._calculate_modal_dimensions(
            app,
            target_width=target_width,
            target_height=target_height,
        )
        text_area_height = max(3, height - _CELL_MODAL_CHROME_HEIGHT)

        text_area = TextArea(
            text=error_text,
            read_only=True,
            scrollbar=True,
            wrap_lines=True,
            height=text_area_height,
        )

        def _close_modal(target_app) -> None:
            self._remove_modal(target_app)
            self.refresh()

        tui_modals.bind_close_keys(text_area, on_close=_close_modal)

        body = Box(body=HSplit([text_area], padding=1), padding=1)

        def _copy_error() -> None:
            self._copy_to_clipboard(
                error_text,
                success_message="copied reload error to clipboard",
                failure_message="clipboard unavailable",
            )
            app.invalidate()

        copy_button = Button(text="Copy to clipboard", handler=_copy_error)
        close_button = Button(text="Close", handler=lambda: _close_modal(app))

        dialog = Dialog(
            title="Reload failed",
            body=body,
            buttons=[copy_button, close_button],
        )

        self._display_modal(
            app,
            dialog,
            focus=copy_button,
            context_type="reload_error",
            width=width,
            height=height,
        )

    def _open_cell_value_modal(self, event) -> None:
        """Open a modal showing details about the currently focused cell."""

        if not self.viewer.columns:
            return

        column_name = self.viewer.columns[self.viewer.cur_col]
        row_index = self.viewer.cur_row

        value = None
        value_error: str | None = None
        try:
            slice_ = self.viewer.sheet.fetch_slice(row_index, 1, [column_name])
            if isinstance(slice_, TableSlice):
                table_slice = slice_
            elif isinstance(slice_, pl.DataFrame):
                schema = getattr(self.viewer.sheet, "schema", {})
                table_slice = table_slice_from_dataframe(slice_, schema)
            else:
                table_slice = table_slice_from_dataframe(
                    pl.DataFrame(slice_), getattr(self.viewer.sheet, "schema", {})
                )

            if table_slice.height > 0 and column_name in table_slice.column_names:
                value = table_slice.column(column_name).values[0]
        except Exception as exc:  # pragma: no cover - defensive
            value_error = str(exc)

        target_width = 60
        target_height = 40
        width, height = self._calculate_modal_dimensions(
            event.app,
            target_width=target_width,
            target_height=target_height,
        )
        content_width = max(20, width - 6)

        def _render_text(*, pretty: bool) -> str:
            if value_error is not None:
                return f"Error: {value_error}"
            if pretty:
                console_buffer = StringIO()
                console = Console(
                    record=True,
                    width=content_width,
                    highlight=False,
                    file=console_buffer,
                )
                console.print(Pretty(value, expand_all=True, overflow="fold"))
                return console.export_text(clear=False)
            if isinstance(value, str):
                return value
            return str(value)

        render_pretty = value_error is None and not isinstance(value, str)
        rendered_text = _render_text(pretty=render_pretty)

        def _toggle_label(*, pretty: bool) -> str:
            return "Raw" if pretty else "Pretty"

        # Account for dialog chrome (label, padding, frame, and buttons) so the
        # text area fits within the requested height without triggering the
        # "window too small" warning from prompt_toolkit.
        text_area_height = max(3, height - _CELL_MODAL_CHROME_HEIGHT)

        text_area = TextArea(
            text=rendered_text,
            read_only=True,
            scrollbar=True,
            wrap_lines=True,
            height=text_area_height,
        )

        def _toggle_render() -> None:
            nonlocal render_pretty
            render_pretty = not render_pretty
            text_area.text = _render_text(pretty=render_pretty)
            text_area.buffer.cursor_position = 0
            toggle_button.text = _toggle_label(pretty=render_pretty)
            event.app.layout.focus(text_area)
            event.app.invalidate()

        toggle_button = Button(
            text=_toggle_label(pretty=render_pretty),
            handler=_toggle_render,
        )

        dialog, ok_button = self._build_read_only_modal_dialog(
            app=event.app,
            title=f"Cell {column_name} @ row {row_index + 1}",
            text_area=text_area,
            extra_buttons=[toggle_button],
            ok_on_right=True,
        )

        self._display_modal(
            event.app,
            dialog,
            focus=text_area,
            context_type="cell_value",
            payload={"column": column_name, "row": row_index},
            width=width,
            height=height,
        )

    def _apply_selection_action(self, action: SheetEnterAction) -> None:
        """Apply a selection-derived projection to the parent view."""

        if len(self.view_stack) < _STACK_MIN_SIZE:
            self.viewer.status_message = "no source view"
            self.refresh()
            return

        summary_viewer = self.viewer
        source_viewer = self.view_stack.parent
        if source_viewer is None:
            summary_viewer.status_message = "no source view"
            self.refresh()
            return

        selected_lookup = {name for name in action.columns if isinstance(name, str)}
        if not selected_lookup:
            summary_viewer.status_message = "select at least one column"
            self.refresh()
            return

        ordered_columns = [name for name in source_viewer.columns if name in selected_lookup]
        if not ordered_columns:
            summary_viewer.status_message = "no matching columns to keep"
            self.refresh()
            return

        try:
            source_viewer.keep_columns(ordered_columns)
        except Exception as exc:  # pragma: no cover - defensive
            summary_viewer.status_message = f"keep columns error: {exc}"[:120]
            self.refresh()
            return

        with suppress(Exception):
            summary_viewer.clear_row_selection()
        if action.pop_viewer:
            self._pop_viewer()
        self.refresh()

    def _filter_by_pick(self) -> None:
        """Apply filter based on the currently selected value in a frequency view."""
        # Get the frequency viewer (current view) and the source viewer (parent)
        if len(self.view_stack) < _STACK_MIN_SIZE:
            return

        freq_viewer = self.viewer
        source_viewer = self.view_stack.parent
        if source_viewer is None:
            return

        # Ensure we're in a frequency view
        if not hasattr(freq_viewer, "is_freq_view") or not getattr(
            freq_viewer, "is_freq_view", False
        ):
            return

        selected_ids = set(getattr(freq_viewer, "_selected_row_ids", set()))
        values: list[object] = []
        if selected_ids:
            values = _ordered_freq_values(freq_viewer, selected_ids)
        if not values:
            try:
                values = [freq_viewer.sheet.get_value_at(freq_viewer.cur_row)]
            except Exception:
                self.viewer.status_message = "unable to pick value"
                return

        # Apply the filter to the source view
        try:
            # Build predicate filter for the source column
            source_col = freq_viewer.freq_source_col
            if source_col is None:
                self.viewer.status_message = "unknown frequency source"
                return
            predicate = build_filter_predicate_for_values(source_col, values)
            source_viewer.apply_predicate(predicate, mode="append")
        except Exception as exc:
            self.viewer.status_message = f"filter error: {exc}"
        else:
            self.viewer.status_message = None
            with suppress(Exception):
                freq_viewer.clear_row_selection()
            self._pop_viewer()
            self.refresh()

    def _open_filter_modal(self, event, *, initial_text: str | None = None) -> None:
        self._search_controller.open_filter_modal(event, initial_text=initial_text)

    def _open_filter_modal_with_text(self, event, text: str) -> None:
        self._search_controller.open_filter_modal_with_text(event, text)

    def _open_transform_modal(self, event, *, initial_text: str | None = None) -> None:
        self._search_controller.open_transform_modal(event, initial_text=initial_text)

    def _open_sql_filter_modal(self, event, *, initial_text: str | None = None) -> None:
        self._search_controller.open_sql_filter_modal(event, initial_text=initial_text)

    def _open_sql_filter_modal_with_text(self, event, text: str) -> None:
        self._search_controller.open_sql_filter_modal_with_text(event, text)

    def _open_command_modal(self, event) -> None:
        self._search_controller.open_command_modal(event)

    def _open_shell_modal(self, event) -> None:
        self._search_controller.open_shell_modal(event)

    def _open_row_search_modal(self, event) -> None:
        self._search_controller.open_row_search_modal(event)

    def _open_filter_contains_modal(self, event) -> None:
        self._search_controller.open_filter_contains_modal(event)

    def _open_search_modal(self, event) -> None:
        self._search_controller.open_search_modal(event)

    def _open_column_search_modal(self, event) -> None:
        self._search_controller.open_column_search_modal(event)

    def _apply_column_search(self, query: str) -> bool:
        """Compute matches for ``query`` and focus the first result."""

        matches = self._compute_column_search_matches(query)
        state = self._col_search_state
        state.set(query, matches, current_col=self.viewer.cur_col)
        if not matches:
            self.viewer.status_message = f"column search: no match for '{query}'"
            return False

        target = state.position or 0
        if self._focus_column_search_match(target):
            return True

        self.viewer.status_message = f"column search: unable to focus '{query}'"
        return False

    def _iter_column_search_candidates(self) -> Iterator[tuple[int, str]]:
        """Yield candidate column indices and names for column search ranking."""

        state = viewer_public_state(self.viewer)
        columns: list[str]
        hidden: set[str]
        if state is None:  # pragma: no cover - defensive
            columns = list(getattr(self.viewer, "columns", ()))
            hidden = set(getattr(self.viewer, "_hidden_cols", ()))
        else:
            columns = list(state.columns)
            hidden = set(state.hidden_columns)

        for idx, name in enumerate(columns):
            if name in hidden:
                continue
            yield idx, name

    def _compute_column_search_matches(self, query: str) -> list[int]:
        """Rank matching columns by how closely they match ``query``."""

        query_lower = query.lower()
        ranked: list[tuple[tuple[int, int], int]] = []

        for idx, name in self._iter_column_search_candidates():
            lowered = name.lower()
            if query_lower not in lowered:
                continue
            if lowered == query_lower:
                priority = 0
            elif lowered.startswith(query_lower):
                priority = 1
            else:
                priority = 2
            ranked.append(((priority, idx), idx))

        ranked.sort(key=lambda item: item[0])
        return [idx for _, idx in ranked]

    def _focus_column_search_match(self, position: int) -> bool:
        matches = self._col_search_state.matches
        if position < 0 or position >= len(matches):
            return False

        match_idx = matches[position]
        if match_idx >= len(self.viewer.columns):
            self._recompute_column_search_matches()
            matches = self._col_search_state.matches
            if position < 0 or position >= len(matches):
                return False
            match_idx = matches[position]

        col_name = self.viewer.columns[match_idx]
        moved = self.viewer.goto_col(col_name)
        if moved:
            self._col_search_state.position = position
            total = len(matches)
            self.viewer.status_message = f"column search: {col_name} ({position + 1}/{total})"
        return moved

    def _handle_column_search_navigation(self, *, forward: bool) -> bool:
        """Navigate among column search matches in response to ``n``/``N``."""

        state = self._col_search_state
        if not state.query or not state.matches:
            return False

        self._recompute_column_search_matches()
        matches = state.matches
        if not matches:
            self.viewer.status_message = f"column search: no match for '{state.query}'"
            self._clear_column_search()
            return True

        try:
            anchor = matches.index(self.viewer.cur_col)
        except ValueError:
            anchor = -1 if forward else len(matches)

        step = 1 if forward else -1
        target = anchor + step
        if 0 <= target < len(matches):
            if self._focus_column_search_match(target):
                return True
            self.viewer.status_message = "column search: unable to focus match"
            return True

        direction = "next" if forward else "previous"
        self.viewer.status_message = f"column search: no {direction} match"
        return True

    def _clear_column_search(self) -> None:
        """Reset column search bookkeeping so ``n``/``N`` fall back to row search."""

        self._col_search_state.clear()

    def _recompute_column_search_matches(self) -> None:
        """Refresh cached matches for the active column search query."""

        state = self._col_search_state
        if not state.query:
            state.clear()
            return

        matches = self._compute_column_search_matches(state.query)
        state.recompute(matches, current_col=self.viewer.cur_col)

    def _status_error_message(self, prefixes: Sequence[str]) -> str | None:
        """Return the current status message when it matches one of ``prefixes``."""

        message = self.viewer.status_message
        if not message:
            return None
        normalized = message.strip().lower()
        for prefix in prefixes:
            if normalized.startswith(prefix):
                return message
        return None

    def _open_error_modal(self, event, title: str, error_message: str, *, retry=None) -> None:
        """Open a modal dialog to display error messages with proper formatting."""
        text_area = TextArea(
            text=error_message,
            read_only=True,
            scrollbar=True,
            wrap_lines=True,
        )
        msg_kb = KeyBindings()

        def _close(app, event_obj=None) -> None:
            self._remove_modal(app)
            if retry is not None:
                retry_event = event_obj
                if retry_event is None:
                    retry_event = SimpleNamespace(app=app)
                retry(retry_event)
            else:
                self.refresh()

        @msg_kb.add("escape")
        def _close_and_reopen_filter(event) -> None:
            _close(event.app, event)

        @msg_kb.add("enter")
        def _close_enter(event) -> None:
            _close(event.app, event)

        tui_modals.merge_text_area_key_bindings(text_area, msg_kb)

        content = HSplit([text_area], padding=0)
        body = Box(body=content, padding=1)
        go_back_button = Button(text="Go back", handler=lambda: _close(event.app))
        dialog = Dialog(title=f"⚠ Error: {title}", body=body, buttons=[go_back_button])
        self._display_modal(
            event.app,
            dialog,
            focus=go_back_button,
            context_type="error",
            width=80,
        )

    def _open_text_modal(self, event, title: str, text: str) -> None:
        target_width = 60
        target_height = 40
        width, height = self._calculate_modal_dimensions(
            event.app,
            target_width=target_width,
            target_height=target_height,
        )
        text_area_height = max(3, height - _CELL_MODAL_CHROME_HEIGHT)

        text_area = TextArea(
            text=text,
            read_only=True,
            scrollbar=True,
            wrap_lines=True,
            height=text_area_height,
        )

        dialog, ok_button = self._build_read_only_modal_dialog(
            app=event.app,
            title=title,
            text_area=text_area,
        )

        self._display_modal(
            event.app,
            dialog,
            focus=ok_button,
            context_type="message",
            width=width,
            height=height,
        )
