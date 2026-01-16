"""
Keymap definitions for the Pulka TUI.

This module centralises prompt_toolkit key bindings so `Screen` stays focused on
orchestration rather than inline binding setup.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings

from pulka_builtin_plugins.freq.plugin import open_frequency_viewer
from pulka_builtin_plugins.transpose.plugin import open_transpose_viewer

from ..core.sheet_traits import resolve_sheet_traits
from ..sheets.commands_sheet import CommandsHelpEntry, key_only_entry

if TYPE_CHECKING:
    from ..core.viewer import Viewer
    from .screen import Screen


def _select_source_viewer(viewers: Sequence[Viewer], column: str) -> Viewer | None:
    """Return the most recent non-derived viewer whose sheet exposes ``column``."""

    for viewer in reversed(viewers):
        if getattr(viewer, "is_hist_view", False) or getattr(viewer, "is_freq_view", False):
            continue
        schema = getattr(viewer.sheet, "schema", {}) or {}
        if column in schema:
            return viewer
    return None


def _bind_key_action(
    kb: KeyBindings,
    *,
    keys: Sequence[str],
    help_keys: str,
    help_action: str,
    help_description: str,
    help_entries: list[CommandsHelpEntry],
    handler: Callable[[Any], None],
    filter: Condition | None = None,
    eager: bool = False,
    add_help: bool = True,
) -> None:
    @kb.add(*keys, filter=filter, eager=eager)
    def _(event):
        handler(event)

    if add_help:
        help_entries.append(key_only_entry(help_keys, help_action, description=help_description))


@dataclass(frozen=True, slots=True)
class KeyOnlyActionSpec:
    keys: tuple[str, ...]
    help_keys: str
    help_action: str
    help_description: str
    handler: str
    filter: str
    eager: bool = False
    add_help: bool = True


KEY_ONLY_ACTION_SPECS = (
    KeyOnlyActionSpec(
        ("escape",),
        "Esc",
        "Modal cancel",
        "Cancel the active modal",
        handler="escape_modal",
        filter="modal_active",
        eager=True,
    ),
    KeyOnlyActionSpec(
        ("c-c",),
        "Ctrl-C",
        "Clear modal input",
        "Clear the active modal input field",
        handler="clear_modal_input",
        filter="modal_input_active",
        eager=True,
    ),
    KeyOnlyActionSpec(
        ("q",),
        "q, Q",
        "Back/quit",
        "Back from derived view; quit at root",
        handler="quit_back",
        filter="modal_inactive",
    ),
    KeyOnlyActionSpec(
        ("Q",),
        "q, Q",
        "Back/quit",
        "Back from derived view; quit at root",
        handler="quit_now",
        filter="always",
        eager=True,
        add_help=False,
    ),
    KeyOnlyActionSpec(
        ("o",),
        "o",
        "File browser open",
        "Open the selected file browser entry",
        handler="open_file_browser_entry",
        filter="file_browser_open",
    ),
    KeyOnlyActionSpec(
        ("c-r",),
        "Ctrl-R",
        "Reload",
        "Reload the active dataset",
        handler="reload_dataset",
        filter="modal_inactive",
        eager=True,
    ),
    KeyOnlyActionSpec(
        ("@",),
        "@",
        "Recorder toggle",
        "Toggle the flight recorder",
        handler="toggle_recorder",
        filter="modal_inactive",
    ),
    KeyOnlyActionSpec(
        (":",),
        ":",
        "Command modal",
        "Open the command prompt",
        handler="open_command_modal",
        filter="modal_inactive",
    ),
    KeyOnlyActionSpec(
        ("!",),
        "!",
        "Shell modal",
        "Open the shell command prompt",
        handler="open_shell_modal",
        filter="modal_inactive",
    ),
    KeyOnlyActionSpec(
        ("x",),
        "x",
        "File delete modal",
        "Open the file delete prompt",
        handler="open_file_delete_modal",
        filter="modal_inactive",
    ),
    KeyOnlyActionSpec(
        ("enter",),
        "Enter",
        "Contextual action",
        "Run the current contextual action",
        handler="enter_action",
        filter="modal_inactive",
    ),
)

_TRANSFORM_IDENTIFIERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _register_key_only_actions(
    kb: KeyBindings,
    screen: Screen,
    help_entries: list[CommandsHelpEntry],
    *,
    modal_active: Condition,
    modal_inactive: Condition,
    file_browser_active: Condition,
    modal_input_active: Condition,
) -> None:
    def _clear_modal_input(event):
        screen._record_key_event(event)
        ctx = screen._modal_manager.context
        field = ctx.get("field") if ctx else None
        if not field or not field.text:
            return
        field.text = ""
        field.buffer.cursor_position = 0
        screen.refresh()

    def _escape_modal(event):
        screen._record_key_event(event)
        ctx = screen._modal_manager.context
        ctx_type = ctx.get("type") if ctx else None
        screen._remove_modal(event.app)
        if ctx:
            if ctx_type == "search":
                screen.viewer.status_message = "search canceled"
            elif ctx_type == "expr_filter":
                screen.viewer.status_message = "filter canceled"
            elif ctx_type == "sql_filter":
                screen.viewer.status_message = "SQL filter canceled"
            elif ctx_type == "transform":
                screen.viewer.status_message = "transform canceled"
            elif ctx_type == "column_search":
                screen.viewer.status_message = "column search canceled"
                screen._clear_column_search()
            elif ctx_type == "command":
                screen.viewer.status_message = "command canceled"
            elif ctx_type == "shell":
                screen.viewer.status_message = "shell command canceled"
            elif ctx_type == "file_change":
                screen._complete_file_change_prompt(reload_file=False)
        screen.refresh()

    def _quit_back(event):
        screen._record_key_event(event)
        # Back if on a derived view; quit if at root
        if len(screen.view_stack) > 1:
            screen._pop_viewer()
            screen.refresh()
        else:
            event.app.exit()

    def _quit_now(event):
        screen._record_key_event(event)
        event.app.exit()

    def _open_file_browser_entry(event):
        screen._record_key_event(event)
        screen._handle_enter(event)

    def _reload_dataset(event):
        screen._record_key_event(event)
        screen._reload_dataset()

    def _open_command_modal(event):
        screen._record_key_event(event)
        screen._open_command_modal(event)

    def _open_shell_modal(event):
        screen._record_key_event(event)
        screen._open_shell_modal(event)

    def _open_file_delete_modal(event):
        screen._record_key_event(event)
        screen._open_file_delete_modal(event)

    def _enter_action(event):
        screen._record_key_event(event)
        if screen._clipboard.is_active():
            screen._handle_enter(event)
            screen.refresh()
            return
        # Preserve frequency view interaction semantics
        if (
            len(screen.view_stack) > 1
            and hasattr(screen.viewer, "is_freq_view")
            and getattr(screen.viewer, "is_freq_view", False)
        ):
            screen._filter_by_pick()
            return
        screen._handle_enter(event)

    handlers = {
        "clear_modal_input": _clear_modal_input,
        "escape_modal": _escape_modal,
        "quit_back": _quit_back,
        "quit_now": _quit_now,
        "open_file_browser_entry": _open_file_browser_entry,
        "reload_dataset": _reload_dataset,
        "toggle_recorder": screen._toggle_recorder,
        "open_command_modal": _open_command_modal,
        "open_shell_modal": _open_shell_modal,
        "open_file_delete_modal": _open_file_delete_modal,
        "enter_action": _enter_action,
    }
    filters = {
        "always": True,
        "modal_active": modal_active,
        "modal_inactive": modal_inactive,
        "file_browser_open": modal_inactive & file_browser_active,
        "modal_input_active": modal_input_active,
    }

    for spec in KEY_ONLY_ACTION_SPECS:
        _bind_key_action(
            kb,
            keys=spec.keys,
            help_keys=spec.help_keys,
            help_action=spec.help_action,
            help_description=spec.help_description,
            help_entries=help_entries,
            handler=handlers[spec.handler],
            filter=filters[spec.filter],
            eager=spec.eager,
            add_help=spec.add_help,
        )


def build_key_bindings(screen: Screen) -> KeyBindings:
    """Return key bindings configured for the provided screen instance."""

    kb = KeyBindings()
    help_entries: list[CommandsHelpEntry] = []
    modal_inactive = Condition(lambda: not screen._modal_manager.active)
    modal_active = ~modal_inactive
    modal_input_active = Condition(
        lambda: bool(
            screen._modal_manager.active
            and screen._modal_manager.context
            and screen._modal_manager.context.get("field")
        )
    )
    region_active = Condition(lambda: screen._clipboard.is_active())
    file_browser_active = Condition(
        lambda: bool(
            getattr(getattr(screen, "viewer", None), "sheet", None)
            and resolve_sheet_traits(screen.viewer.sheet).is_file_browser
        )
    )

    _register_key_only_actions(
        kb,
        screen,
        help_entries,
        modal_active=modal_active,
        modal_inactive=modal_inactive,
        file_browser_active=file_browser_active,
        modal_input_active=modal_input_active,
    )

    @kb.add("escape", filter=modal_inactive & region_active)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._cancel_clipboard_region()
        screen.refresh()

    @kb.add("escape", filter=modal_inactive & ~region_active)
    def _(event):
        screen._record_key_event(event)
        if screen.viewer.clear_status_if_error():
            screen.refresh()

    for digit in range(1, 10):
        key = str(digit)

        @kb.add(key, filter=modal_inactive, eager=True)
        def _(event, digit=digit):
            screen._record_key_event(event)
            screen._append_count_digit(digit)

    # Move
    @kb.add("j", filter=modal_inactive)
    @kb.add("down", filter=modal_inactive)
    def _(event):
        count = screen._consume_count()
        screen._clear_g_buf()
        if count > 1:
            screen._pending_row_delta = 0
            screen.viewer.move_rows(count)
            screen.refresh()
        else:
            screen._queue_move(dr=1)
            screen._invalidate_app()
        screen._record_key_event(event)

    @kb.add("k", filter=modal_inactive)
    @kb.add("up", filter=modal_inactive)
    def _(event):
        count = screen._consume_count()
        screen._clear_g_buf()
        if count > 1:
            screen._pending_row_delta = 0
            screen.viewer.move_rows(-count)
            screen.refresh()
        else:
            screen._queue_move(dr=-1)
            screen._invalidate_app()
        screen._record_key_event(event)

    @kb.add("h", filter=modal_inactive)
    @kb.add("left", filter=modal_inactive)
    def _(event):
        count = screen._consume_count()
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_left", repeat=count)
        screen.refresh()

    @kb.add("H", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("slide_left")
        screen.refresh()

    @kb.add("l", filter=modal_inactive)
    @kb.add("right", filter=modal_inactive)
    def _(event):
        count = screen._consume_count()
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_right", repeat=count)
        screen.refresh()

    @kb.add("L", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("slide_right")
        screen.refresh()

    @kb.add("pageup", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_page_up")
        screen.refresh()

    @kb.add("pagedown", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_page_down")
        screen.refresh()

    @kb.add("J", filter=modal_inactive)
    @kb.add("z", "j", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_half_page_down")
        screen.refresh()

    @kb.add("K", filter=modal_inactive)
    @kb.add("z", "k", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_half_page_up")
        screen.refresh()

    @kb.add("z", "l", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_half_page_right")
        screen.refresh()

    @kb.add("z", "h", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_half_page_left")
        screen.refresh()

    @kb.add("y", "y", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_cell")
        screen.refresh()

    @kb.add("y", "p", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_path")
        screen.refresh()

    @kb.add("y", "c", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_column")
        screen.refresh()

    @kb.add("y", "a", "c", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_all_columns")
        screen.refresh()

    @kb.add("y", "s", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_schema")
        screen.refresh()

    @kb.add("y", "t", "e", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_table_excel")
        screen.refresh()

    @kb.add("y", "t", "m", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_table_markdown")
        screen.refresh()

    @kb.add("y", "t", "a", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_table_ascii")
        screen.refresh()

    @kb.add("y", "t", "u", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("yank_table_unicode")
        screen.refresh()

    @kb.add("g", "g", filter=modal_inactive)  # gg top
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_top")
        screen.refresh(skip_metrics=True)

    @kb.add("g", "h", filter=modal_inactive)  # first column overall
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_column_first_overall")
        screen.refresh()

    @kb.add("g", "l", filter=modal_inactive)  # last column overall
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_column_last_overall")
        screen.refresh()

    @kb.add("g", "H", filter=modal_inactive)  # slide current column to first
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("slide_first")
        screen.refresh()

    @kb.add("g", "L", filter=modal_inactive)  # slide current column to last
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("slide_last")
        screen.refresh()

    @kb.add("g", "_", filter=modal_inactive)  # maximize all columns
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("maximize_all_columns")
        screen.refresh()

    @kb.add("G", filter=modal_inactive)  # bottom (best effort)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_bottom")
        screen.refresh()

    @kb.add("0", filter=modal_inactive)  # first col
    def _(event):
        screen._record_key_event(event)
        if screen._append_count_digit(0):
            return
        screen._clear_g_buf()
        screen._execute_command("move_first_column")
        screen.refresh()

    @kb.add("$", filter=modal_inactive)  # last fully visible col
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("move_last_column")
        screen.refresh()

    @kb.add("_", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("maximize_column")
        screen.refresh()

    @kb.add("z", "z", filter=modal_inactive)  # center current row
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_center_row")
        screen.refresh()

    @kb.add("z", "t", filter=modal_inactive)  # current row to top of viewport
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_row_to_top")
        screen.refresh()

    @kb.add("z", "b", filter=modal_inactive)  # current row to bottom of viewport
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_row_to_bottom")
        screen.refresh()

    @kb.add("z", "T", filter=modal_inactive)  # first visible row
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_viewport_top")
        screen.refresh()

    @kb.add("z", "M", filter=modal_inactive)  # middle visible row
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_viewport_middle")
        screen.refresh()

    @kb.add("z", "B", filter=modal_inactive)  # last visible row
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_viewport_bottom")
        screen.refresh()

    @kb.add("<", filter=modal_inactive)  # prev different value
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_prev_different_value")
        screen.refresh()

    @kb.add(">", filter=modal_inactive)  # next different value
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("move_next_different_value")
        screen.refresh()

    @kb.add("[", filter=modal_inactive)  # sort descending by current column (toggle)
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("sort_desc")
        screen.refresh()

    @kb.add("]", filter=modal_inactive)  # sort ascending by current column (toggle)
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("sort_asc")
        screen.refresh()

    @kb.add("{", filter=modal_inactive)  # stack descending sort by current column (toggle)
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("sort_desc_stack")
        screen.refresh()

    @kb.add("}", filter=modal_inactive)  # stack ascending sort by current column (toggle)
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("sort_asc_stack")
        screen.refresh()

    @kb.add("e", filter=modal_inactive & ~file_browser_active)  # expression filter
    def _(event):
        screen._record_key_event(event)
        screen._open_filter_modal(event)

    @kb.add("E", filter=modal_inactive & ~file_browser_active, eager=True)  # transform modal
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._open_transform_modal(event)

    @kb.add("f", filter=modal_inactive & ~file_browser_active)  # SQL filter
    def _(event):
        screen._record_key_event(event)
        screen._open_sql_filter_modal(event)

    @kb.add("c", filter=modal_inactive)  # column search modal
    def _(event):
        screen._record_key_event(event)
        screen._open_column_search_modal(event)

    @kb.add("|", filter=modal_inactive)  # select rows containing text in current column
    def _(event):
        screen._record_key_event(event)
        screen._open_row_search_modal(event)

    @kb.add("/", filter=modal_inactive)  # search current column
    def _(event):
        screen._record_key_event(event)
        screen._open_search_modal(event)
        screen.refresh()

    @kb.add("\\", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        screen._open_filter_contains_modal(event)
        screen.refresh()

    @kb.add("*", filter=modal_inactive)  # next match for current cell value
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("search_value_next")
        screen.refresh()

    @kb.add("#", filter=modal_inactive)  # previous match for current cell value
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("search_value_prev")
        screen.refresh()

    @kb.add("n", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        if screen._handle_column_search_navigation(forward=True):
            screen.refresh()
            return
        screen._execute_command("search_next_match")
        screen.refresh()

    @kb.add("N", filter=modal_inactive)
    def _(event):
        screen._record_key_event(event)
        if screen._handle_column_search_navigation(forward=False):
            screen.refresh()
            return
        screen._execute_command("search_prev_match")
        screen.refresh()

    @kb.add("r", "r", filter=modal_inactive)  # reset filters/sorts/selection
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("reset")
        screen.refresh()

    @kb.add("r", "e", filter=modal_inactive)  # reset expression filters
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("reset_expr_filter")
        screen.refresh()

    @kb.add("r", "f", filter=modal_inactive)  # reset SQL filters
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("reset_sql_filter")
        screen.refresh()

    @kb.add("r", "s", filter=modal_inactive)  # reset sorts
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("reset_sort")
        screen.refresh()

    for identifier in _TRANSFORM_IDENTIFIERS:

        @kb.add("r", "t", identifier, filter=modal_inactive)  # remove transform by id
        def _(event, identifier=identifier):
            screen._record_key_event(event)
            screen._remove_transform_by_identifier(identifier)
            screen.refresh()

    help_entries.append(
        key_only_entry("rt<id>", "Remove transform", description="Remove transform by id")
    )

    @kb.add("r", "_", filter=modal_inactive)  # reset maximized widths
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("reset_max_columns")
        screen.refresh()

    @kb.add("r", " ", filter=modal_inactive)  # reset selection (alias to gu)
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("clear_selection")
        screen.refresh()

    @kb.add("?", filter=modal_inactive)  # help sheet
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("help_sheet")
        screen.refresh()

    @kb.add("i", filter=modal_inactive)  # toggle insight panel mode
    def _(event):
        screen._record_key_event(event)
        screen.set_insight_panel_mode()

    @kb.add("I", filter=modal_inactive)  # toggle insight panel
    def _(event):
        screen._record_key_event(event)
        screen.set_insight_panel()

    @kb.add("C", filter=modal_inactive)  # column summary (Shift+C)
    def _(event):
        screen._record_key_event(event)
        if not screen.viewer.columns:
            return
        screen._execute_command("summary_sheet")
        screen.refresh()

    @kb.add("F", filter=modal_inactive)  # frequency table of the current column
    def _(event):
        screen._record_key_event(event)
        if not screen.viewer.columns:
            return
        colname = screen.viewer.columns[screen.viewer.cur_col]
        source_viewer = _select_source_viewer(screen.view_stack.viewers, colname)
        if source_viewer is None:
            screen.viewer.status_message = f"frequency view unavailable for column {colname}"
            screen.refresh()
            return
        try:
            screen.viewer = open_frequency_viewer(
                source_viewer,
                colname,
                session=screen.session,
                view_stack=screen.view_stack,
                screen=screen,
            )
        except Exception as exc:
            screen.viewer.status_message = f"freq error: {exc}"[:120]
        screen.refresh()

    @kb.add("t", filter=modal_inactive & ~file_browser_active)  # transpose current row
    def _(event):
        screen._record_key_event(event)
        if not screen.viewer.columns:
            return
        current_row = max(0, getattr(screen.viewer, "cur_row", 0))
        try:
            screen.viewer = open_transpose_viewer(
                screen.viewer,
                session=screen.session,
                view_stack=screen.view_stack,
                sample_rows=1,
                start_row=current_row,
            )
            screen.viewer.status_message = f"transpose row {current_row + 1}"
        except Exception as exc:
            screen.viewer.status_message = f"transpose error: {exc}"[:120]
        screen.refresh()

    @kb.add("T", filter=modal_inactive & ~file_browser_active)  # transpose view (Shift+T)
    def _(event):
        screen._record_key_event(event)
        if not screen.viewer.columns:
            return
        try:
            screen.viewer = open_transpose_viewer(
                screen.viewer,
                session=screen.session,
                view_stack=screen.view_stack,
            )
        except Exception as exc:
            screen.viewer.status_message = f"transpose error: {exc}"[:120]
        screen.refresh()

    @kb.add("d", filter=modal_inactive)  # drop current column
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("drop")
        screen.refresh()

    @kb.add("g", "v", filter=modal_inactive)  # restore dropped columns
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("reset_drop")
        screen.refresh()

    @kb.add("g", "u", filter=modal_inactive)  # clear selection
    def _(event):
        screen._record_key_event(event)
        screen._clear_g_buf()
        screen._execute_command("clear_selection")
        screen.refresh()

    @kb.add("m", "a", filter=modal_inactive)  # materialize active filters/sorts/projection
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("materialize_all")
        screen.refresh()

    @kb.add("m", "m", filter=modal_inactive)  # materialize active filters/sorts/projection
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("materialize_all")
        screen.refresh()

    @kb.add("m", "s", filter=modal_inactive)  # materialize selection
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("materialize_selection")
        screen.refresh()

    @kb.add(",", filter=modal_inactive)  # select all rows matching current value
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("select_same_value")
        screen.refresh()

    @kb.add("+", filter=modal_inactive)  # append filter for current cell value
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("filter_value")
        screen.refresh()

    @kb.add("-", filter=modal_inactive)  # append negative filter for current cell value
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("filter_value_not")
        screen.refresh()

    @kb.add(" ", filter=modal_inactive)  # toggle row selection
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("select_row")
        screen._execute_command("move_down")
        screen.refresh()

    @kb.add("~", filter=modal_inactive)  # invert selection for visible rows
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("invert_selection")
        screen.refresh()

    @kb.add("u", filter=modal_inactive)  # undo last operation
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("undo")
        screen.refresh()

    @kb.add("U", filter=modal_inactive)  # redo last operation
    def _(event):
        screen._record_key_event(event)
        screen._execute_command("redo")
        screen.refresh()

    screen._key_only_help_entries = tuple(help_entries)

    return kb
