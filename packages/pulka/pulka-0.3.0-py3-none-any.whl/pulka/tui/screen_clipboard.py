"""Clipboard region selection handling for the TUI."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass

from ..core.viewer import Viewer


@dataclass(slots=True)
class ClipboardRegionState:
    """Track the starting cell for a clipboard region selection."""

    row_id: int | None = None
    col_index: int | None = None
    awaiting_start: bool = True
    format: str = "tsv"


class ClipboardRegionController:
    """Manage clipboard region selection and copying."""

    def __init__(
        self,
        *,
        get_viewer: Callable[[], Viewer | None],
        refresh: Callable[[], None],
        reset_pending_moves: Callable[[], None],
        copy_to_clipboard: Callable[[str, str, str], None],
    ) -> None:
        self._get_viewer = get_viewer
        self._refresh = refresh
        self._reset_pending_moves = reset_pending_moves
        self._copy_to_clipboard = copy_to_clipboard
        self._state: ClipboardRegionState | None = None

    def is_active(self) -> bool:
        return self._state is not None

    def awaiting_start(self) -> bool:
        return bool(self._state and self._state.awaiting_start)

    def start(self, *, format_name: str = "tsv") -> None:
        viewer = self._get_viewer()
        if viewer is None:
            return
        with suppress(Exception):
            viewer._ui_state.pop("clipboard_region_anchor", None)
        self._reset_pending_moves()
        columns = list(getattr(viewer, "visible_cols", []) or [])
        row_positions = list(getattr(viewer, "visible_row_positions", []) or [])
        if not columns or not row_positions:
            viewer.status_message = "no visible cells to copy"
            return
        self._state = ClipboardRegionState(format=format_name)
        viewer.status_message = "select first corner cell, Enter to set (Esc to cancel)"

    def start_markdown(self) -> None:
        self.start(format_name="markdown")

    def start_ascii(self) -> None:
        self.start(format_name="ascii")

    def start_unicode(self) -> None:
        self.start(format_name="unicode")

    def set_start(self) -> None:
        state = self._state
        viewer = self._get_viewer()
        if state is None or viewer is None:
            return
        indices = self._resolve_viewport_cursor_indices(viewer)
        if indices is None:
            viewer.status_message = "no visible cells to copy"
            return
        row_index, col_visible_index = indices
        row_positions = list(getattr(viewer, "visible_row_positions", []) or [])
        columns = list(getattr(viewer, "visible_cols", []) or [])
        if not row_positions or not columns:
            viewer.status_message = "no visible cells to copy"
            return
        if row_index < 0 or row_index >= len(row_positions):
            viewer.status_message = "no visible cells to copy"
            return
        if col_visible_index < 0 or col_visible_index >= len(columns):
            viewer.status_message = "no visible cells to copy"
            return

        row_id = row_positions[row_index]
        col_name = columns[col_visible_index]
        col_index = None
        all_cols = list(getattr(viewer, "columns", []) or [])
        with suppress(ValueError):
            col_index = all_cols.index(col_name)
        if col_index is None:
            viewer.status_message = "no visible cells to copy"
            return

        state.row_id = row_id
        state.col_index = col_index
        state.awaiting_start = False
        with suppress(Exception):
            viewer._ui_state["clipboard_region_anchor"] = (row_id, col_index)
        viewer.status_message = "select second corner cell, Enter to copy (Esc to cancel)"

    def set_start_at(self, row_id: int, col_name: str) -> None:
        state = self._state
        viewer = self._get_viewer()
        if state is None or viewer is None:
            return
        row_positions = list(getattr(viewer, "visible_row_positions", []) or [])
        columns = list(getattr(viewer, "visible_cols", []) or [])
        if not row_positions or not columns:
            viewer.status_message = "no visible cells to copy"
            return
        if row_id not in row_positions:
            viewer.status_message = "selection outside viewport"
            return
        if col_name not in columns:
            viewer.status_message = "selection outside viewport"
            return

        all_cols = list(getattr(viewer, "columns", []) or [])
        try:
            col_index = all_cols.index(col_name)
        except ValueError:
            viewer.status_message = "selection outside viewport"
            return

        state.row_id = row_id
        state.col_index = col_index
        state.awaiting_start = False
        with suppress(Exception):
            viewer._ui_state["clipboard_region_anchor"] = (row_id, col_index)
        viewer.status_message = "select second corner cell, Enter to copy (Esc to cancel)"

    def cancel(self) -> None:
        viewer = self._get_viewer()
        if self._state is None or viewer is None:
            return
        with suppress(Exception):
            viewer._ui_state.pop("clipboard_region_anchor", None)
        self._state = None
        self._reset_pending_moves()
        viewer.status_message = "clipboard region canceled"

    def finalize(self) -> None:
        state = self._state
        viewer = self._get_viewer()
        if state is None or viewer is None:
            return
        with suppress(Exception):
            viewer._ui_state.pop("clipboard_region_anchor", None)
        self._state = None
        self._reset_pending_moves()
        if state.awaiting_start or state.row_id is None or state.col_index is None:
            viewer.status_message = "select first corner cell first"
            return
        indices = self._resolve_viewport_cursor_indices(viewer)
        if indices is None:
            viewer.status_message = "no visible cells to copy"
            return
        self._copy_clipboard_region_to_clipboard(viewer, state, indices)

    def finalize_at(self, end: tuple[int, int]) -> None:
        state = self._state
        viewer = self._get_viewer()
        if state is None or viewer is None:
            return
        with suppress(Exception):
            viewer._ui_state.pop("clipboard_region_anchor", None)
        self._state = None
        self._reset_pending_moves()
        if state.awaiting_start or state.row_id is None or state.col_index is None:
            viewer.status_message = "select first corner cell first"
            return
        self._copy_clipboard_region_to_clipboard(viewer, state, end)

    def on_cell_click(self, row_id: int, col_name: str) -> None:
        state = self._state
        viewer = self._get_viewer()
        if state is None or viewer is None:
            return
        row_positions = list(getattr(viewer, "visible_row_positions", []) or [])
        columns = list(getattr(viewer, "visible_cols", []) or [])
        if not row_positions or not columns:
            viewer.status_message = "no visible cells to copy"
            return
        if row_id not in row_positions:
            viewer.status_message = "selection outside viewport"
            return
        if col_name not in columns:
            viewer.status_message = "selection outside viewport"
            return
        row_index = row_positions.index(row_id)
        col_visible_index = columns.index(col_name)
        if state.awaiting_start:
            self.set_start_at(row_id, col_name)
        else:
            self.finalize_at((row_index, col_visible_index))

    def _resolve_viewport_cursor_indices(self, viewer: Viewer) -> tuple[int, int] | None:
        columns = list(getattr(viewer, "visible_cols", []) or [])
        if not columns:
            return None
        try:
            current_col = viewer.current_colname()
        except Exception:
            current_col = None
        if not current_col:
            cur_col = getattr(viewer, "cur_col", None)
            if isinstance(cur_col, int):
                all_cols = getattr(viewer, "columns", [])
                if 0 <= cur_col < len(all_cols):
                    current_col = all_cols[cur_col]
        if not current_col:
            return None
        try:
            col_index = columns.index(current_col)
        except ValueError:
            return None

        row_positions = list(getattr(viewer, "visible_row_positions", []) or [])
        if not row_positions:
            return None
        cur_row = getattr(viewer, "cur_row", None)
        if not isinstance(cur_row, int):
            return None
        try:
            row_index = row_positions.index(cur_row)
        except ValueError:
            row0 = getattr(viewer, "row0", 0)
            row_index = max(0, min(len(row_positions) - 1, cur_row - row0))
        return row_index, col_index

    @staticmethod
    def _sanitize_clipboard_cell(value: object) -> str:
        text = "" if value is None else str(value)
        return text.replace("\t", " ").replace("\n", " ").replace("\r", " ")

    @classmethod
    def _sanitize_markdown_cell(cls, value: object) -> str:
        text = cls._sanitize_clipboard_cell(value)
        return text.replace("|", "\\|")

    @classmethod
    def _sanitize_ascii_cell(cls, value: object) -> str:
        text = cls._sanitize_clipboard_cell(value)
        return text.replace("|", "\\|")

    def _copy_clipboard_region_to_clipboard(
        self, viewer: Viewer, start: ClipboardRegionState, _end: tuple[int, int]
    ) -> None:
        columns = list(getattr(viewer, "visible_cols", []) or [])
        row_positions = list(getattr(viewer, "visible_row_positions", []) or [])
        if not columns or not row_positions:
            viewer.status_message = "no visible data to copy"
            return

        if start.row_id is None or start.col_index is None:
            viewer.status_message = "select first corner cell first"
            return
        end_row_index, end_col_visible_index = _end
        if end_row_index < 0 or end_row_index >= len(row_positions):
            viewer.status_message = "selection outside viewport"
            return
        if end_col_visible_index < 0 or end_col_visible_index >= len(columns):
            viewer.status_message = "selection outside viewport"
            return

        end_row_id = row_positions[end_row_index]
        end_col_name = columns[end_col_visible_index]
        all_cols = list(getattr(viewer, "columns", []) or [])
        end_col_index: int | None = None
        with suppress(ValueError):
            end_col_index = all_cols.index(end_col_name)
        if end_col_index is None:
            viewer.status_message = "selection outside viewport"
            return

        row_lo_id = min(start.row_id, end_row_id)
        row_hi_id = max(start.row_id, end_row_id)
        col_lo = min(start.col_index, end_col_index)
        col_hi = max(start.col_index, end_col_index)

        visible_columns_fn = getattr(viewer, "visible_columns", None)
        if callable(visible_columns_fn):
            visible_columns = list(visible_columns_fn() or [])
        else:
            hidden_cols = set(getattr(viewer, "_hidden_cols", set()) or set())
            visible_columns = [name for name in all_cols if name not in hidden_cols]

        visible_set = set(visible_columns)
        selected_columns = [
            name
            for idx, name in enumerate(all_cols)
            if col_lo <= idx <= col_hi and name in visible_set
        ]
        if not selected_columns:
            viewer.status_message = "no columns to copy"
            return

        selection_active = False
        has_selection = getattr(viewer, "has_active_selection", None)
        if callable(has_selection):
            selection_active = has_selection()
        else:
            selection_active = bool(
                getattr(viewer, "_selected_row_ids", None)
                or getattr(viewer, "_selection_filter_expr", None)
                or getattr(viewer, "_value_selection_filter", None)
            )

        selection_lookup = set(getattr(viewer, "_selected_row_ids", set()) or set())
        selection_expr = None
        if selection_active:
            selection_expr = getattr(viewer, "_selection_filter_expr", None)
            if not selection_expr:
                value_expr_fn = getattr(viewer, "_value_selection_filter_expr", None)
                if callable(value_expr_fn):
                    try:
                        selection_expr = value_expr_fn()
                    except Exception:
                        selection_expr = None

        row_start = min(row_lo_id, row_hi_id)
        row_end = max(row_lo_id, row_hi_id)
        if row_end < row_start:
            viewer.status_message = "no rows to copy"
            return

        fetch_columns = list(selected_columns)
        if selection_expr:
            fetch_columns = list(getattr(viewer, "columns", []) or [])
            if not fetch_columns:
                viewer.status_message = "no columns to copy"
                return

        format_name = start.format if start.format else "tsv"
        sanitize = self._sanitize_clipboard_cell
        if format_name in {"markdown", "ascii", "unicode"}:
            sanitize = (
                self._sanitize_markdown_cell
                if format_name == "markdown"
                else self._sanitize_ascii_cell
            )
            header_cells = [sanitize(name) for name in selected_columns]
            rows: list[list[str]] = []
        else:
            header_line = "\t".join(sanitize(name) for name in selected_columns)
            lines = [header_line]
        rows_copied = 0

        row_provider = getattr(viewer, "row_provider", None)
        if row_provider is None:
            viewer.status_message = "clipboard copy unavailable"
            return

        plan = getattr(viewer, "_current_plan", None)
        plan_value = plan() if callable(plan) else None

        page_size = getattr(row_provider, "page_size", 512)
        try:
            chunk_size = max(1, int(page_size))
        except (TypeError, ValueError):
            chunk_size = 512

        cursor = row_start
        while cursor <= row_end:
            fetch_count = min(chunk_size, row_end - cursor + 1)
            try:
                table_slice, _ = row_provider.get_slice(
                    plan_value, fetch_columns, cursor, fetch_count
                )
            except Exception as exc:
                viewer.status_message = f"clipboard copy failed: {exc}"[:120]
                return

            height = getattr(table_slice, "height", 0)
            if height <= 0:
                break

            base_row = table_slice.start_offset if table_slice.start_offset is not None else cursor
            row_positions = range(base_row, base_row + height)

            selection_matches = None
            if selection_expr:
                resolver = getattr(viewer, "_selection_matches_for_slice", None)
                if callable(resolver):
                    selection_matches = resolver(table_slice, row_positions, selection_expr)
                if selection_matches is None and not selection_lookup:
                    viewer.status_message = "selection unavailable for clipboard copy"
                    return

            id_resolver = getattr(viewer, "_row_identifier_for_slice", None)
            if selection_active and not callable(id_resolver):
                viewer.status_message = "selection unavailable for clipboard copy"
                return

            column_values = [table_slice.column(name).formatted(0) for name in selected_columns]
            for idx in range(height):
                if selection_active:
                    row_id = id_resolver(
                        table_slice,
                        idx,
                        row_positions=row_positions,
                        absolute_row=base_row + idx,
                    )
                    if row_id is None:
                        continue
                    if selection_lookup or selection_matches is not None:
                        if row_id not in selection_lookup and (
                            selection_matches is None or row_id not in selection_matches
                        ):
                            continue
                    else:
                        continue

                row_values = []
                for col_values in column_values:
                    try:
                        cell = col_values[idx]
                    except Exception:
                        cell = ""
                    row_values.append(sanitize(cell))
                if format_name in {"markdown", "ascii", "unicode"}:
                    rows.append(row_values)
                else:
                    lines.append("\t".join(row_values))
                rows_copied += 1

            next_cursor = base_row + height
            if next_cursor <= cursor:
                cursor += max(1, height)
            else:
                cursor = next_cursor

        if rows_copied <= 0:
            viewer.status_message = (
                "no selected rows in region" if selection_active else "no rows to copy"
            )
            return

        if format_name == "markdown":
            header_line = "| " + " | ".join(header_cells) + " |"
            sep_line = "| " + " | ".join("---" for _ in header_cells) + " |"
            row_lines = ["| " + " | ".join(row) + " |" for row in rows]
            payload = "\n".join([header_line, sep_line, *row_lines])
        elif format_name in {"ascii", "unicode"}:
            widths = [len(cell) for cell in header_cells]
            for row in rows:
                for idx, cell in enumerate(row):
                    widths[idx] = max(widths[idx], len(cell))

            def _pad_cells(cells: list[str]) -> list[str]:
                return [
                    f" {cell}{' ' * (width - len(cell))} "
                    for cell, width in zip(cells, widths, strict=True)
                ]

            if format_name == "unicode":
                top = "┌" + "┬".join("─" * (width + 2) for width in widths) + "┐"
                mid = "├" + "┼".join("─" * (width + 2) for width in widths) + "┤"
                bottom = "└" + "┴".join("─" * (width + 2) for width in widths) + "┘"
                vert = "│"
            else:
                top = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
                mid = top
                bottom = top
                vert = "|"
            header = vert + vert.join(_pad_cells(header_cells)) + vert
            row_lines = [vert + vert.join(_pad_cells(row)) + vert for row in rows]
            payload = "\n".join([top, header, mid, *row_lines, bottom])
        else:
            payload = "\n".join(lines)
        self._copy_to_clipboard(
            payload,
            success_message=f"copied {rows_copied}x{len(selected_columns)} region to clipboard",
            failure_message="clipboard unavailable",
        )
