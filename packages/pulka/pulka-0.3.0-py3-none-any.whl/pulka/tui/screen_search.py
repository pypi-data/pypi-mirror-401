"""Search and modal flows for the TUI screen."""

from __future__ import annotations

import os
import subprocess
from contextlib import suppress
from pathlib import Path
from typing import Any

from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import Dialog, TextArea

from ..core.sheet_traits import resolve_sheet_traits
from ..core.viewer.ui_hooks import NullViewerUIHooks
from ..data.filter_lang import FilterError
from ..data.transform_lang import TransformError
from ..sheets.file_browser_sheet import file_browser_status_text
from . import modals as tui_modals
from .completions import ColumnNameCompleter, FilesystemPathCompleter


class ScreenSearchController:
    """Owns search/modals and associated histories."""

    def __init__(
        self,
        *,
        screen: Any,
        history_max_size: int,
        format_expr_filters: Any,
    ) -> None:
        self._screen = screen
        self._history_max_size = history_max_size
        self._format_expr_filters = format_expr_filters
        self._search_history: list[str] = []
        self._row_search_history: list[str] = []
        self._filter_contains_history: list[str] = []
        self._expr_filter_history: list[str] = []
        self._sql_filter_history: list[str] = []
        self._transform_history: list[str] = []
        self._command_history: list[str] = ["write output.parquet"]
        self._shell_history: list[str] = []
        self._col_search_history: list[str] = []

    def open_filter_modal(self, event, *, initial_text: str | None = None) -> None:
        screen = self._screen
        title = "Expression Filter"
        prompt_text = "Polars expression (use c.<column>) - Enter: replace existing"
        current_expr_filter = ""
        with suppress(Exception):
            current_expr_filter = self._format_expr_filters(getattr(screen.viewer, "filters", ()))
        default_text = initial_text or current_expr_filter or ""
        if not default_text:
            current_col = None
            with suppress(Exception):
                current_col = screen.viewer.current_colname()
            if current_col:
                if current_col.isidentifier():
                    default_text = f"c.{current_col}"
                else:
                    safe_name = current_col.replace('"', '\\"')
                    default_text = f'c["{safe_name}"]'

        def accept(buff):
            raw_text = buff.text
            text = raw_text.strip()
            if text.lower() == "cancel":
                screen.viewer.status_message = "filter canceled"
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            try:
                args = [text] if text else []
                result = screen._runtime.invoke(
                    "filter_expr",
                    args=args,
                    source="tui",
                    context_mutator=screen._mutate_context,
                    propagate=(FilterError,),
                )
            except FilterError as err:
                screen._open_error_modal(
                    event,
                    "Filter Error",
                    str(err),
                    retry=lambda ev: self.open_filter_modal(ev, initial_text=raw_text),
                )
            except Exception as exc:
                screen._open_error_modal(
                    event,
                    "Unexpected Error",
                    str(exc),
                    retry=lambda ev: self.open_filter_modal(ev, initial_text=raw_text),
                )
            else:
                dispatch = screen._finalise_runtime_result(result)
                status_error = screen._status_error_message(("filter error",))
                error_message = result.message or status_error
                if error_message:
                    screen._open_error_modal(
                        event,
                        "Filter Error",
                        error_message,
                        retry=lambda ev: self.open_filter_modal(ev, initial_text=raw_text),
                    )
                    return True
                if dispatch is not None:
                    self.record_expr_filter(text)
                screen.viewer.status_message = None
                screen._remove_modal(event.app)
                screen.refresh()
            return True

        filter_field = TextArea(
            text=default_text,
            multiline=True,
            height=4,
            accept_handler=accept,
            history=None,
            completer=ColumnNameCompleter(screen.viewer.columns),
            complete_while_typing=True,
        )
        filter_field.buffer.cursor_position = len(default_text)

        tui_modals.bind_enter_to_accept(filter_field)
        body = tui_modals.build_prompt_body(prompt_text, filter_field)
        dialog = Dialog(title=title, body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=filter_field,
            context_type="expr_filter",
            payload={"field": filter_field},
            width=80,
        )

    def open_filter_modal_with_text(self, event, text: str) -> None:
        self.open_filter_modal(event, initial_text=text)

    def open_transform_modal(self, event, *, initial_text: str | None = None) -> None:
        screen = self._screen
        if screen.viewer.plan_controller.current_plan() is None:
            screen.viewer.status_message = "transform unsupported for this view"
            screen.refresh()
            return
        title = "Transform"
        existing_text = getattr(screen.viewer, "_transform_text", None)
        prompt_text = (
            "Polars LazyFrame transform (lf -> LazyFrame) - Enter: replace view"
            if existing_text
            else "Polars LazyFrame transform (lf -> LazyFrame) - Enter: derived view"
        )
        history = InMemoryHistory()
        for item in self._transform_history:
            history.append_string(item)

        default_text = initial_text or "lf"
        if initial_text is None and existing_text:
            default_text = existing_text
        elif initial_text is None:
            current_col = None
            with suppress(Exception):
                current_col = screen.viewer.current_colname()
            if current_col:
                if current_col.isidentifier():
                    default_text = f"lf.with_columns(c.{current_col})"
                else:
                    safe_name = current_col.replace('"', '\\"')
                    default_text = f'lf.with_columns(c["{safe_name}"])'

        def accept(buff):
            raw_text = buff.text
            text = raw_text.strip()
            if text.lower() == "cancel":
                screen.viewer.status_message = "transform canceled"
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            try:
                result = screen._runtime.invoke(
                    "transform_expr",
                    args=[text],
                    source="tui",
                    context_mutator=screen._mutate_context,
                    propagate=(TransformError,),
                )
            except TransformError as err:
                screen._open_error_modal(
                    event,
                    "Transform Error",
                    str(err),
                    retry=lambda ev: self.open_transform_modal(ev, initial_text=raw_text),
                )
            except Exception as exc:
                screen._open_error_modal(
                    event,
                    "Unexpected Error",
                    str(exc),
                    retry=lambda ev: self.open_transform_modal(ev, initial_text=raw_text),
                )
            else:
                dispatch = screen._finalise_runtime_result(result)
                error_message = result.message or screen._status_error_message(("transform error",))
                if error_message:
                    screen._open_error_modal(
                        event,
                        "Transform Error",
                        error_message,
                        retry=lambda ev: self.open_transform_modal(ev, initial_text=raw_text),
                    )
                    return True
                if dispatch is not None:
                    self.record_transform(text)
                screen.viewer.status_message = None
                screen._remove_modal(event.app)
                screen.refresh()
            return True

        transform_field = TextArea(
            text=default_text,
            multiline=True,
            height=6,
            accept_handler=accept,
            history=history,
            completer=ColumnNameCompleter(screen.viewer.columns),
            complete_while_typing=True,
        )
        transform_field.buffer.cursor_position = len(default_text)

        tui_modals.bind_enter_to_accept(transform_field)
        body = tui_modals.build_prompt_body(prompt_text, transform_field)
        dialog = Dialog(title=title, body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=transform_field,
            context_type="transform",
            payload={"field": transform_field},
            width=80,
        )

    def open_sql_filter_modal(self, event, *, initial_text: str | None = None) -> None:
        screen = self._screen
        title = "SQL Filter"
        prompt_text = "SQL WHERE clause (column names only) - Enter: replace existing"
        default_text = initial_text or ""
        if not default_text:
            current_col = None
            with suppress(Exception):
                current_col = screen.viewer.current_colname()
            if current_col:
                if current_col.isidentifier():
                    default_text = current_col
                else:
                    default_text = ColumnNameCompleter._quote_identifier(current_col)

        def accept(buff):
            raw_text = buff.text
            text = raw_text.strip()
            if text.lower() == "cancel":
                screen.viewer.status_message = "SQL filter canceled"
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            args = [text] if text else []
            try:
                result = screen._runtime.invoke(
                    "filter_sql",
                    args=args,
                    source="tui",
                    context_mutator=screen._mutate_context,
                    propagate=(FilterError,),
                )
            except Exception as exc:
                screen._open_error_modal(
                    event,
                    "SQL Filter Error",
                    str(exc),
                    retry=lambda ev: self.open_sql_filter_modal(ev, initial_text=raw_text),
                )
            else:
                dispatch = screen._finalise_runtime_result(result)
                status_error = screen._status_error_message(("sql filter error",))
                error_message = result.message or status_error
                if error_message:
                    screen._open_error_modal(
                        event,
                        "SQL Filter Error",
                        error_message,
                        retry=lambda ev: self.open_sql_filter_modal(ev, initial_text=raw_text),
                    )
                    return True
                if text and dispatch is not None:
                    self.record_sql_filter(text)
                screen.viewer.status_message = None
                screen._remove_modal(event.app)
                screen.refresh()
            return True

        filter_field = TextArea(
            text=default_text,
            multiline=True,
            height=4,
            accept_handler=accept,
            history=None,
            completer=ColumnNameCompleter(screen.viewer.columns, mode="sql"),
            complete_while_typing=True,
        )
        filter_field.buffer.cursor_position = len(default_text)

        tui_modals.bind_enter_to_accept(filter_field)
        body = tui_modals.build_prompt_body(prompt_text, filter_field)
        dialog = Dialog(title=title, body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=filter_field,
            context_type="sql_filter",
            payload={"field": filter_field},
            width=80,
        )

    def open_sql_filter_modal_with_text(self, event, text: str) -> None:
        self.open_sql_filter_modal(event, initial_text=text)

    def open_command_modal(self, event) -> None:
        screen = self._screen
        history = InMemoryHistory()
        for item in self._command_history:
            history.append_string(item)

        def accept(buff):
            raw_text = buff.text
            command_text = raw_text.strip()

            if not command_text:
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            lowered = command_text.split(None, 1)[0].lower()
            if lowered in {"transform", "transform_expr"}:
                screen.viewer.status_message = "transform is available via Shift+E modal"
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            result = screen._runtime.dispatch_raw(
                command_text,
                source="tui",
                context_mutator=screen._mutate_context,
            )
            dispatch = screen._finalise_runtime_result(result)
            if dispatch is not None:
                self.record_command(command_text)
            screen._remove_modal(event.app)
            screen.refresh()
            return True

        command_field = TextArea(
            text="",
            multiline=False,
            accept_handler=accept,
            history=history,
            completer=FilesystemPathCompleter(screen._path_completion_base_dir),
            complete_while_typing=True,
        )
        command_field.buffer.cursor_position = 0

        examples = []
        for spec in screen.commands.iter_specs():
            hints = spec.ui_hints or {}
            example = hints.get("example") if isinstance(hints, dict) else hints.get("example")
            if example:
                examples.append(str(example))
        unique_examples: list[str] = []
        for example in examples:
            if example not in unique_examples:
                unique_examples.append(example)
        prompt = (
            "Command:"
            if not unique_examples
            else f"Command (e.g. {', '.join(unique_examples[:3])}):"
        )

        body = tui_modals.build_prompt_body(prompt, command_field)
        dialog = Dialog(title="Command", body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=command_field,
            context_type="command",
            payload={"field": command_field},
            width=60,
        )

    def open_shell_modal(self, event) -> None:
        screen = self._screen
        if isinstance(screen.viewer.ui_hooks, NullViewerUIHooks):
            screen.viewer.status_message = "shell commands unavailable in headless mode"
            screen.refresh()
            return

        history = InMemoryHistory()
        for item in self._shell_history:
            history.append_string(item)

        def accept(buff):
            raw_text = buff.text
            command_text = raw_text.strip()

            if not command_text:
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            self.record_shell_command(command_text)
            screen._remove_modal(event.app)
            screen.refresh()

            async def _run_shell() -> None:
                try:
                    exit_code = await run_in_terminal(
                        lambda: self._run_shell_command(command_text),
                        in_executor=True,
                    )
                except Exception as exc:
                    screen.viewer.status_message = f"shell error: {exc}"[:120]
                    screen.refresh()
                    return

                screen.viewer.status_message = f"shell exit {exit_code}"
                screen.refresh()

            if event.app is not None:
                event.app.create_background_task(_run_shell())
            else:
                exit_code = self._run_shell_command(command_text)
                screen.viewer.status_message = f"shell exit {exit_code}"
                screen.refresh()
            return True

        command_field = TextArea(
            text="",
            multiline=False,
            accept_handler=accept,
            history=history,
            completer=FilesystemPathCompleter(screen._path_completion_base_dir),
            complete_while_typing=True,
        )
        command_field.buffer.cursor_position = 0
        field_kb = KeyBindings()

        @field_kb.add("tab")
        def _trigger_completion(event) -> None:
            buff = event.current_buffer
            if buff.complete_state is None:
                buff.start_completion(select_first=True)
            buff.complete_next()

        tui_modals.merge_text_area_key_bindings(command_field, field_kb)

        body = tui_modals.build_prompt_body("! command:", command_field)
        dialog = Dialog(title="Shell", body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=command_field,
            context_type="shell",
            payload={"field": command_field},
            width=60,
        )

    def _run_shell_command(self, command_text: str) -> int:
        screen = self._screen
        shell = os.environ.get("SHELL") or "/bin/sh"
        cwd: Path | None = None
        with suppress(Exception):
            base_dir = screen._path_completion_base_dir()
            if base_dir is not None and base_dir.exists():
                cwd = base_dir
        exit_code = 1
        try:
            result = subprocess.run(
                [shell, "-lc", command_text],
                check=False,
                stdin=subprocess.DEVNULL,
                cwd=cwd,
            )
            exit_code = result.returncode
        except FileNotFoundError:
            result = subprocess.run(
                ["/bin/sh", "-lc", command_text],
                check=False,
                stdin=subprocess.DEVNULL,
                cwd=cwd,
            )
            exit_code = result.returncode
        except Exception as exc:
            print(f"shell error: {exc}")

        with suppress(EOFError):
            input("Press Enter to return to Pulka...")
        return exit_code

    def open_row_search_modal(self, event) -> None:
        screen = self._screen

        def accept(buff):
            text = buff.text.strip()
            if not text:
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            if text.lower() == "cancel":
                screen.viewer.status_message = "row selection canceled"
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            try:
                columns = ()
                try:
                    columns = (screen.viewer.columns[screen.viewer.cur_col],)
                except Exception:
                    columns = screen.viewer.columns[:1]
                screen.viewer.select_rows_containing(text, columns=columns)
                self.record_row_search(text)
            except Exception as exc:
                screen.viewer.status_message = f"Row selection error: {exc}"
            screen._remove_modal(event.app)
            screen.refresh()
            return True

        history = InMemoryHistory()
        for item in self._row_search_history:
            history.append_string(item)

        search_field = TextArea(
            text="",
            multiline=False,
            accept_handler=accept,
            history=history,
        )
        search_field.buffer.cursor_position = 0

        body = tui_modals.build_prompt_body(
            "Substring (current column, case-insensitive):",
            search_field,
        )
        dialog = Dialog(title="Select Rows (current column)", body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=search_field,
            context_type="row_search",
            payload={"field": search_field},
            width=60,
        )

    def open_filter_contains_modal(self, event) -> None:
        screen = self._screen

        def accept(buff):
            cleaned_text = buff.text.strip()
            if not cleaned_text:
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            if cleaned_text.lower() == "cancel":
                screen.viewer.status_message = "filter canceled"
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            try:
                sheet = screen.viewer.sheet
                traits = resolve_sheet_traits(sheet)
                if traits.is_file_browser:
                    setter = getattr(sheet, "set_contains_filter", None)
                    if callable(setter):
                        changed = setter(cleaned_text)
                        if changed:
                            self.record_filter_contains(cleaned_text)
                            controller = getattr(screen, "_file_browser_controller", None)
                            if controller is not None:
                                controller.refresh_sheet(sheet, screen.viewer)
                            else:
                                screen.viewer.status_message = file_browser_status_text(sheet)
                            screen.viewer.clamp()
                        else:
                            screen.viewer.status_message = "filter unchanged"
                    else:
                        screen.viewer.status_message = "filtering not supported"
                else:
                    screen.viewer.append_filter_for_contains_text(cleaned_text)
                    self.record_filter_contains(cleaned_text)
            except Exception as exc:
                screen.viewer.status_message = f"filter error: {exc}"
            screen._remove_modal(event.app)
            screen.refresh()
            return True

        history = InMemoryHistory()
        for item in self._filter_contains_history:
            history.append_string(item)

        search_field = TextArea(
            text="",
            multiline=False,
            accept_handler=accept,
            history=history,
        )
        search_field.buffer.cursor_position = 0

        body = tui_modals.build_prompt_body(
            "Substring (current column, case-insensitive):",
            search_field,
        )
        dialog = Dialog(title="Filter Rows (current column)", body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=search_field,
            context_type="filter_contains",
            payload={"field": search_field},
            width=60,
        )

    def open_search_modal(self, event) -> None:
        screen = self._screen

        def accept(buff):
            text = buff.text.strip()
            if text.lower() == "cancel":
                screen.viewer.status_message = "search canceled"
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            # Apply search to the viewer
            try:
                screen.viewer.set_search(text)
                current = screen.viewer.search_text
                screen._clear_column_search()
                self.record_search(text)
                if current:
                    screen.viewer.search(forward=True, include_current=True)
                screen._remove_modal(event.app)
                screen.refresh()
            except Exception as exc:
                screen.viewer.status_message = f"Search error: {exc}"
            return True

        history = InMemoryHistory()
        for item in self._search_history:
            history.append_string(item)

        search_field = TextArea(
            text="",
            multiline=False,
            accept_handler=accept,
            history=history,
        )
        search_field.buffer.cursor_position = 0

        body = tui_modals.build_prompt_body(
            "Substring (current column, case-insensitive):",
            search_field,
        )
        dialog = Dialog(title="Search", body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=search_field,
            context_type="search",
            payload={"field": search_field},
            width=60,
        )

    def open_column_search_modal(self, event) -> None:
        """Open the column search modal with history and tab completion."""
        screen = self._screen

        def accept(buff):
            raw_text = buff.text
            query = raw_text.strip()

            if not query or query.lower() == "cancel":
                screen.viewer.status_message = "column search canceled"
                screen._clear_column_search()
                screen._remove_modal(event.app)
                screen.refresh()
                return True

            screen._remove_modal(event.app)
            success = screen._apply_column_search(query)
            self.record_column_search(query)
            if not success:
                screen._clear_column_search()
            screen.refresh()
            return True

        history = InMemoryHistory()
        for item in self._col_search_history:
            history.append_string(item)

        search_field = TextArea(
            text="",
            multiline=False,
            accept_handler=accept,
            history=history,
            completer=ColumnNameCompleter(screen.viewer.columns, mode="plain"),
            complete_while_typing=True,
        )
        search_field.buffer.cursor_position = 0

        body = tui_modals.build_prompt_body("Column name (prefix or substring):", search_field)
        dialog = Dialog(title="Column Search", body=body, buttons=[])
        screen._display_modal(
            event.app,
            dialog,
            focus=search_field,
            context_type="column_search",
            payload={"field": search_field},
            width=60,
        )

    def record_search(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        with suppress(ValueError):
            self._search_history.remove(text)
        self._search_history.append(text)
        if len(self._search_history) > self._history_max_size:
            del self._search_history[0]

    def record_row_search(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._row_search_history.remove(cleaned)
        self._row_search_history.append(cleaned)
        if len(self._row_search_history) > self._history_max_size:
            del self._row_search_history[0]

    def record_filter_contains(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._filter_contains_history.remove(cleaned)
        self._filter_contains_history.append(cleaned)
        if len(self._filter_contains_history) > self._history_max_size:
            del self._filter_contains_history[0]

    def record_command(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._command_history.remove(cleaned)
        self._command_history.append(cleaned)
        if len(self._command_history) > self._history_max_size:
            del self._command_history[0]

    def record_shell_command(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._shell_history.remove(cleaned)
        self._shell_history.append(cleaned)
        if len(self._shell_history) > self._history_max_size:
            del self._shell_history[0]

    def record_column_search(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._col_search_history.remove(cleaned)
        self._col_search_history.append(cleaned)
        if len(self._col_search_history) > self._history_max_size:
            del self._col_search_history[0]

    def record_expr_filter(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._expr_filter_history.remove(cleaned)
        self._expr_filter_history.append(cleaned)
        if len(self._expr_filter_history) > self._history_max_size:
            del self._expr_filter_history[0]

    def record_sql_filter(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._sql_filter_history.remove(cleaned)
        self._sql_filter_history.append(cleaned)
        if len(self._sql_filter_history) > self._history_max_size:
            del self._sql_filter_history[0]

    def record_transform(self, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        with suppress(ValueError):
            self._transform_history.remove(cleaned)
        self._transform_history.append(cleaned)
        if len(self._transform_history) > self._history_max_size:
            del self._transform_history[0]
