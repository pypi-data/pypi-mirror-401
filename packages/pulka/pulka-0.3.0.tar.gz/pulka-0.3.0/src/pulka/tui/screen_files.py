"""File browser and dataset change handling for the TUI screen."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from contextlib import suppress
from pathlib import Path
from typing import Any

from prompt_toolkit.widgets import Button, Dialog

from ..core.sheet_actions import SheetEnterAction
from ..core.sheet_traits import resolve_display_path, resolve_sheet_traits
from ..sheets.file_browser_sheet import FileDeletionResult
from . import modals as tui_modals
from .controllers.dataset_reload import DatasetReloadController
from .controllers.file_browser import FileBrowserController
from .controllers.file_ops import FileOpsController
from .controllers.file_watch import FileSnapshot, FileWatchController


class ScreenFileController:
    """Coordinate file browser actions and dataset reload prompts."""

    def __init__(
        self,
        *,
        get_viewer: Callable[[], Any],
        get_session: Callable[[], Any],
        get_file_watch: Callable[[], FileWatchController | None],
        get_hooks: Callable[[], Any],
        get_app: Callable[[], Any],
        file_browser: FileBrowserController,
        file_ops: FileOpsController,
        dataset_reload: DatasetReloadController,
        refresh: Callable[[], None],
        invalidate: Callable[[], None],
        apply_insight_state: Callable[[], None],
        display_modal: Callable[..., None],
        remove_modal: Callable[..., None],
        open_missing_dataset_modal: Callable[..., None],
    ) -> None:
        self._get_viewer = get_viewer
        self._get_session = get_session
        self._get_file_watch = get_file_watch
        self._get_hooks = get_hooks
        self._get_app = get_app
        self._file_browser = file_browser
        self._file_ops = file_ops
        self._dataset_reload = dataset_reload
        self._refresh = refresh
        self._invalidate = invalidate
        self._apply_insight_state = apply_insight_state
        self._display_modal = display_modal
        self._remove_modal = remove_modal
        self._open_missing_dataset_modal = open_missing_dataset_modal

    def handle_open_path_action(self, action: SheetEnterAction) -> None:
        if action.open_as == "directory":
            self.enter_browser_directory(action.path)
            return
        if action.open_as == "dataset":
            self.open_dataset_from_action(action.path)
            return

    def enter_browser_directory(self, target: Path | None) -> None:
        viewer = self._get_viewer()
        session = self._get_session()
        if viewer is None or session is None:
            return
        if target is None:
            viewer.status_message = "entry is not openable"
            self._refresh()
            return
        sheet = getattr(viewer, "sheet", None)
        builder = getattr(sheet, "at_path", None)
        if not callable(builder):
            viewer.status_message = "browser cannot change directory"
            self._refresh()
            return
        try:
            new_sheet = builder(target)
        except FileNotFoundError:
            viewer.status_message = f"directory not found: {target}"
            self._refresh()
            return
        except Exception as exc:
            viewer.status_message = f"dir open failed: {exc}"
            self._refresh()
            return

        refresh_from_disk = getattr(new_sheet, "refresh_from_disk", None)
        if callable(refresh_from_disk):
            with suppress(Exception):
                refresh_from_disk()

        source_label = resolve_display_path(new_sheet, fallback=str(target))
        viewer.replace_sheet(new_sheet, source_path=source_label)
        with suppress(Exception):
            viewer._clear_selection_state()
        with suppress(Exception):
            viewer.row_count_tracker.ensure_total_rows()
        message = getattr(new_sheet, "status_message", None)
        if not message:
            count = new_sheet.row_count() or 0
            message = f"{count} entries"
        viewer.status_message = message
        self.after_file_browser_directory_change()
        self._refresh()

    def open_dataset_from_action(self, target: Path | None) -> None:
        viewer = self._get_viewer()
        session = self._get_session()
        file_watch = self._get_file_watch()
        if viewer is None or session is None:
            return
        if target is None:
            viewer.status_message = "entry is not openable"
            self._refresh()
            return
        try:
            session.open_dataset_viewer(target, base_viewer=viewer)
        except FileNotFoundError:
            viewer.status_message = f"path not found: {target}"
            self._refresh()
            return
        except Exception as exc:
            viewer.status_message = f"open failed: {exc}"
            self._refresh()
            return
        viewer.status_message = f"opened {target.name or target}"
        if file_watch is not None:
            file_watch.sync(force=True)
        self._refresh()

    def after_file_browser_directory_change(self) -> None:
        viewer = self._get_viewer()
        file_watch = self._get_file_watch()
        if file_watch is not None:
            file_watch.sync_file_browser(force=True)
        self._apply_insight_state()
        if viewer is not None:
            with suppress(Exception):
                viewer.row_count_tracker.ensure_total_rows()

    def path_completion_base_dir(self) -> Path:
        viewer = self._get_viewer()
        session = self._get_session()
        sheet = getattr(viewer, "sheet", None)
        directory = getattr(sheet, "directory", None) if sheet is not None else None
        if directory:
            with suppress(Exception):
                return Path(directory)
        command_cwd = getattr(session, "command_cwd", None) if session is not None else None
        if command_cwd:
            with suppress(Exception):
                return Path(command_cwd)
        dataset_path = getattr(session, "dataset_path", None) if session is not None else None
        if dataset_path:
            with suppress(Exception):
                ds_path = Path(dataset_path)
                return ds_path if ds_path.is_dir() else ds_path.parent
        return Path.cwd()

    def open_file_from_browser(self, target: Path) -> None:
        viewer = self._get_viewer()
        session = self._get_session()
        file_watch = self._get_file_watch()
        if viewer is None or session is None:
            return
        try:
            session.open_dataset_viewer(target, base_viewer=viewer)
        except Exception as exc:
            viewer.status_message = f"open failed: {exc}"
            self._refresh()
            return
        viewer.status_message = f"opened {target.name or target}"
        if file_watch is not None:
            file_watch.sync(force=True)
        self._refresh()

    def file_browser_delete_targets(self, sheet) -> list[object]:
        viewer = self._get_viewer()
        if viewer is None:
            return []
        targets, status = self._file_browser.resolve_entries(deletable=True, viewer=viewer)
        if status:
            viewer.status_message = status
        if targets:
            return targets
        self._refresh()
        return []

    def file_browser_entries(self, sheet) -> list[object]:
        viewer = self._get_viewer()
        if viewer is None:
            return []
        targets, status = self._file_browser.resolve_entries(viewer=viewer)
        if status:
            viewer.status_message = status
        if targets:
            return targets
        self._refresh()
        return []

    def open_file_delete_modal(self, event) -> None:
        viewer = self._get_viewer()
        sheet = getattr(viewer, "sheet", None) if viewer is not None else None
        if viewer is None or sheet is None or not resolve_sheet_traits(sheet).is_file_browser:
            return

        targets = self.file_browser_delete_targets(sheet)
        if not targets:
            return

        count = len(targets)
        title = "Delete item" if count == 1 else "Delete items"
        name = targets[0].path.name if count == 1 else None
        has_dir = any(getattr(entry, "is_dir", False) for entry in targets)

        try:
            file_count, impact_errors = sheet.deletion_impact(targets)
        except Exception:
            file_count, impact_errors = 0, []

        message_lines = []
        if count == 1:
            if has_dir:
                message_lines.append(f"Delete folder {name or 'item'} and its contents?")
            else:
                message_lines.append(f"Delete {name or 'file'}?")
        else:
            kind = "items" if has_dir else "files"
            message_lines.append(f"Delete all {count} selected {kind}?")

        suffix = "" if file_count == 1 else "s"
        recurse_note = " recursively" if has_dir else ""
        message_lines.append(f"This will delete {file_count} file{suffix}{recurse_note}.")
        if impact_errors:
            path, err = impact_errors[0]
            message_lines.append(f"Count may be incomplete ({path}: {err})")

        body = tui_modals.build_lines_body(message_lines)
        app = event.app

        def _resolve(confirmed: bool) -> None:
            self._remove_modal(app)
            if confirmed:
                self.delete_file_browser_entries(sheet, targets)

        yes_button = Button(text="Yes", handler=lambda: _resolve(True))
        cancel_button = Button(text="Cancel", handler=lambda: _resolve(False))

        dialog = Dialog(
            title=title,
            body=body,
            buttons=[yes_button, cancel_button],
        )
        self._display_modal(
            app,
            dialog,
            focus=yes_button,
            context_type="file_delete",
            payload={"count": count},
            width=60,
        )

    def delete_file_browser_entries(self, sheet, entries: Sequence[object]) -> None:
        viewer = self._get_viewer()
        if viewer is None:
            return

        try:
            result: FileDeletionResult = self._file_browser.delete_entries(sheet, entries)
        except Exception as exc:
            viewer.status_message = f"delete failed: {exc}"
            self._refresh()
            return

        with suppress(Exception):
            viewer.clear_row_selection()

        message = "No items deleted"
        if result.deleted:
            if len(result.deleted) == 1:
                target = result.deleted[0]
                message = f"Deleted {target.name or target}"
            else:
                message = f"Deleted {len(result.deleted)} items"

        if result.errors:
            path, error = result.errors[0]
            prefix = f"{message}; " if result.deleted else "Delete failed: "
            message = f"{prefix}{path.name}: {error}"

        if result.changed or result.errors:
            self.handle_file_browser_refresh(sheet)

        viewer.status_message = message[:120]
        self._refresh()

    def request_file_transfer(
        self, operation: str, dest: str, *, source_paths: Sequence[Path] | None = None
    ) -> None:
        self._file_ops.request_transfer(operation, dest, source_paths=source_paths)

    def request_file_rename(self, new_name: str) -> None:
        self._file_ops.request_rename(new_name)

    def request_file_mkdir(self, path: str) -> None:
        self._file_ops.request_mkdir(path)

    def perform_file_transfer(
        self, operation: str, targets: list[tuple[Path, Path]], *, allow_overwrite: bool = False
    ) -> None:
        self._file_ops.perform_transfer(operation, targets, allow_overwrite=allow_overwrite)

    def reload_dataset(self) -> None:
        self._dataset_reload.reload_dataset()

    @staticmethod
    def is_missing_error(exc: Exception) -> bool:
        return DatasetReloadController.is_missing_error(exc)

    def handle_missing_dataset(self, dataset_path: Path) -> None:
        self._dataset_reload.handle_missing_dataset(dataset_path)

    def handle_reload_error(self, exc: Exception, dataset_path: Path) -> None:
        self._dataset_reload.handle_reload_error(exc, dataset_path)

    def handle_file_browser_refresh(self, sheet) -> None:
        viewer = self._get_viewer()
        if viewer is None or viewer.sheet is not sheet:
            return
        self._file_browser.refresh_sheet(sheet, viewer)
        self._invalidate()

    def handle_file_browser_error(self, exc: Exception) -> None:
        viewer = self._get_viewer()
        if viewer is not None:
            viewer.status_message = f"dir refresh failed: {exc}"
        self._invalidate()

    def check_dataset_file_changes(self, *, force: bool = False) -> None:
        file_watch = self._get_file_watch()
        if file_watch is None:
            return
        file_watch.check_dataset(force=force)

    def check_file_browser_changes(self, *, force: bool = False) -> None:
        file_watch = self._get_file_watch()
        if file_watch is None:
            return
        file_watch.check_file_browser(force=force)

    def file_watch_prompt_active(self) -> bool:
        file_watch = self._get_file_watch()
        return bool(file_watch and file_watch.dataset_prompt_active)

    def set_file_watch_prompt_active(self, active: bool) -> None:
        file_watch = self._get_file_watch()
        if file_watch is None:
            return
        if active:
            file_watch.set_dataset_prompt_active(True)
        else:
            file_watch.clear_dataset_prompt()

    def schedule_file_change_prompt(
        self,
        path: Path,
        snapshot: FileSnapshot | None,
    ) -> None:
        def _open_prompt() -> None:
            self.open_dataset_file_change_modal(path=path, snapshot=snapshot)

        hooks = self._get_hooks()
        if hooks is None:
            _open_prompt()
            return
        hooks.call_soon(_open_prompt)

    def open_dataset_file_change_modal(
        self,
        *,
        path: Path,
        snapshot: FileSnapshot | None,
    ) -> None:
        file_watch = self._get_file_watch()
        if file_watch is None:
            return
        if file_watch.dataset_path != path:
            file_watch.clear_dataset_prompt()
            return
        if snapshot is None:
            snapshot = FileSnapshot(
                mtime_ns=None,
                size=None,
                inode=None,
                missing=True,
                error=None,
            )
        if snapshot.missing:
            self._open_missing_dataset_modal(path=path, snapshot=snapshot)
            return
        message_lines = [
            f"{path} changed on disk while Pulka is running.",
        ]
        if snapshot.missing:
            missing_reason = snapshot.error or "The file may have been deleted or replaced."
            message_lines.append(missing_reason)
        else:
            message_lines.append("Reload to view the latest data or keep the current snapshot.")

        body = tui_modals.build_lines_body(message_lines)
        app = self._get_app()
        if app is None:
            return

        def _resolve(reload_file: bool) -> None:
            self._remove_modal(app)
            self.complete_file_change_prompt(reload_file=reload_file)
            if not reload_file:
                self._refresh()

        reload_button = Button(text="Reload file", handler=lambda: _resolve(True))
        keep_button = Button(text="Keep current view", handler=lambda: _resolve(False))

        dialog = Dialog(
            title="File changed",
            body=body,
            buttons=[reload_button, keep_button],
        )
        self._display_modal(
            app,
            dialog,
            focus=reload_button,
            context_type="file_change",
            payload={"path": str(path)},
            width=80,
        )

    def complete_file_change_prompt(self, *, reload_file: bool) -> None:
        file_watch = self._get_file_watch()
        viewer = self._get_viewer()
        if file_watch is None or viewer is None:
            return
        file_watch.complete_dataset_prompt(refresh_snapshot=not reload_file)
        if reload_file:
            self.reload_dataset()
            return
        viewer.status_message = "file changed on disk (kept current view)"
        file_watch.sync_dataset(force=True)
