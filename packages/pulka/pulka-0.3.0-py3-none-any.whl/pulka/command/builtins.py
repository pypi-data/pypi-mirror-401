"""
Built-in command handlers for Pulka.

This module contains the standard command handlers that are available in both
TUI and headless modes.
"""

# Import for runtime use
import ast
import hashlib
import os
import shlex
import warnings
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import CancelledError as FutureCancelledError
from contextlib import nullcontext, suppress
from pathlib import Path
from time import monotonic_ns
from typing import Any

from polars.exceptions import PerformanceWarning

from ..clipboard import copy_to_clipboard
from ..core.engine.polars_adapter import PolarsPhysicalPlan, unwrap_physical_plan
from ..core.errors import CancelledError, PulkaCoreError
from ..core.plan import FilterClause, QueryPlan
from ..core.sheet import SHEET_FEATURE_PLAN, SHEET_FEATURE_SLICE, sheet_supports
from ..core.sheet_traits import resolve_display_path, resolve_sheet_traits
from ..core.viewer import Viewer, viewer_public_state
from ..core.viewer.ui_state import inherit_ui_state
from ..data.export import write_view_to_path
from ..data.transform_lang import TransformError, compile_transform
from ..sheets.data_sheet import DataSheet
from ..sheets.file_browser_sheet import file_browser_status_text
from .registry import CommandContext


def register_builtin_commands(registry):
    """Register all built-in commands."""
    # Navigation commands
    registry.register(
        "move_down",
        handle_down,
        "Move cursor down",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register(
        "move_up",
        handle_up,
        "Move cursor up",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register(
        "move_left",
        handle_left,
        "Move cursor left",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register(
        "move_right",
        handle_right,
        "Move cursor right",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register(
        "move_page_down",
        handle_pagedown,
        "Move down by page",
        0,
        repeatable=True,
        aliases=("page_down",),
        domain="Navigation",
    )
    registry.register(
        "move_half_page_down",
        handle_half_pagedown,
        "Move down by half page",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register(
        "move_page_up",
        handle_pageup,
        "Move up by page",
        0,
        repeatable=True,
        aliases=("page_up",),
        domain="Navigation",
    )
    registry.register(
        "move_half_page_right",
        handle_half_pageright,
        "Move right by half page",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register(
        "move_half_page_left",
        handle_half_pageleft,
        "Move left by half page",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register(
        "move_half_page_up",
        handle_half_pageup,
        "Move up by half page",
        0,
        repeatable=True,
        domain="Navigation",
    )
    registry.register("move_top", handle_top, "Go to top", 0, domain="Navigation")
    registry.register("move_bottom", handle_bottom, "Go to bottom", 0, domain="Navigation")
    registry.register(
        "move_first_column",
        handle_first,
        "Go to first column",
        0,
        domain="Navigation",
    )
    registry.register(
        "move_last_column",
        handle_last,
        "Go to last column",
        0,
        domain="Navigation",
    )
    registry.register(
        "move_viewport_top",
        handle_viewport_top,
        "Go to the first visible row",
        0,
        aliases=("zT",),
        domain="Navigation",
    )
    registry.register(
        "move_viewport_middle",
        handle_viewport_middle,
        "Go to the middle visible row",
        0,
        aliases=("zM",),
        domain="Navigation",
    )
    registry.register(
        "move_viewport_bottom",
        handle_viewport_bottom,
        "Go to the last visible row",
        0,
        aliases=("zB",),
        domain="Navigation",
    )
    registry.register(
        "slide_left",
        handle_slide_left,
        "Slide current column left",
        0,
        domain="Navigation",
    )
    registry.register(
        "slide_right",
        handle_slide_right,
        "Slide current column right",
        0,
        domain="Navigation",
    )
    registry.register(
        "slide_first",
        handle_slide_first,
        "Slide current column to first",
        0,
        domain="Navigation",
    )
    registry.register(
        "slide_last",
        handle_slide_last,
        "Slide current column to last",
        0,
        domain="Navigation",
    )

    # View commands
    registry.register(
        "sort_asc",
        handle_sort_asc,
        "Sort ascending by current column (toggle)",
        0,
        domain="View",
    )
    registry.register(
        "sort_desc",
        handle_sort_desc,
        "Sort descending by current column (toggle)",
        0,
        domain="View",
    )
    registry.register(
        "sort_asc_stack",
        handle_sort_asc_stack,
        "Stack ascending sort on current column (toggle)",
        0,
        domain="View",
    )
    registry.register(
        "sort_desc_stack",
        handle_sort_desc_stack,
        "Stack descending sort on current column (toggle)",
        0,
        domain="View",
    )
    registry.register(
        "filter_expr",
        handle_filter,
        "Apply expression filter",
        -1,
        domain="Filter",
        ui_hints={"example": 'filter_expr c["price"] > 5'},
    )
    registry.register(
        "filter_value",
        handle_filter_value,
        "Append filter for current cell value",
        0,
        domain="Filter",
    )
    registry.register(
        "filter_value_not",
        handle_filter_value_not,
        "Append negative filter for current cell value",
        0,
        domain="Filter",
    )
    registry.register(
        "filter_sql",
        handle_sql_filter,
        "Apply SQL filter",
        -1,
        domain="Filter",
        ui_hints={"example": "filter_sql SELECT * FROM data WHERE price > 5"},
    )
    registry.register(
        "reset",
        handle_reset,
        "Reset filters, sorts, and selection",
        0,
        aliases=("rr",),
        domain="View",
    )
    registry.register(
        "reset_expr_filter",
        handle_reset_expression_filter,
        "Clear expression filters",
        0,
        aliases=("re",),
        domain="Filter",
    )
    registry.register(
        "reset_sql_filter",
        handle_reset_sql_filter,
        "Clear SQL filters",
        0,
        aliases=("rf",),
        domain="Filter",
    )
    registry.register(
        "reset_sort",
        handle_reset_sort,
        "Clear sorting",
        0,
        aliases=("rs",),
        domain="View",
    )
    registry.register(
        "transform_expr",
        handle_transform,
        "Apply a Polars LazyFrame transform into a derived sheet",
        1,
        argument_mode="single",
        domain="Transform",
        ui_hints={"example": 'transform_expr lf.with_columns(pl.lit(1).alias("x"))'},
    )
    registry.register(
        "move_to_column",
        handle_goto,
        "Go to column",
        1,
        domain="Navigation",
        ui_hints={"example": "move_to_column revenue"},
    )
    registry.register(
        "render",
        handle_render,
        "Render current view",
        0,
        aliases=("print",),
        domain="View",
        ui_hints={"example": "render", "force_render": True, "hidden": True},
    )
    registry.register(
        "freeze",
        handle_freeze,
        "Freeze rows or columns",
        1,
        domain="View",
        ui_hints={"example": "freeze c2"},
    )
    registry.register(
        "unfreeze",
        handle_unfreeze,
        "Clear frozen rows and columns",
        0,
        domain="View",
    )

    # Column operations
    registry.register("drop", handle_hide, "Drop current column", 0, domain="Column")
    registry.register(
        "reset_drop",
        handle_unhide,
        "Restore all dropped columns",
        0,
        aliases=("rd",),
        domain="Column",
    )
    registry.register(
        "select_row",
        handle_select_row,
        "Toggle selection for current row",
        0,
        aliases=(" ",),
        domain="Selection",
    )
    registry.register(
        "invert_selection",
        handle_invert_selection,
        "Invert selection for visible rows",
        0,
        domain="Selection",
    )
    registry.register(
        "clear_selection",
        handle_clear_selection,
        "Clear all selected rows",
        0,
        domain="Selection",
    )
    registry.register(
        "materialize_all",
        handle_materialize_all,
        "Materialize active filters/sorts/projection into a new sheet",
        0,
        aliases=("ma", "mm"),
        domain="Sheets",
    )
    registry.register(
        "materialize_selection",
        handle_materialize_selection,
        "Materialize the current selection into a new sheet",
        0,
        aliases=("ms",),
        domain="Sheets",
    )
    registry.register(
        "select_same_value",
        handle_select_same_value,
        "Select rows matching the current cell value",
        0,
        domain="Selection",
    )
    registry.register(
        "select_contains",
        handle_select_contains,
        "Select rows where any column contains the given text",
        1,
        domain="Selection",
        ui_hints={"example": "select_contains error"},
    )
    registry.register(
        "filter_contains",
        handle_filter_contains,
        "Append a contains filter on the current column",
        1,
        domain="Filter",
    )
    registry.register("undo", handle_undo, "Undo last operation", 0, domain="Transform")
    registry.register("redo", handle_redo, "Redo last operation", 0, domain="Transform")

    # Clipboard commands
    registry.register(
        "yank_cell",
        handle_yank_cell,
        "Copy the active cell to the clipboard",
        0,
        aliases=("yy",),
        domain="Clipboard",
    )
    registry.register(
        "yank_path",
        handle_yank_path,
        "Copy the current dataset path to the clipboard",
        0,
        aliases=("yp",),
        domain="Clipboard",
    )
    registry.register(
        "yank_column",
        handle_yank_column,
        "Copy the current column name to the clipboard",
        0,
        aliases=("yc",),
        domain="Clipboard",
    )
    registry.register(
        "yank_all_columns",
        handle_yank_all_columns,
        "Copy visible column names as a Python list",
        0,
        aliases=("yac",),
        domain="Clipboard",
    )
    registry.register(
        "yank_schema",
        handle_yank_schema,
        "Copy the current schema mapping to the clipboard",
        0,
        aliases=("ys",),
        domain="Clipboard",
    )
    registry.register(
        "yank_table_excel",
        handle_yank_table_excel,
        "Copy a viewport region to the clipboard for Excel",
        0,
        aliases=("yte",),
        domain="Clipboard",
    )
    registry.register(
        "yank_table_markdown",
        handle_yank_table_markdown,
        "Copy a viewport region to the clipboard as Markdown",
        0,
        aliases=("ytm",),
        domain="Clipboard",
    )
    registry.register(
        "yank_table_ascii",
        handle_yank_table_ascii,
        "Copy a viewport region to the clipboard as an ASCII table",
        0,
        aliases=("yta",),
        domain="Clipboard",
    )
    registry.register(
        "yank_table_unicode",
        handle_yank_table_unicode,
        "Copy a viewport region to the clipboard as a Unicode table",
        0,
        aliases=("ytu",),
        domain="Clipboard",
    )

    # Maximize operations
    registry.register(
        "maximize_column",
        handle_maxcol,
        "Toggle maximize current column",
        0,
        domain="View",
    )
    registry.register(
        "maximize_all_columns",
        handle_maxall,
        "Toggle maximize all columns",
        0,
        domain="View",
    )
    registry.register(
        "reset_max_columns",
        handle_resetmax,
        "Reset maximized column widths",
        0,
        domain="View",
    )

    # Export commands
    registry.register(
        "write",
        handle_write,
        "Export the active view to disk",
        -1,
        aliases=("w",),
        domain="Export",
        ui_hints={"example": "write output.parquet"},
    )

    # Repro export command
    registry.register(
        "repro_export",
        handle_repro_export,
        "Export reproducible dataset slice",
        -1,
        domain="Export",
    )

    # Sheet navigation commands
    registry.register("schema", handle_schema, "Show column schema", 0, domain="Help")
    registry.register(
        "help_sheet",
        handle_commands,
        "Show help sheet",
        0,
        aliases=("help", "commands"),
        domain="Help",
    )
    registry.register(
        "status",
        handle_status,
        "Show status message history",
        0,
        domain="Help",
    )
    registry.register(
        "cd",
        handle_cd,
        "Change working directory",
        1,
        domain="File Browser",
        ui_hints={"example": "cd ./data"},
    )
    registry.register(
        "file_browser_sheet",
        handle_browse,
        "Open directory browser",
        -1,
        aliases=("browse", "b", "browser"),
        domain="File Browser",
        ui_hints={"example": "file_browser_sheet ~/data"},
    )
    registry.register(
        "insight",
        handle_insight,
        "Toggle insight sidecar in the TUI",
        -1,
        domain="View",
    )

    # Search commands
    registry.register("search", handle_search, "Search current column", 1, domain="Search")
    registry.register(
        "search_next_match",
        handle_next_diff,
        "Next search match",
        0,
        domain="Search",
    )
    registry.register(
        "search_prev_match",
        handle_prev_diff,
        "Previous search match",
        0,
        domain="Search",
    )
    registry.register(
        "search_value_next",
        handle_search_value_next,
        "Search forward for the current cell value",
        0,
        domain="Search",
    )
    registry.register(
        "search_value_prev",
        handle_search_value_prev,
        "Search backward for the current cell value",
        0,
        domain="Search",
    )

    # Navigation enhancement commands
    registry.register(
        "move_center_row",
        handle_center,
        "Center current row",
        0,
        domain="Navigation",
    )
    registry.register(
        "move_row_to_top",
        handle_row_top,
        "Scroll current row to top of viewport",
        0,
        aliases=("zt",),
        domain="Navigation",
    )
    registry.register(
        "move_row_to_bottom",
        handle_row_bottom,
        "Scroll current row to bottom of viewport",
        0,
        aliases=("zb",),
        domain="Navigation",
    )
    registry.register(
        "move_next_different_value",
        handle_next_different,
        "Next different value",
        0,
        domain="Navigation",
    )
    registry.register(
        "move_prev_different_value",
        handle_prev_different,
        "Previous different value",
        0,
        domain="Navigation",
    )

    # Column navigation commands
    registry.register(
        "move_column_first_overall",
        handle_first_overall,
        "Go to first column overall",
        0,
        domain="Navigation",
    )
    registry.register(
        "move_column_last_overall",
        handle_last_overall,
        "Go to last column overall",
        0,
        domain="Navigation",
    )

    # Aliases
    registry.register_alias("_", "maximize_column")
    registry.register_alias("g_", "maximize_all_columns")
    registry.register_alias("repro", "repro_export")
    registry.register_alias("?", "help_sheet")
    registry.register_alias("/", "search")
    registry.register_alias("\\", "filter_contains")
    registry.register_alias("h", "move_left")
    registry.register_alias("j", "move_down")
    registry.register_alias("k", "move_up")
    registry.register_alias("l", "move_right")
    registry.register_alias("[", "sort_desc")
    registry.register_alias("]", "sort_asc")
    registry.register_alias("{", "sort_desc_stack")
    registry.register_alias("}", "sort_asc_stack")
    registry.register_alias("|", "select_contains")
    registry.register_alias("n", "search_next_match")
    registry.register_alias("N", "search_prev_match")
    registry.register_alias("*", "search_value_next")
    registry.register_alias("#", "search_value_prev")
    registry.register_alias("zz", "move_center_row")
    registry.register_alias("<", "move_prev_different_value")
    registry.register_alias(">", "move_next_different_value")
    registry.register_alias("gh", "move_column_first_overall")
    registry.register_alias("gl", "move_column_last_overall")
    registry.register_alias("H", "slide_left")
    registry.register_alias("L", "slide_right")
    registry.register_alias("d", "drop")
    registry.register_alias("-", "filter_value_not")
    registry.register_alias("c", "move_to_column")
    registry.register_alias("E", "transform_expr")
    registry.register_alias("u", "undo")
    registry.register_alias("U", "redo")
    registry.register_alias("e", "filter_expr")
    registry.register_alias("f", "filter_sql")
    registry.register_alias("gH", "slide_first")
    registry.register_alias("gL", "slide_last")
    registry.register_alias("0", "move_first_column")
    registry.register_alias("$", "move_last_column")
    registry.register_alias("gg", "move_top")
    registry.register_alias("G", "move_bottom")
    registry.register_alias("J", "move_half_page_down")
    registry.register_alias("K", "move_half_page_up")
    registry.register_alias("zj", "move_half_page_down")
    registry.register_alias("zk", "move_half_page_up")
    registry.register_alias("zl", "move_half_page_right")
    registry.register_alias("zh", "move_half_page_left")
    registry.register_alias("i", "insight")
    registry.register_alias("~", "invert_selection")
    registry.register_alias("r ", "clear_selection")
    registry.register_alias("r_", "reset_max_columns")
    registry.register_alias(",", "select_same_value")
    registry.register_alias("+", "filter_value")

    # Summary command is provided by the built-in plugin; ensure it is available headless.
    try:
        from pulka_builtin_plugins.summary.plugin import _summary_cmd
    except Exception:  # pragma: no cover - plugin import guard
        pass
    else:
        with registry.provider_scope("pulka-summary"):
            registry.register(
                "summary_sheet",
                _summary_cmd,
                "Column summary sheet",
                0,
                aliases=("summary", "columns", "C"),
                domain="Sheets",
            )

    # Frequency command is provided by the built-in plugin; ensure it is available headless.
    try:
        from pulka_builtin_plugins.freq.plugin import _freq_cmd
    except Exception:  # pragma: no cover - plugin import guard
        pass
    else:
        with registry.provider_scope("pulka-freq"):
            registry.register(
                "frequency_sheet",
                _freq_cmd,
                "Frequency table of current column",
                -1,
                aliases=("freq", "F"),
                domain="Sheets",
            )

    # File operations (file browser)
    registry.register(
        "copy",
        handle_copy_file,
        "Copy focused/selected file(s) to destination path",
        1,
        domain="File Browser",
        ui_hints={"example": "copy ./backup/"},
    )
    registry.register_alias("cp", "copy")
    registry.register(
        "move",
        handle_move_file,
        "Move focused/selected file(s) to destination path",
        1,
        domain="File Browser",
        ui_hints={"example": "move ../archive/old.csv"},
    )
    registry.register(
        "rename",
        handle_rename_file,
        "Rename focused/selected item within current directory",
        1,
        domain="File Browser",
        ui_hints={"example": "rename new_name.parquet"},
    )
    registry.register(
        "mkdir",
        handle_mkdir,
        "Create a directory relative to the current browser path",
        1,
        domain="File Browser",
        ui_hints={"example": "mkdir new_folder/subdir"},
    )
    registry.register_alias("mv", "move")


def _snapshot_state(viewer: Any):
    """Return a public snapshot for ``viewer`` when supported."""

    return viewer_public_state(viewer)


def _resolve_session(context: CommandContext):
    """Return the active session when available from context or viewer."""

    session = getattr(context, "session", None)
    if session is not None:
        return session
    viewer = getattr(context, "viewer", None)
    if viewer is not None:
        return getattr(viewer, "session", None)
    return None


def _materialize_plan(viewer: Viewer, plan: QueryPlan) -> DataSheet | None:
    """Compile ``plan`` to a new DataSheet with fresh row ids."""

    compiler = viewer.engine.build_plan_compiler()
    if compiler is None:
        viewer.status_message = "materialize unsupported for this sheet"
        return None

    try:
        physical_plan = compiler.compile(plan)
    except PulkaCoreError as exc:
        viewer._status_from_error("materialize", exc)
        return None
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"materialize error: {exc}"[:120]
        return None

    try:
        polars_plan = unwrap_physical_plan(physical_plan)
        lazy_frame = polars_plan.to_lazyframe()
        row_id_column = getattr(viewer.row_provider, "_row_id_column", None)
        if row_id_column:
            try:
                schema = lazy_frame.collect_schema()
            except Exception:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=PerformanceWarning)
                    schema = getattr(lazy_frame, "schema", {})
            if row_id_column in schema:
                with suppress(Exception):
                    lazy_frame = lazy_frame.drop([row_id_column])
        materialized = PolarsPhysicalPlan(
            lazy_frame,
            source_kind=polars_plan.source_kind,
            source_path=polars_plan.source_path,
        )
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"materialize error: {exc}"[:120]
        return None

    projection = plan.projection_or(viewer.columns)
    row_id_column = getattr(viewer.row_provider, "_row_id_column", None)
    columns = [name for name in projection if row_id_column is None or name != row_id_column]
    if not columns:
        columns = [
            name for name in viewer.columns if row_id_column is None or name != row_id_column
        ]

    try:
        return DataSheet(materialized, runner=viewer.job_runner, columns=columns)
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"materialize error: {exc}"[:120]
        return None


def _derived_viewer_kwargs(session, base_viewer: Viewer) -> dict[str, object]:
    return {
        "viewport_rows": getattr(base_viewer, "_viewport_rows_override", None),
        "viewport_cols": getattr(base_viewer, "_viewport_cols_override", None),
        "source_path": getattr(base_viewer, "_source_path", None),
        "session": session,
        "ui_hooks": session.view_stack.ui_hooks,
        "status_durations": getattr(session, "_status_duration_overrides", {}),
    }


def _prepare_derived_viewer(session, base_viewer: Viewer, sheet: DataSheet) -> Viewer:
    child_viewer = Viewer(
        sheet,
        runner=session.job_runner,
        **_derived_viewer_kwargs(session, base_viewer),
    )
    inherit_ui_state(base_viewer, child_viewer)
    if getattr(base_viewer, "_pulka_has_real_source_path", False):
        child_viewer._pulka_has_real_source_path = True  # type: ignore[attr-defined]
    return child_viewer


def _push_materialized_viewer(
    session, base_viewer: Viewer, sheet: DataSheet, status: str
) -> Viewer | None:
    """Push ``sheet`` as a new viewer derived from ``base_viewer``."""

    child_viewer = _prepare_derived_viewer(session, base_viewer, sheet)
    session.push_viewer(child_viewer)
    with suppress(Exception):
        session.command_runtime.prepare_viewer(child_viewer)
    child_viewer.status_message = status
    return child_viewer


def _replace_materialized_viewer(
    session, base_viewer: Viewer, sheet: DataSheet, status: str
) -> Viewer | None:
    """Replace the active viewer with ``sheet`` while keeping stack depth."""

    child_viewer = _prepare_derived_viewer(session, base_viewer, sheet)
    session.view_stack.replace_active(child_viewer)
    with suppress(Exception):
        session.command_runtime.prepare_viewer(child_viewer)
    child_viewer.status_message = status
    return child_viewer


def handle_transform(context: CommandContext, args: list[str]) -> None:
    """Apply a Polars LazyFrame transform and open it as a derived sheet."""

    viewer = context.viewer
    session = _resolve_session(context)
    if session is None:
        viewer.status_message = "transform unavailable (no session)"
        return

    if not args:
        viewer.status_message = "transform requires an expression"
        return

    expr = args[0].strip()
    if not expr:
        viewer.status_message = "transform requires an expression"
        return

    plan = viewer.plan_controller.current_plan()
    if plan is None:
        viewer.status_message = "transform unsupported for this sheet"
        return

    lazy_frame, polars_plan = _lazyframe_for_plan(viewer, plan, op="transform")
    if lazy_frame is None or polars_plan is None:
        return

    compile_columns = _columns_from_lazyframe(
        lazy_frame, row_id_column=getattr(viewer.row_provider, "_row_id_column", None)
    )
    try:
        transform_fn = compile_transform(expr, compile_columns or viewer.columns)
    except TransformError as exc:
        viewer.status_message = f"transform error: {exc}"[:120]
        return
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"transform error: {exc}"[:120]
        return

    try:
        transformed = transform_fn(lazy_frame)
    except TransformError as exc:
        viewer.status_message = f"transform error: {exc}"[:120]
        return
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"transform error: {exc}"[:120]
        return

    row_id_column = getattr(viewer.row_provider, "_row_id_column", None)
    columns = _columns_from_lazyframe(transformed, row_id_column=row_id_column)
    if not columns:
        columns = [
            name for name in viewer.columns if row_id_column is None or name != row_id_column
        ]

    try:
        sheet = DataSheet(
            PolarsPhysicalPlan(
                transformed,
                source_kind=getattr(polars_plan, "source_kind", None),
                source_path=getattr(polars_plan, "source_path", None),
            ),
            runner=viewer.job_runner,
            columns=columns,
        )
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"transform error: {exc}"[:120]
        return

    hash_fragment = hashlib.sha256(expr.encode("utf-8")).hexdigest()[:7]
    replace_active = getattr(viewer, "_transform_text", None) is not None
    depth = viewer.stack_depth if replace_active else viewer.stack_depth + 1
    status = f"transform_expr -> depth {depth} (xf:{hash_fragment})"
    if replace_active:
        child = _replace_materialized_viewer(session, viewer, sheet, status)
    else:
        child = _push_materialized_viewer(session, viewer, sheet, status)
    if child is not None:
        child._transform_text = expr  # type: ignore[attr-defined]
        child._transform_hash = hash_fragment  # type: ignore[attr-defined]


def handle_down(context: CommandContext, args):
    """Move cursor down one row."""
    recorder = getattr(context, "recorder", None)
    if recorder and recorder.enabled:
        before_state = _snapshot_state(context.viewer)
        if before_state is None:
            context.viewer.move_down(1)
            return
        fallback_total_rows = getattr(context.viewer, "_total_rows", None)
        start_ns = monotonic_ns()
        context.viewer.move_down(1)
        duration_ms = (monotonic_ns() - start_ns) / 1_000_000
        after_state = _snapshot_state(context.viewer)
        if after_state is None:  # pragma: no cover - defensive
            after_state = before_state
        before_row = before_state.cursor.row
        before_row0 = before_state.viewport.row0
        after_row = after_state.cursor.row
        after_row0 = after_state.viewport.row0
        view_height = before_state.visible_row_count or after_state.visible_row_count
        payload = {
            "before_row": before_row,
            "before_row0": before_row0,
            "after_row": after_row,
            "after_row0": after_row0,
            "view_height": view_height,
            "scrolled": after_row0 != before_row0,
        }
        total_rows = (
            before_state.total_rows
            if before_state.total_rows is not None
            else after_state.total_rows
        )
        if total_rows is None:
            total_rows = (
                fallback_total_rows
                if fallback_total_rows is not None
                else after_state.visible_row_count
            )
        if total_rows is not None:
            payload["total_rows"] = total_rows
            payload["hit_bottom"] = after_row >= max(0, total_rows - 1)
        recorder.record_perf(phase="move.down", duration_ms=duration_ms, payload=payload)
        return

    context.viewer.move_down(1)


def _file_browser_required(context: CommandContext) -> bool:
    viewer = getattr(context, "viewer", None)
    sheet = getattr(viewer, "sheet", None)
    if sheet is None or not resolve_sheet_traits(sheet).is_file_browser:
        if viewer is not None:
            viewer.status_message = "command only available in file browser"
        return False
    return True


def _reset_file_browser_filter(context: CommandContext) -> bool:
    viewer = getattr(context, "viewer", None)
    if viewer is None:
        return False
    sheet = getattr(viewer, "sheet", None)
    if sheet is None or not resolve_sheet_traits(sheet).is_file_browser:
        return False

    clear = getattr(sheet, "clear_filter", None)
    cleared = False
    if callable(clear):
        with suppress(Exception):
            cleared = bool(clear())
    if cleared:
        builder = getattr(sheet, "at_path", None)
        directory = getattr(sheet, "directory", None)
        if callable(builder) and directory is not None:
            with suppress(Exception):
                new_sheet = builder(directory)
                source_label = resolve_display_path(new_sheet, fallback=str(directory))
                viewer.replace_sheet(new_sheet, source_path=source_label)
                sheet = new_sheet
    provider = getattr(viewer, "row_provider", None)
    if provider is not None:
        with suppress(Exception):
            provider.clear()
    with suppress(Exception):
        viewer.invalidate_row_cache()
    with suppress(Exception):
        viewer._sync_hidden_columns_from_plan()
    with suppress(Exception):
        tracker = viewer.row_count_tracker
        tracker.invalidate()
        tracker.ensure_total_rows()
    viewer.status_message = file_browser_status_text(sheet)
    return True


def _navigation_viewer(context: CommandContext) -> Viewer | None:
    """Return the active viewer for navigation commands."""

    return getattr(context, "viewer", None)


def _body_view_height(viewer: Viewer) -> int:
    body_height = getattr(viewer, "_body_view_height", None)
    if not callable(body_height):
        return 1
    try:
        value = int(body_height())
    except (TypeError, ValueError):
        return 1
    return max(1, value)


def _resolve_transfer_path(raw: str, base_dir: Path) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    try:
        return path.resolve()
    except Exception:
        return path.absolute()


def _parse_file_transfer_args(
    context: CommandContext, args: list[str], *, command: str
) -> tuple[str, list[Path] | None] | None:
    viewer = context.viewer
    if not args:
        viewer.status_message = f"{command} requires a destination path"
        return None

    raw = args[0].strip()
    if not raw:
        viewer.status_message = f"{command} requires a destination path"
        return None

    try:
        parts = shlex.split(raw)
    except ValueError as exc:
        viewer.status_message = f"{command} args invalid: {exc}"[:120]
        return None

    if not parts:
        viewer.status_message = f"{command} requires a destination path"
        return None

    if len(parts) == 1:
        return parts[0], None

    sheet = getattr(viewer, "sheet", None)
    base_dir = Path(getattr(sheet, "directory", Path.cwd()))
    first_path = _resolve_transfer_path(parts[0], base_dir)
    if not first_path.exists():
        return raw, None

    source_paths: list[Path] = []
    for token in parts[:-1]:
        path = _resolve_transfer_path(token, base_dir)
        if not path.exists():
            viewer.status_message = f"source not found: {token}"[:120]
            return None
        source_paths.append(path)
    return parts[-1], source_paths


def handle_copy_file(context: CommandContext, args):
    """Copy focused/selected file(s) to destination path."""

    if not _file_browser_required(context):
        return
    parsed = _parse_file_transfer_args(context, args, command="copy")
    if parsed is None:
        return
    dest, source_paths = parsed
    screen = getattr(context, "screen", None)
    if screen is None:
        context.viewer.status_message = "copy requires TUI"
        return
    screen._request_file_transfer("copy", dest, source_paths=source_paths)


def handle_move_file(context: CommandContext, args):
    """Move focused/selected file(s) to destination path."""

    if not _file_browser_required(context):
        return
    parsed = _parse_file_transfer_args(context, args, command="move")
    if parsed is None:
        return
    dest, source_paths = parsed
    screen = getattr(context, "screen", None)
    if screen is None:
        context.viewer.status_message = "move requires TUI"
        return
    screen._request_file_transfer("move", dest, source_paths=source_paths)


def handle_rename_file(context: CommandContext, args):
    """Rename the focused/selected item within the current directory."""

    if not _file_browser_required(context):
        return
    if not args:
        context.viewer.status_message = "rename requires a new name"
        return

    new_name = args[0]
    screen = getattr(context, "screen", None)
    if screen is None:
        context.viewer.status_message = "rename requires TUI"
        return
    screen._request_file_rename(new_name)


def handle_mkdir(context: CommandContext, args):
    """Create a directory relative to the current browser path."""

    if not _file_browser_required(context):
        return
    if not args:
        context.viewer.status_message = "mkdir requires a destination path"
        return

    dest = args[0]
    screen = getattr(context, "screen", None)
    if screen is None:
        context.viewer.status_message = "mkdir requires TUI"
        return
    screen._request_file_mkdir(dest)


def _resolve_active_cell_display(
    viewer: Any, *, max_chars: int | None = 4096
) -> tuple[str, str] | None:
    """Return the display text for the active cell.

    When ``max_chars`` is ``None`` the raw value is returned without truncation.
    """

    columns = list(getattr(viewer, "columns", ()) or ())
    if not columns:
        return None

    cur_col = getattr(viewer, "cur_col", 0)
    if cur_col < 0 or cur_col >= len(columns):
        return None

    cur_row = getattr(viewer, "cur_row", 0)
    column_name = columns[cur_col]
    sheet = getattr(viewer, "sheet", None)
    if sheet is None or not sheet_supports(sheet, SHEET_FEATURE_SLICE):
        return None

    try:
        table_slice = sheet.fetch_slice(cur_row, 1, [column_name])
    except Exception:
        return None

    if getattr(table_slice, "height", 0) <= 0:
        return None

    try:
        column = table_slice.column(column_name)
    except Exception:
        return None

    limit = 0 if max_chars is None else max(0, max_chars)
    formatted_text: str | None = None
    formatter = getattr(column, "formatted", None)
    if callable(formatter) and max_chars is not None:
        try:
            formatted_values = formatter(limit if limit > 0 else 0)
        except Exception:
            formatted_values = ()
        if formatted_values:
            formatted_text = formatted_values[0]

    if formatted_text is None:
        values = getattr(column, "values", ())
        try:
            raw_value = values[0]
        except Exception:
            raw_value = None
        formatted_text = "" if raw_value is None else str(raw_value)

    return column_name, formatted_text


def _resolve_active_dataset_path(context: CommandContext) -> Path | None:
    """Best-effort resolver for the active dataset path."""

    session = getattr(context, "session", None)
    if session is not None:
        dataset_path = getattr(session, "dataset_path", None)
        if dataset_path is not None:
            return _normalise_path(dataset_path)

    viewer = getattr(context, "viewer", None)
    if viewer is None:
        return None
    source = getattr(viewer, "_source_path", None)
    if isinstance(source, Path):
        return _normalise_path(source)
    if isinstance(source, str) and source and not source.startswith("<"):
        return _normalise_path(Path(source))
    return None


def _normalise_path(path: Path) -> Path:
    candidate = path
    with suppress(Exception):
        candidate = candidate.expanduser()
    try:
        return candidate.resolve()
    except Exception:
        return candidate


def _cd_base_directory(context: CommandContext) -> Path:
    """Return the base directory for resolving :cd targets."""

    viewer = getattr(context, "viewer", None)
    sheet = getattr(viewer, "sheet", None)
    directory = getattr(sheet, "directory", None) if sheet is not None else None
    if directory is not None:
        try:
            return _normalise_path(Path(directory))
        except Exception:
            pass

    session = _resolve_session(context)
    override = getattr(session, "command_cwd", None) if session is not None else None
    if override is not None:
        try:
            return _normalise_path(Path(override))
        except Exception:
            pass

    dataset_path = _resolve_active_dataset_path(context)
    if dataset_path is not None:
        return dataset_path if dataset_path.is_dir() else dataset_path.parent

    try:
        return Path.cwd()
    except Exception:
        return Path()


def _resolve_current_column(viewer: Any) -> str | None:
    if viewer is None:
        return None
    columns = getattr(viewer, "columns", None)
    if not columns:
        return None
    try:
        return viewer.current_colname()
    except Exception:
        pass
    try:
        cur_col = getattr(viewer, "cur_col", 0)
        return columns[cur_col]
    except Exception:
        return None


def _visible_columns(viewer: Any) -> list[str]:
    if viewer is None:
        return []
    try:
        cols = viewer.visible_columns()
    except Exception:
        cols = getattr(viewer, "columns", []) or []
    return list(cols)


def handle_yank_cell(context: CommandContext, args):
    """Copy the active cell's display text to the clipboard."""

    viewer = context.viewer
    result = _resolve_active_cell_display(viewer, max_chars=None)
    if result is None:
        viewer.status_message = "nothing to copy"
        return

    column, text = result
    success = copy_to_clipboard(text)
    if success:
        viewer.status_message = f"copied {column} to clipboard"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_path(context: CommandContext, args):
    """Copy the dataset path (when available) to the clipboard."""

    viewer = context.viewer
    path = _resolve_active_dataset_path(context)
    if path is None:
        viewer.status_message = "dataset path unavailable"
        return

    success = copy_to_clipboard(str(path))
    if success:
        viewer.status_message = f"copied {path} to clipboard"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_column(context: CommandContext, args):
    """Copy the current column name to the clipboard."""

    viewer = context.viewer
    column = _resolve_current_column(viewer)
    if column is None:
        viewer.status_message = "no column to copy"
        return

    success = copy_to_clipboard(str(column))
    if success:
        viewer.status_message = f"copied column {column}"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_all_columns(context: CommandContext, args):
    """Copy visible column names as a vertically formatted Python list."""

    viewer = context.viewer
    columns = _visible_columns(viewer)
    if not columns:
        viewer.status_message = "no columns to copy"
        return

    formatted = "[\n" + "\n".join(f"    {repr(col)}," for col in columns) + "\n]"
    success = copy_to_clipboard(formatted)
    if success:
        viewer.status_message = f"copied {len(columns)} columns"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_schema(context: CommandContext, args):
    """Copy the current schema mapping to the clipboard."""

    viewer = context.viewer
    schema_obj = getattr(context.sheet, "schema", None)
    if not schema_obj:
        viewer.status_message = "schema not available"
        return

    if isinstance(schema_obj, Mapping):
        ordered = _visible_columns(viewer) or list(schema_obj.keys())
        lines: list[str] = []
        for name in ordered:
            if name not in schema_obj:
                continue
            dtype = schema_obj.get(name)
            dtype_repr = str(dtype) if dtype is not None else "None"
            lines.append(f"    {repr(name)}: {dtype_repr},")
        if not lines:
            for name, dtype in schema_obj.items():
                dtype_repr = str(dtype) if dtype is not None else "None"
                lines.append(f"    {repr(name)}: {dtype_repr},")
        formatted_schema = "{\n" + "\n".join(lines) + "\n}"
    else:
        formatted_schema = repr(schema_obj)

    success = copy_to_clipboard(formatted_schema)
    if success:
        viewer.status_message = "schema copied"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_table_excel(context: CommandContext, args):
    """Start a viewport region selection for Excel-ready clipboard output."""

    viewer = context.viewer
    screen = getattr(context, "screen", None)
    if screen is None:
        viewer.status_message = "yte requires TUI"
        return
    starter = getattr(screen, "_start_clipboard_region", None)
    if not callable(starter):
        viewer.status_message = "yte requires TUI"
        return
    starter()


def handle_yank_table_markdown(context: CommandContext, args):
    """Start a viewport region selection for Markdown clipboard output."""

    viewer = context.viewer
    screen = getattr(context, "screen", None)
    if screen is None:
        viewer.status_message = "ytm requires TUI"
        return
    starter = getattr(screen, "_start_clipboard_region_markdown", None)
    if not callable(starter):
        viewer.status_message = "ytm requires TUI"
        return
    starter()


def handle_yank_table_ascii(context: CommandContext, args):
    """Start a viewport region selection for ASCII table clipboard output."""

    viewer = context.viewer
    screen = getattr(context, "screen", None)
    if screen is None:
        viewer.status_message = "yta requires TUI"
        return
    starter = getattr(screen, "_start_clipboard_region_ascii", None)
    if not callable(starter):
        viewer.status_message = "yta requires TUI"
        return
    starter()


def handle_yank_table_unicode(context: CommandContext, args):
    """Start a viewport region selection for Unicode table clipboard output."""

    viewer = context.viewer
    screen = getattr(context, "screen", None)
    if screen is None:
        viewer.status_message = "ytu requires TUI"
        return
    starter = getattr(screen, "_start_clipboard_region_unicode", None)
    if not callable(starter):
        viewer.status_message = "ytu requires TUI"
        return
    starter()


def handle_up(context: CommandContext, args):
    """Move cursor up one row."""
    recorder = getattr(context, "recorder", None)
    if recorder and recorder.enabled:
        before_state = _snapshot_state(context.viewer)
        if before_state is None:
            context.viewer.move_up(1)
            return
        start_ns = monotonic_ns()
        context.viewer.move_up(1)
        duration_ms = (monotonic_ns() - start_ns) / 1_000_000
        after_state = _snapshot_state(context.viewer)
        if after_state is None:  # pragma: no cover - defensive
            after_state = before_state
        payload = {
            "before_row": before_state.cursor.row,
            "before_row0": before_state.viewport.row0,
            "after_row": after_state.cursor.row,
            "after_row0": after_state.viewport.row0,
            "view_height": before_state.visible_row_count or after_state.visible_row_count,
            "scrolled": after_state.viewport.row0 != before_state.viewport.row0,
            "hit_top": after_state.cursor.row == 0,
        }
        recorder.record_perf(phase="move.up", duration_ms=duration_ms, payload=payload)
        return

    context.viewer.move_up(1)


def handle_left(context: CommandContext, args):
    """Move cursor left one column."""
    context.viewer.move_left(1)


def handle_right(context: CommandContext, args):
    """Move cursor right one column."""
    recorder = getattr(context, "recorder", None)
    if recorder and recorder.enabled:
        before_state = _snapshot_state(context.viewer)
        if before_state is None:
            context.viewer.move_right(1)
            return
        start_ns = monotonic_ns()
        context.viewer.move_right(1)
        duration_ms = (monotonic_ns() - start_ns) / 1_000_000
        after_state = _snapshot_state(context.viewer)
        if after_state is None:  # pragma: no cover - defensive
            after_state = before_state
        payload = {
            "before_col": before_state.cursor.col,
            "before_col0": before_state.viewport.col0,
            "after_col": after_state.cursor.col,
            "after_col0": after_state.viewport.col0,
            "visible_cols_before": before_state.visible_column_count or len(before_state.columns),
            "visible_cols_after": after_state.visible_column_count or len(after_state.columns),
        }
        recorder.record_perf(phase="move.right", duration_ms=duration_ms, payload=payload)
        return

    context.viewer.move_right(1)


def handle_pagedown(context: CommandContext, args):
    """Move down by one page."""
    context.viewer.page_down()


def handle_pageup(context: CommandContext, args):
    """Move up by one page."""
    context.viewer.page_up()


def handle_half_pageright(context: CommandContext, args):
    """Move right by half page."""
    context.viewer.half_page_right()


def handle_half_pageleft(context: CommandContext, args):
    """Move left by half page."""
    context.viewer.half_page_left()


def handle_half_pagedown(context: CommandContext, args):
    """Move down by half page."""
    context.viewer.half_page_down()


def handle_half_pageup(context: CommandContext, args):
    """Move up by half page."""
    context.viewer.half_page_up()


def handle_top(context: CommandContext, args):
    """Go to the top row."""
    context.viewer.go_top()


def handle_bottom(context: CommandContext, args):
    """Go to the bottom row."""
    context.viewer.go_bottom()


def handle_viewport_top(context: CommandContext, args):
    """Go to the first visible row in the current viewport."""
    viewer = _navigation_viewer(context)
    if viewer is None:
        return
    if not viewer.go_visible_top():
        viewer.status_message = "no visible rows"


def handle_viewport_middle(context: CommandContext, args):
    """Go to the middle visible row in the current viewport."""
    viewer = _navigation_viewer(context)
    if viewer is None:
        return
    if not viewer.go_visible_middle():
        viewer.status_message = "no visible rows"


def handle_viewport_bottom(context: CommandContext, args):
    """Go to the last visible row in the current viewport."""
    viewer = _navigation_viewer(context)
    if viewer is None:
        return
    if not viewer.go_visible_bottom():
        viewer.status_message = "no visible rows"


def handle_first(context: CommandContext, args):
    """Go to the first visible column."""
    context.viewer.first_col()


def handle_last(context: CommandContext, args):
    """Go to the last fully visible column."""
    context.viewer.last_col()


def handle_slide_left(context: CommandContext, args):
    """Slide the current column one position to the left."""
    context.viewer.slide_column_left()


def handle_slide_right(context: CommandContext, args):
    """Slide the current column one position to the right."""
    context.viewer.slide_column_right()


def handle_slide_first(context: CommandContext, args):
    """Slide the current column to the first visible slot."""
    context.viewer.slide_column_to_start()


def handle_slide_last(context: CommandContext, args):
    """Slide the current column to the last visible slot."""
    context.viewer.slide_column_to_end()


def handle_sort_asc(context: CommandContext, args):
    """Sort ascending by the current column, toggling off on repeat."""
    context.viewer.set_sort_direction(desc=False, stack=False)
    context.sheet = context.viewer.sheet


def handle_sort_desc(context: CommandContext, args):
    """Sort descending by the current column, toggling off on repeat."""
    context.viewer.set_sort_direction(desc=True, stack=False)
    context.sheet = context.viewer.sheet


def handle_sort_asc_stack(context: CommandContext, args):
    """Stack an ascending sort on the current column, toggling off on repeat."""
    context.viewer.set_sort_direction(desc=False, stack=True)
    context.sheet = context.viewer.sheet


def handle_sort_desc_stack(context: CommandContext, args):
    """Stack a descending sort on the current column, toggling off on repeat."""
    context.viewer.set_sort_direction(desc=True, stack=True)
    context.sheet = context.viewer.sheet
    context.sheet = context.viewer.sheet


def handle_filter_value(context: CommandContext, args: list[str]) -> None:
    """Append a filter for the active cell's value on the current column."""

    context.viewer.append_filter_for_current_value()
    context.sheet = context.viewer.sheet


def handle_filter_value_not(context: CommandContext, args: list[str]) -> None:
    """Append a negative filter for the active cell's value on the current column."""

    context.viewer.append_negative_filter_for_current_value()
    context.sheet = context.viewer.sheet


def handle_filter(context: CommandContext, args):
    """Apply a filter to the current sheet."""
    mode = "replace"
    if len(args) >= 2 and args[-1].strip().lower() in {"replace", "append"}:
        mode = args[-1].strip().lower()
        filter_expr = " ".join(args[:-1])
    else:
        filter_expr = " ".join(args)
    filter_expr = filter_expr or None
    context.viewer.apply_filter(filter_expr, mode=mode)
    context.sheet = context.viewer.sheet


def handle_sql_filter(context: CommandContext, args):
    """Apply an SQL WHERE-clause filter to the current sheet."""
    mode = "replace"
    if len(args) >= 2 and args[-1].strip().lower() in {"replace", "append"}:
        mode = args[-1].strip().lower()
        filter_sql = " ".join(args[:-1])
    else:
        filter_sql = " ".join(args)
    filter_sql = filter_sql or None
    context.viewer.apply_sql_filter(filter_sql, mode=mode)
    context.sheet = context.viewer.sheet


def handle_reset_expression_filter(context: CommandContext, args) -> None:
    """Clear any expression filters while keeping SQL filters."""

    if not _reset_file_browser_filter(context):
        context.viewer.reset_expression_filter()
    context.sheet = context.viewer.sheet


def handle_reset_sql_filter(context: CommandContext, args) -> None:
    """Clear any SQL filters while keeping expression filters."""

    context.viewer.reset_sql_filter()
    context.sheet = context.viewer.sheet


def handle_reset_sort(context: CommandContext, args) -> None:
    """Clear any active sorting on the sheet."""

    context.viewer.reset_sorting()
    context.sheet = context.viewer.sheet


def handle_reset(context: CommandContext, args):
    """Reset all filters, sorting, and selection."""
    if not _reset_file_browser_filter(context):
        context.viewer.reset_filters()
    context.sheet = context.viewer.sheet


def handle_freeze(context: CommandContext, args):
    """Freeze rows or columns based on the provided spec."""
    if not args:
        raise ValueError("usage: freeze c<number>|r<number>")

    spec = args[0].strip().lower()
    if not spec:
        raise ValueError("usage: freeze c<number>|r<number>")

    viewer = context.viewer

    if spec[0] == "c":
        count_text = spec[1:]
        try:
            count = int(count_text) if count_text else 1
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("freeze columns expects an integer count") from exc
        viewer.set_frozen_columns(max(0, count))
        actual = len(getattr(viewer, "frozen_columns", []))
        if actual:
            plural = "column" if actual == 1 else "columns"
            viewer.status_message = f"frozen {actual} {plural}"
        else:
            viewer.status_message = "no columns frozen"
    elif spec[0] == "r":
        count_text = spec[1:]
        try:
            count = int(count_text) if count_text else 1
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("freeze rows expects an integer count") from exc
        viewer.set_frozen_rows(max(0, count))
        if count > 0:
            plural = "row" if count == 1 else "rows"
            viewer.status_message = f"frozen first {count} {plural}"
        else:
            viewer.status_message = "no rows frozen"
    else:
        raise ValueError("usage: freeze c<number>|r<number>")


def handle_unfreeze(context: CommandContext, args):
    """Clear any frozen rows or columns."""
    viewer = context.viewer
    viewer.clear_freeze()
    viewer.status_message = "unfroze rows and columns"


def handle_goto(context: CommandContext, args):
    """Go to a specific column."""
    if not args:
        return
    col_name = args[0]
    try:
        col_idx = context.viewer.columns.index(col_name)
        context.viewer.cur_col = col_idx
        if col_idx < context.viewer.col0:
            context.viewer.col0 = col_idx
        elif col_idx >= context.viewer.col0 + len(context.viewer.visible_cols):
            # Adjust viewport to show the column
            context.viewer.col0 = col_idx
        context.viewer.clamp()
    except ValueError:
        # Column not found - could raise error or ignore
        pass


def handle_render(context: CommandContext, args):
    """Render command - primarily for headless mode."""
    # This command typically just signals that a render should happen
    # The actual rendering is handled by the calling code
    pass


def handle_hide(context: CommandContext, args):
    """Hide the current column."""
    context.viewer.hide_current_column()


def handle_unhide(context: CommandContext, args):
    """Unhide all hidden columns."""
    context.viewer.unhide_all_columns()


def handle_select_row(context: CommandContext, args):
    """Toggle selection for the focused row."""

    context.viewer.toggle_row_selection()


def handle_invert_selection(context: CommandContext, args):
    """Invert selection for the current viewport."""

    context.viewer.invert_selection()


def handle_clear_selection(context: CommandContext, args):
    """Clear all selected rows."""

    context.viewer.clear_row_selection()


def handle_materialize_all(context: CommandContext, args):
    """Materialize the active view (filters, sorts, projection) into a new sheet."""

    viewer = context.viewer
    session = _resolve_session(context)
    if session is None:
        viewer.status_message = "materialize unavailable (no session)"
        return

    plan = viewer.plan_controller.current_plan()
    if plan is None:
        viewer.status_message = "materialize unsupported for this sheet"
        return

    projection = plan.projection_or(viewer.columns)
    normalized_plan = QueryPlan(
        filter_clauses=plan.filter_clauses,
        sort=plan.sort,
        projection=projection,
        search_text=None,
        limit=None,
        offset=0,
    )

    sheet = _materialize_plan(viewer, normalized_plan)
    if sheet is None:
        return

    status = f"materialized view -> depth {viewer.stack_depth + 1}"
    _push_materialized_viewer(session, viewer, sheet, status)


def handle_materialize_selection(context: CommandContext, args):
    """Materialize only the currently selected rows into a new sheet."""

    viewer = context.viewer
    session = _resolve_session(context)
    if session is None:
        viewer.status_message = "materialize unavailable (no session)"
        return

    base_plan = viewer.plan_controller.current_plan()
    if base_plan is None:
        viewer.status_message = "materialize unsupported for this sheet"
        return

    row_id_column = getattr(viewer.row_provider, "_row_id_column", None)
    plan_columns = list(base_plan.projection_or(viewer.columns))
    if row_id_column and row_id_column not in plan_columns:
        plan_columns.append(row_id_column)

    selection_clause = viewer._selection_filter_clause(plan_columns)
    if selection_clause is None:
        selected_count = len(getattr(viewer, "_selected_row_ids", ()))
        if selected_count > 0:
            viewer.status_message = "selection too large to materialize"
        else:
            viewer.status_message = "no selection to materialize"
        return

    try:
        filter_clause = FilterClause("expr", selection_clause)
    except Exception:
        viewer.status_message = "unable to materialize selection"
        return

    projection = base_plan.projection_or(viewer.columns)
    filter_clauses = (*base_plan.filter_clauses, filter_clause)
    selection_plan = QueryPlan(
        filter_clauses=filter_clauses,
        sort=base_plan.sort,
        projection=projection,
        search_text=None,
        limit=None,
        offset=0,
    )

    sheet = _materialize_plan(viewer, selection_plan)
    if sheet is None:
        return

    status = f"materialized selection -> depth {viewer.stack_depth + 1}"
    _push_materialized_viewer(session, viewer, sheet, status)


def handle_select_same_value(context: CommandContext, args: list[str]) -> None:
    """Select rows that share the current cell's value in the active column."""

    context.viewer.select_matching_value_rows()


def handle_select_contains(context: CommandContext, args: list[str]) -> None:
    """Select rows where the active column contains the provided substring."""

    viewer = context.viewer
    if not args or not args[0]:
        viewer.status_message = "selection requires a search term"
        return

    query = args[0]
    columns = ()
    try:
        columns = (viewer.columns[viewer.cur_col],)
    except Exception:
        columns = viewer.columns[:1]
    try:
        viewer.select_rows_containing(query, columns=columns)
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"selection error: {exc}"


def handle_filter_contains(context: CommandContext, args: list[str]) -> None:
    """Append a contains filter on the active column."""

    viewer = context.viewer
    if not args or not args[0]:
        viewer.status_message = "filter requires a search term"
        return

    viewer.append_filter_for_contains_text(args[0])
    context.sheet = viewer.sheet


def handle_undo(context: CommandContext, args):
    """Undo the last operation."""
    context.viewer.undo_last_operation()


def handle_redo(context: CommandContext, args):
    """Redo the last undone operation."""
    context.viewer.redo_last_operation()


def handle_maxcol(context: CommandContext, args):
    """Toggle maximize current column."""
    context.viewer.toggle_maximize_current_col()


def handle_maxall(context: CommandContext, args):
    """Toggle maximize all columns."""
    context.viewer.toggle_maximize_all_cols()


def handle_resetmax(context: CommandContext, args):
    """Reset maximized column widths to defaults."""

    viewer = context.viewer
    viewer._force_default_width_mode()
    viewer.status_message = "maximized widths reset"
    viewer.clamp()


def _lazyframe_for_plan(viewer: Viewer, plan: QueryPlan, *, op: str):
    """Compile ``plan`` to a Polars LazyFrame, dropping row ids if present."""

    compiler = viewer.engine.build_plan_compiler()
    if compiler is None:
        viewer.status_message = f"{op} unsupported for this sheet"
        return None, None

    try:
        physical_plan = compiler.compile(plan)
    except PulkaCoreError as exc:
        viewer._status_from_error(op, exc)
        return None, None
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"{op} error: {exc}"[:120]
        return None, None

    try:
        polars_plan = unwrap_physical_plan(physical_plan)
        lazy_frame = polars_plan.to_lazyframe()
        row_id_column = getattr(viewer.row_provider, "_row_id_column", None)
        if row_id_column:
            try:
                schema = lazy_frame.collect_schema()
            except Exception:
                schema = getattr(lazy_frame, "schema", {})
            if row_id_column in schema:
                with suppress(Exception):
                    lazy_frame = lazy_frame.drop([row_id_column])
    except Exception as exc:  # pragma: no cover - defensive
        viewer.status_message = f"{op} error: {exc}"[:120]
        return None, None

    return lazy_frame, polars_plan


def _columns_from_lazyframe(lazy_frame, *, row_id_column: str | None) -> list[str]:
    try:
        schema = lazy_frame.collect_schema()
    except Exception:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PerformanceWarning)
            schema = getattr(lazy_frame, "schema", {})
    if hasattr(schema, "keys"):
        columns = list(schema.keys())
    elif hasattr(schema, "names"):
        columns = list(schema.names())
    else:
        columns = list(schema) if schema else []
    if row_id_column:
        columns = [name for name in columns if name != row_id_column]
    return columns


def handle_write(context: CommandContext, args):
    """Export the active sheet to a user-provided path."""

    viewer = context.viewer
    recorder = _active_recorder(context)

    if not args:
        _update_status(viewer, recorder, "write requires a destination path")
        return

    raw_destination = args[0]
    try:
        destination = _resolve_destination_path(raw_destination)
    except Exception as exc:  # pragma: no cover - defensive
        _update_status(viewer, recorder, f"write path error: {exc}")
        return

    try:
        format_hint, option_values = _parse_write_options(args[1:])
    except ValueError as exc:
        _update_status(viewer, recorder, f"write option error: {exc}")
        return

    sheet = viewer.sheet
    if not sheet_supports(sheet, SHEET_FEATURE_PLAN):
        _update_status(viewer, recorder, "write requires a plan-capable sheet")
        return

    plan_snapshot = getattr(sheet, "plan", None)
    options_mapping = dict(option_values) if option_values else {}
    export_options = options_mapping or None
    ui = getattr(context, "ui", None)
    if ui is None:
        ui = getattr(context, "screen", None)
    runner = getattr(getattr(context, "session", None), "job_runner", None)

    if ui is None or runner is None:
        _execute_write_now(
            sheet,
            plan_snapshot,
            destination,
            format_hint,
            export_options,
            viewer,
            recorder,
        )
        return

    _update_status(viewer, recorder, "Export in progress...")

    job_tag = _make_write_job_tag(destination)

    def _job(_: int) -> Path:
        snapshot = _snapshot_sheet_for_export(sheet, plan_snapshot)
        return write_view_to_path(
            snapshot,
            destination,
            format_hint=format_hint,
            options=export_options,
        )

    try:
        future = runner.submit(sheet, job_tag, _job, cache_result=False)
    except Exception as exc:  # pragma: no cover - defensive
        _update_status(viewer, recorder, f"write error: {exc}")
        return

    notifier = _make_write_completion_notifier(ui)
    handle = _WriteJobHandle(
        future,
        destination,
        recorder,
        status_source=getattr(viewer, "status_source", None),
        on_done=notifier,
    )
    if ui is not None:
        ui.register_job(viewer, handle)


def handle_repro_export(context: CommandContext, args):
    """Export a reproducible dataset slice."""
    from ..logging.redaction import redact_path

    # Parse arguments
    row_margin = 10
    include_all_columns = False

    # Parse possible arguments
    for arg in args:
        if arg.startswith("rows="):
            try:
                row_margin = int(arg.split("=", 1)[1])
            except (ValueError, IndexError):
                context.viewer.status_message = f"invalid row margin: {arg}"
                return
        elif arg.startswith("all_columns="):
            try:
                include_all_columns = arg.split("=", 1)[1].lower() in ("true", "1", "yes")
            except (ValueError, IndexError):
                context.viewer.status_message = f"invalid all_columns value: {arg}"
                return

    # Get the recorder from context - may not be available
    recorder = getattr(context, "recorder", None)
    if recorder is None:
        context.viewer.status_message = "recorder not available"
        return

    try:
        # Call the export method on the recorder
        export_path = recorder.export_repro_slice(
            session=context.session,  # Pass the session
            row_margin=row_margin,
            include_all_columns=include_all_columns,
        )

        # Show status message with redacted path basename
        redacted = redact_path(str(export_path))
        context.viewer.status_message = f"repro export → {redacted['basename'][:20]}…"

    except Exception as e:
        context.viewer.status_message = f"repro export failed: {str(e)[:50]}"


def _set_file_browser_directory(viewer: Viewer, target: Path) -> tuple[str | None, str | None]:
    """Update the active file browser to ``target``."""

    sheet = getattr(viewer, "sheet", None)
    if sheet is None or not resolve_sheet_traits(sheet).is_file_browser:
        return None, None

    builder = getattr(sheet, "at_path", None)
    if not callable(builder):
        return None, "browser cannot change directory"

    try:
        new_sheet = builder(target)
    except Exception as exc:
        return None, f"cd failed: {exc}"

    source_label = resolve_display_path(new_sheet, fallback=str(target))
    viewer.replace_sheet(new_sheet, source_path=source_label)
    with suppress(Exception):
        viewer._clear_selection_state()
    with suppress(Exception):
        viewer.row_count_tracker.ensure_total_rows()
    return file_browser_status_text(new_sheet), None


def handle_cd(context: CommandContext, args):
    """Change the working directory for subsequent commands."""

    viewer = context.viewer
    recorder = _active_recorder(context)

    if not args or not args[0].strip():
        _update_status(viewer, recorder, "cd requires a path")
        return

    raw_target = args[0].strip()
    base_dir = _cd_base_directory(context)

    target_path = Path(raw_target).expanduser()
    if not target_path.is_absolute():
        target_path = base_dir / target_path
    resolved = _normalise_path(target_path)

    if not resolved.exists():
        _update_status(viewer, recorder, f"{resolved} does not exist")
        return
    if not resolved.is_dir():
        _update_status(viewer, recorder, f"{resolved} is not a directory")
        return

    try:
        os.chdir(resolved)
    except Exception as exc:
        _update_status(viewer, recorder, f"cd failed: {exc}")
        return

    session = _resolve_session(context)
    if session is not None:
        with suppress(Exception):
            session.command_cwd = resolved

    browser_message, browser_error = _set_file_browser_directory(viewer, resolved)
    if browser_error:
        _update_status(viewer, recorder, browser_error)
        return

    status = f"cwd -> {resolved}"
    if browser_message:
        status = f"{status}; {browser_message}"
    _update_status(viewer, recorder, status)


def handle_browse(context: CommandContext, args):
    session = getattr(context, "session", None)
    viewer = getattr(context, "viewer", None)
    if session is None or viewer is None:
        return
    if len(args) > 1:
        viewer.status_message = "file_browser_sheet accepts at most one path"
        return
    target = args[0] if args else None
    try:
        session.open_file_browser(target)
    except ValueError as exc:
        viewer.status_message = str(exc)
    except Exception as exc:  # pragma: no cover - defensive guard
        viewer.status_message = f"file_browser_sheet failed: {exc}"


def handle_commands(context: CommandContext, args: list[str]) -> None:
    """Open a derived sheet listing all available commands."""

    viewer = getattr(context, "viewer", None)
    session = _resolve_session(context)
    if session is None or viewer is None:
        return
    if args:
        viewer.status_message = "help_sheet does not accept arguments"
        return

    try:
        help_entries = None
        ui = getattr(context, "ui", None)
        if ui is not None:
            provider = getattr(ui, "commands_help_entries", None)
            if callable(provider):
                help_entries = provider()
        sheet_options = {"commands": session.commands}
        if help_entries:
            sheet_options["help_entries"] = help_entries
        session.open_sheet_view("help_sheet", base_viewer=viewer, **sheet_options)
        with suppress(Exception):
            session.command_runtime.prepare_viewer(session.viewer)
    except Exception as exc:  # pragma: no cover - defensive guard
        viewer.status_message = f"help_sheet failed: {exc}"[:120]


def handle_status(context: CommandContext, args: list[str]) -> None:
    """Open a derived sheet listing status message history."""

    viewer = getattr(context, "viewer", None)
    session = _resolve_session(context)
    if session is None or viewer is None:
        return
    if args:
        viewer.status_message = "status does not accept arguments"
        return

    try:
        records = session.status_history_records()
        session.open_sheet_view("status_messages", base_viewer=viewer, records=records)
        with suppress(Exception):
            session.command_runtime.prepare_viewer(session.viewer)
    except Exception as exc:  # pragma: no cover - defensive guard
        viewer.status_message = f"status failed: {exc}"[:120]


def handle_schema(context: CommandContext, args):
    """Display column schema information."""
    if not hasattr(context.sheet, "schema"):
        context.viewer.status_message = "schema not available"
        return

    schema = context.sheet.schema
    if not schema:
        context.viewer.status_message = "no schema information"
        return

    # In headless mode, we'll just set a status message with schema info
    # In TUI mode, this would typically open a modal
    schema_info = ", ".join(f"{k}:{v}" for k, v in schema.items())
    context.viewer.status_message = f"schema: {schema_info[:100]}..."


def handle_insight(context: CommandContext, args):
    """Toggle or explicitly control the insight sidecar."""

    screen = getattr(context, "screen", None)
    if screen is None or not hasattr(screen, "set_insight_panel"):
        context.viewer.status_message = "insight command requires the TUI"
        return
    if not args:
        state = screen.set_insight_panel()
        context.viewer.status_message = "insight panel on" if state else "insight panel off"
        return
    target = args[0].strip().lower()
    if target in {"on", "1", "true", "yes"}:
        screen.set_insight_panel(True)
        context.viewer.status_message = "insight panel on"
    elif target in {"off", "0", "false", "no"}:
        screen.set_insight_panel(False)
        context.viewer.status_message = "insight panel off"
    elif target in {"column", "columns"}:
        screen.set_insight_panel_mode("column")
        context.viewer.status_message = "insight mode: column"
    elif target in {"transform", "transforms"}:
        screen.set_insight_panel_mode("transform")
        context.viewer.status_message = "insight mode: transforms"
    else:
        context.viewer.status_message = f"unknown insight option: {target}"


def handle_search(context: CommandContext, args):
    """Search current column for substring."""
    if not args or not args[0]:
        context.viewer.status_message = "search requires a search term"
        return

    search_term = args[0]
    try:
        context.viewer.set_search(search_term)
        current = context.viewer.search_text
        if current:
            context.viewer.search(forward=True, include_current=True)
    except Exception as exc:
        context.viewer.status_message = f"search error: {exc}"
    else:
        context.sheet = context.viewer.sheet


def handle_search_value_next(context: CommandContext, args):
    """Search forward for the active cell value in the current column."""
    try:
        context.viewer.search_value(forward=True, include_current=False, center=True)
    except Exception as exc:
        context.viewer.status_message = f"value search error: {exc}"


def handle_search_value_prev(context: CommandContext, args):
    """Search backward for the active cell value in the current column."""
    try:
        context.viewer.search_value(forward=False, include_current=False, center=True)
    except Exception as exc:
        context.viewer.status_message = f"value search error: {exc}"


def handle_next_diff(context: CommandContext, args):
    """Go to next search match or selected row."""
    try:
        viewer = context.viewer
        has_selection = getattr(viewer, "has_active_selection", None)
        navigator = getattr(viewer, "next_selected_row", None)
        last_action = getattr(viewer, "last_repeat_action", None)
        last_search = getattr(viewer, "last_search_kind", None)
        if (
            callable(has_selection)
            and has_selection()
            and callable(navigator)
            and (last_action == "selection" or last_search is None)
        ):
            navigator()
            return

        search_kind = getattr(context.viewer, "last_search_kind", None)
        found = context.viewer.repeat_last_search(forward=True)
        if search_kind == "value":
            return
        if found:
            context.viewer.status_message = "next match"
        else:
            context.viewer.status_message = "no more matches"
    except Exception as exc:
        context.viewer.status_message = f"search error: {exc}"


def handle_prev_diff(context: CommandContext, args):
    """Go to previous search match or selected row."""
    try:
        viewer = context.viewer
        has_selection = getattr(viewer, "has_active_selection", None)
        navigator = getattr(viewer, "prev_selected_row", None)
        last_action = getattr(viewer, "last_repeat_action", None)
        last_search = getattr(viewer, "last_search_kind", None)
        if (
            callable(has_selection)
            and has_selection()
            and callable(navigator)
            and (last_action == "selection" or last_search is None)
        ):
            navigator()
            return

        search_kind = getattr(context.viewer, "last_search_kind", None)
        found = context.viewer.repeat_last_search(forward=False)
        if search_kind == "value":
            return
        if found:
            context.viewer.status_message = "previous match"
        else:
            context.viewer.status_message = "no more matches"
    except Exception as exc:
        context.viewer.status_message = f"search error: {exc}"


def handle_center(context: CommandContext, args):
    """Center current row in viewport."""
    viewer = context.viewer
    viewer.center_current_row()
    expected_offset = _body_view_height(viewer) // 2
    if viewer.cur_row - viewer.row0 != expected_offset:
        viewer.status_message = "not enough rows to center"


def handle_row_top(context: CommandContext, args):
    """Scroll current row to the top of the viewport."""
    viewer = _navigation_viewer(context)
    if viewer is None:
        return
    viewer.top_current_row()
    if viewer.cur_row != viewer.row0:
        viewer.status_message = "not enough rows to move to top"


def handle_row_bottom(context: CommandContext, args):
    """Scroll current row to the bottom of the viewport."""
    viewer = _navigation_viewer(context)
    if viewer is None:
        return
    viewer.bottom_current_row()
    body_height = _body_view_height(viewer)
    if viewer.cur_row - viewer.row0 != body_height - 1:
        viewer.status_message = "not enough rows to move to bottom"


def handle_next_different(context: CommandContext, args):
    """Navigate to next different value in current column."""
    if context.viewer.next_different_value():
        context.viewer.center_current_row()
        context.viewer.status_message = "next different value"
    else:
        context.viewer.status_message = "no more different values"


def handle_prev_different(context: CommandContext, args):
    """Navigate to previous different value in current column."""
    if context.viewer.prev_different_value():
        context.viewer.center_current_row()
        context.viewer.status_message = "previous different value"
    else:
        context.viewer.status_message = "no more different values"


def handle_first_overall(context: CommandContext, args):
    """Go to first column overall (adjusts viewport)."""
    context.viewer.first_col_overall()


def handle_last_overall(context: CommandContext, args):
    """Go to last column overall (adjusts viewport)."""
    context.viewer.last_col_overall()


# ---------------------------------------------------------------------------
# Helpers for export command
# ---------------------------------------------------------------------------


def _active_recorder(context: CommandContext):
    recorder = getattr(context, "recorder", None)
    if recorder is None or not getattr(recorder, "enabled", False):
        return None
    return recorder


_STATUS_MESSAGE_MAX_LENGTH = 96


def _normalise_status_message(message: str) -> str:
    """Return a single-line status message clamped to a sane length."""

    collapsed = " ".join(str(message).split())
    if not collapsed:
        return ""
    if len(collapsed) <= _STATUS_MESSAGE_MAX_LENGTH:
        return collapsed
    # Reserve room for an ellipsis to keep the message readable.
    trim_length = max(1, _STATUS_MESSAGE_MAX_LENGTH - 1)
    return f"{collapsed[:trim_length]}…"


def _update_status(viewer: Any, recorder: Any | None, message: str) -> None:
    normalised = _normalise_status_message(message)
    viewer.status_message = normalised
    if recorder is None or not normalised:
        return
    try:
        enabled = getattr(recorder, "enabled", False)
    except Exception:  # pragma: no cover - defensive
        enabled = False
    if not enabled:
        return
    with suppress(Exception):
        recorder.record_status(normalised)


def _resolve_destination_path(raw: str) -> Path:
    destination = Path(raw).expanduser()
    if not destination.is_absolute():
        destination = Path.cwd() / destination
    return destination.resolve()


def _parse_write_options(option_args: Sequence[str]) -> tuple[str | None, dict[str, Any]]:
    format_hint: str | None = None
    options: dict[str, Any] = {}
    for raw in option_args:
        if "=" not in raw:
            raise ValueError(f"option requires key=value: {raw}")
        key, value_text = raw.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("option key cannot be empty")
        value_text = value_text.strip()
        if value_text:
            try:
                parsed_value = ast.literal_eval(value_text)
            except (SyntaxError, ValueError):
                parsed_value = value_text
        else:
            parsed_value = ""
        if key.lower() == "format":
            hint = str(parsed_value).strip()
            format_hint = hint.lstrip(".") if hint.startswith(".") else hint or None
        else:
            options[key] = parsed_value
    return format_hint, options


def _format_destination(destination: Path | str) -> str:
    candidate = Path(destination)
    return candidate.name or candidate.as_posix()


def _make_write_job_tag(destination: Path) -> str:
    digest = hashlib.sha1(destination.as_posix().encode("utf-8")).hexdigest()
    return f"command.write::{digest}"


def _snapshot_sheet_for_export(sheet: Any, plan: Any) -> Any:
    if plan is None:
        return sheet
    with_plan = getattr(sheet, "with_plan", None)
    if not callable(with_plan):
        return sheet
    try:
        return with_plan(plan)
    except Exception:  # pragma: no cover - defensive
        return sheet


def _execute_write_now(
    sheet: Any,
    plan: Any,
    destination: Path,
    format_hint: str | None,
    options: dict[str, Any] | None,
    viewer: Any,
    recorder: Any | None,
) -> None:
    snapshot = _snapshot_sheet_for_export(sheet, plan)
    try:
        result = write_view_to_path(
            snapshot,
            destination,
            format_hint=format_hint,
            options=options,
        )
    except Exception as exc:
        _update_status(viewer, recorder, f"write error: {exc}")
        return
    dest_label = _format_destination(result)
    _update_status(viewer, recorder, f"Export saved to: {dest_label}")


def _make_write_completion_notifier(screen: Any) -> Callable[[], None] | None:
    """Return a callback that schedules a screen refresh when a write job finishes."""

    if screen is None:
        return None

    refresh = getattr(screen, "refresh", None)
    ui_hooks = getattr(screen, "_viewer_ui_hooks", None)
    invalidate = getattr(ui_hooks, "invalidate", None) if ui_hooks is not None else None
    call_soon = getattr(ui_hooks, "call_soon", None) if ui_hooks is not None else None

    def _invoke_refresh() -> None:
        if callable(refresh):
            try:
                refresh(skip_metrics=True)
            except TypeError:
                refresh()
            except Exception:
                return
            return
        if callable(invalidate):
            try:
                invalidate()
            except Exception:
                return

    if callable(call_soon):

        def _notify() -> None:
            def _wrapped() -> None:
                _invoke_refresh()

            try:
                call_soon(_wrapped)
            except Exception:
                _invoke_refresh()

        return _notify

    if callable(refresh) or callable(invalidate):

        def _notify() -> None:
            _invoke_refresh()

        return _notify

    return None


class _WriteJobHandle:
    """Adapter for job-runner futures polled by the TUI screen."""

    def __init__(
        self,
        future: Any,
        destination: Path,
        recorder: Any | None,
        *,
        status_source: str | None = None,
        on_done: Callable[[], None] | None = None,
    ):
        self._future = future
        self._destination = destination
        self._recorder = recorder
        self._on_done = on_done
        self._on_done_called = False
        self._status_source = status_source

        add_done_callback = getattr(future, "add_done_callback", None)
        if callable(add_done_callback) and on_done is not None:

            def _fire(_completed_future: Any) -> None:
                self._trigger_on_done()

            with suppress(Exception):
                add_done_callback(_fire)

    def cancel(self) -> None:
        future = self._future
        if future is None:
            return
        if hasattr(future, "cancel"):
            with suppress(Exception):
                future.cancel()

    def consume_update(self, viewer: Any) -> bool:
        future = self._future
        if future is None:
            self._trigger_on_done()
            return True
        if not future.done():
            return False
        try:
            result = future.result()
        except (CancelledError, FutureCancelledError):
            with self._status_source_context(viewer, self._status_source):
                _update_status(viewer, self._recorder, "write canceled")
            self._trigger_on_done()
            return True
        except Exception as exc:
            with self._status_source_context(viewer, self._status_source):
                _update_status(viewer, self._recorder, f"write error: {exc}")
            self._trigger_on_done()
            return True
        destination = getattr(result, "value", None)
        if destination is None:
            destination = self._destination
        dest_label = _format_destination(destination)
        status_source = getattr(result, "status_source", None) or self._status_source
        with self._status_source_context(viewer, status_source):
            _update_status(viewer, self._recorder, f"Export saved to: {dest_label}")
        self._trigger_on_done()
        return True

    def _trigger_on_done(self) -> None:
        callback = self._on_done
        if callback is None or self._on_done_called:
            return
        self._on_done_called = True
        try:
            callback()
        except Exception:
            return

    @staticmethod
    def _status_source_context(viewer: Any, source: str | None):
        binder = getattr(viewer, "bind_status_source", None)
        if callable(binder):
            return binder(source)
        return nullcontext()
