from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import polars as pl
import pytest

from pulka.api.session import Session
from pulka.core.sheet_actions import resolve_enter_action
from pulka.core.viewer import Viewer
from pulka.data.scanners import ScannerRegistry
from pulka.render.viewport_plan import compute_viewport_plan
from pulka.sheets.data_sheet import DataSheet
from pulka.sheets.file_browser_sheet import FileBrowserSheet
from pulka.tui.screen import Screen


def _create_sheet(path: Path, job_runner) -> FileBrowserSheet:
    return FileBrowserSheet(path, scanners=ScannerRegistry(), runner=job_runner)


def test_file_browser_layout_hints(tmp_path: Path, job_runner):
    sheet = _create_sheet(tmp_path, job_runner)

    assert sheet.compact_width_layout is False
    assert sheet.preferred_fill_column == "name"


def test_file_browser_lists_supported_entries(tmp_path: Path, job_runner) -> None:
    (tmp_path / "subdir").mkdir()
    (tmp_path / "data.csv").write_text("a,b\n1,2\n")
    (tmp_path / "workbook.xlsx").write_text("noop")
    (tmp_path / "ignore.txt").write_text("noop")

    sheet = _create_sheet(tmp_path, job_runner)
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]

    assert "subdir/" in names
    assert "data.csv" in names
    assert "workbook.xlsx" in names
    assert "ignore.txt" not in names
    if tmp_path.parent != tmp_path:
        assert names[0] == ".."


def test_file_browser_actions(tmp_path: Path, job_runner) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a\n1\n")
    sheet = _create_sheet(tmp_path, job_runner)

    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    dir_row = names.index("nested/")
    file_row = names.index("sample.csv")

    dir_action = sheet.action_for_row(dir_row)
    file_action = sheet.action_for_row(file_row)

    assert dir_action is not None
    assert dir_action.type == "enter-directory"
    assert dir_action.path == nested

    assert file_action is not None
    assert file_action.type == "open-file"
    assert file_action.path == csv_path

    dir_viewer = SimpleNamespace(sheet=sheet, cur_row=dir_row)
    file_viewer = SimpleNamespace(sheet=sheet, cur_row=file_row)

    dir_enter = resolve_enter_action(dir_viewer)
    file_enter = resolve_enter_action(file_viewer)

    assert dir_enter is not None
    assert dir_enter.kind == "open-path"
    assert dir_enter.open_as == "directory"
    assert dir_enter.path == nested

    assert file_enter is not None
    assert file_enter.kind == "open-path"
    assert file_enter.open_as == "dataset"
    assert file_enter.path == csv_path


def test_file_browser_viewport_navigation_commands(tmp_path: Path, job_runner) -> None:
    for idx in range(8):
        (tmp_path / f"file-{idx}.csv").write_text("a\n1\n")

    sheet = _create_sheet(tmp_path, job_runner)
    session = Session(None, initial_sheet=sheet, viewport_rows=5)
    viewer = session.viewer
    assert viewer is not None

    try:
        viewer.configure_terminal(width=80, height=5)
        viewer.get_visible_table_slice(viewer.columns)
        visible_rows = viewer.visible_row_positions
        assert len(visible_rows) >= 2

        runtime = session.command_runtime

        viewer.cur_row = visible_rows[-1]
        runtime.invoke("move_viewport_top", source="test")
        assert viewer.cur_row == viewer.visible_row_positions[0]

        viewer.get_visible_table_slice(viewer.columns)
        viewer.cur_row = viewer.visible_row_positions[0]
        runtime.invoke("move_viewport_middle", source="test")
        middle_row = viewer.visible_row_positions[(len(viewer.visible_row_positions) - 1) // 2]
        assert viewer.cur_row == middle_row

        viewer.get_visible_table_slice(viewer.columns)
        viewer.cur_row = viewer.visible_row_positions[0]
        runtime.invoke("move_viewport_bottom", source="test")
        assert viewer.cur_row == viewer.visible_row_positions[-1]

        viewer.get_visible_table_slice(viewer.columns)
        viewer.cur_row = viewer.visible_row_positions[0]
        runtime.invoke("move_center_row", source="test")
        assert viewer.status_message == "not enough rows to center"
    finally:
        session.close()


def test_file_browser_can_jump_to_new_directory(tmp_path: Path, job_runner) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    sheet = _create_sheet(tmp_path, job_runner)

    child_sheet = sheet.at_path(nested)
    assert child_sheet.display_path.endswith("nested")
    if nested.parent != nested:
        assert child_sheet.value_at(0, "name") == ".."


def test_file_browser_parent_preserves_symlink_parent(tmp_path: Path, job_runner) -> None:
    target_root = tmp_path / "real-root"
    target_child = target_root / "child"
    target_child.mkdir(parents=True)
    link = tmp_path / "link"
    try:
        link.symlink_to(target_child, target_is_directory=True)
    except (OSError, NotImplementedError):  # pragma: no cover - platform dependent
        pytest.skip("symlink not supported on this platform")

    sheet = _create_sheet(link, job_runner)
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert names[0] == ".."
    parent_action = sheet.action_for_row(0)
    assert parent_action is not None
    assert parent_action.type == "enter-directory"
    assert parent_action.path == tmp_path


def test_file_browser_relative_path_uses_logical_pwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, job_runner
) -> None:
    real_root = tmp_path / "real-root"
    (real_root / "child").mkdir(parents=True)
    logical_root = tmp_path / "logical-root"
    logical_root.mkdir()
    link = logical_root / "current"
    try:
        link.symlink_to(real_root, target_is_directory=True)
    except (OSError, NotImplementedError):  # pragma: no cover - platform dependent
        pytest.skip("symlink not supported on this platform")

    monkeypatch.chdir(real_root)
    monkeypatch.setenv("PWD", str(link))

    sheet = _create_sheet(Path(), job_runner)
    assert sheet.directory == link
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert "child/" in names
    assert names[0] == ".."
    parent_action = sheet.action_for_row(0)
    assert parent_action is not None
    assert parent_action.type == "enter-directory"
    assert parent_action.path == logical_root


def test_file_browser_relative_path_ignores_stale_pwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, job_runner
) -> None:
    real_root = tmp_path / "real-root"
    stale_root = tmp_path / "stale-root"
    real_root.mkdir()
    stale_root.mkdir()

    monkeypatch.chdir(real_root)
    monkeypatch.setenv("PWD", str(stale_root))

    sheet = _create_sheet(Path(), job_runner)
    assert sheet.directory == real_root


def test_file_browser_len_matches_row_count(tmp_path: Path, job_runner) -> None:
    (tmp_path / "data.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path, job_runner)
    assert len(sheet) == sheet.row_count()


def test_file_browser_cache_version_updates_on_refresh(tmp_path: Path, job_runner) -> None:
    sheet = _create_sheet(tmp_path, job_runner)
    start_version = sheet.cache_version

    (tmp_path / "new.csv").write_text("a\n1\n")

    assert sheet.refresh_from_disk()
    assert sheet.cache_version != start_version


def test_file_browser_can_show_unknown_when_configured(
    tmp_path: Path, monkeypatch, job_runner
) -> None:
    import pulka.data.scan as scan_mod

    (tmp_path / "data").write_text("x")

    monkeypatch.setattr(scan_mod, "_BROWSER_STRICT_EXTENSIONS", False)
    sheet = _create_sheet(tmp_path, job_runner)
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert "data" in names


def test_insight_panel_allowed_after_browser_open(tmp_path: Path, job_runner) -> None:
    data_path = tmp_path / "sample.csv"
    data_path.write_text("a\n1\n")

    browser = _create_sheet(tmp_path, job_runner)
    session = Session(None, initial_sheet=browser)
    screen = Screen(session.viewer)
    try:
        assert not screen._insight_allowed  # browser should disable insight

        screen._open_file_from_browser(data_path)

        assert not getattr(screen.viewer.sheet, "is_file_browser", False)
        assert screen._insight_allowed
    finally:
        unsubscribe = getattr(screen, "_view_stack_unsubscribe", None)
        if callable(unsubscribe):
            unsubscribe()


def test_file_browser_maximizes_name_column(tmp_path: Path, job_runner) -> None:
    (tmp_path / "data.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path, job_runner)

    viewer = Viewer(sheet, runner=job_runner)

    assert viewer.width_mode_state["mode"] == "default"
    assert viewer.maximized_column_index is None

    plan = compute_viewport_plan(viewer, width=120, height=10)
    name_plan = next(col for col in plan.columns if col.name == "name")
    other_widths = [col.width for col in plan.columns if col.name in {"type", "size", "modified"}]

    assert name_plan.width > max(other_widths)


def test_file_browser_width_resets_after_replacing_sheet(tmp_path: Path, job_runner) -> None:
    (tmp_path / "data.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path, job_runner)
    viewer = Viewer(sheet, runner=job_runner)

    df = pl.DataFrame({"value": [1, 2]}).lazy()
    data_sheet = DataSheet(df, runner=job_runner)
    viewer.replace_sheet(data_sheet)

    assert viewer.width_mode_state["mode"] == "default"
    assert viewer.maximized_column_index is None


def test_file_browser_replacing_sheet_clears_viewport_body_cache(
    tmp_path: Path, job_runner
) -> None:
    dir_a = tmp_path / "a"
    dir_b = tmp_path / "b"
    dir_a.mkdir()
    dir_b.mkdir()
    (dir_a / "alpha.csv").write_text("x\n1\n")
    (dir_b / "beta.csv").write_text("y\n2\n")

    viewer = Viewer(_create_sheet(dir_a, job_runner), runner=job_runner)

    plan_a = compute_viewport_plan(viewer, width=80, height=10)
    name_idx = next(idx for idx, col in enumerate(plan_a.columns) if col.name == "name")
    file_row_a = plan_a.cells[2][name_idx].text.strip()
    assert file_row_a == "alpha.csv"

    viewer.replace_sheet(_create_sheet(dir_b, job_runner))

    plan_b = compute_viewport_plan(viewer, width=80, height=10)
    name_idx_b = next(idx for idx, col in enumerate(plan_b.columns) if col.name == "name")
    file_row_b = plan_b.cells[2][name_idx_b].text.strip()
    assert file_row_b == "beta.csv"


def test_file_browser_refresh_detects_directory_changes(tmp_path: Path, job_runner) -> None:
    (tmp_path / "alpha.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path, job_runner)

    # No changes yet
    assert sheet.refresh_from_disk() is False

    beta = tmp_path / "beta.csv"
    beta.write_text("b\n2\n")

    assert sheet.refresh_from_disk() is True
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert "beta.csv" in names

    sizes_snapshot = [sheet.value_at(idx, "size") for idx in range(sheet.row_count() or 0)]

    # Re-running without touching the filesystem should report no change
    assert sheet.refresh_from_disk() is False

    alpha = tmp_path / "alpha.csv"
    alpha.write_text("a\n1\n2\n")

    assert sheet.refresh_from_disk() is True
    sizes = [sheet.value_at(idx, "size") for idx in range(sheet.row_count() or 0)]
    assert sizes != sizes_snapshot


def test_file_browser_sort_keeps_dirs_first(tmp_path: Path, job_runner) -> None:
    (tmp_path / "zzz-dir").mkdir()
    (tmp_path / "aaa.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path, job_runner)
    viewer = Viewer(sheet, runner=job_runner)

    viewer.set_sort_direction(desc=False, stack=False, col_name="name")

    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    first_non_parent = next(name for name in names if name != "..")
    assert first_non_parent.endswith("/")


def test_file_browser_delete_entries(tmp_path: Path, job_runner) -> None:
    remove_me = tmp_path / "remove.csv"
    remove_me.write_text("a\n1\n")
    keep_me = tmp_path / "keep.csv"
    keep_me.write_text("a\n1\n")

    sheet = _create_sheet(tmp_path, job_runner)
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    delete_row = names.index("remove.csv")

    targets = sheet.deletable_entries_for_rows([delete_row])
    assert len(targets) == 1

    result = sheet.delete_entries(targets)

    assert not remove_me.exists()
    assert keep_me.exists()
    assert result.deleted == (remove_me,)
    assert not result.errors

    refreshed = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert "remove.csv" not in refreshed
    assert "keep.csv" in refreshed


def test_file_browser_delete_directory_recursive(tmp_path: Path, job_runner) -> None:
    folder = tmp_path / "folder"
    folder.mkdir()
    (folder / "inner.csv").write_text("a\n1\n")
    nested = folder / "nested"
    nested.mkdir()
    (nested / "deep.csv").write_text("a\n2\n")

    sheet = _create_sheet(tmp_path, job_runner)
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    folder_row = names.index("folder/")

    targets = sheet.deletable_entries_for_rows([folder_row])
    assert len(targets) == 1

    file_count, count_errors = sheet.deletion_impact(targets)
    assert count_errors == []
    assert file_count == 2

    result = sheet.delete_entries(targets)
    assert not folder.exists()
    assert result.deleted == (folder,)
