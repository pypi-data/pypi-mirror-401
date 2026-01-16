"""
Unit tests for navigation commands.

This module tests individual navigation operations like down/up clamping,
page up/down by viewport, gg/G, gh/gl, and z centering.
"""

from __future__ import annotations

import os
import re

import polars as pl
import pytest

from pulka.session import SessionRunner
from pulka.testing.data import make_df, write_df
from pulka.tui.screen import Screen

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(value: str) -> str:
    """Remove ANSI escape sequences from ``value`` for assertions."""

    return ANSI_RE.sub("", value)


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment."""
    os.environ["PULKA_TEST"] = "1"
    os.environ["TZ"] = "UTC"
    os.environ["LC_ALL"] = "C"


@pytest.fixture
def test_data_file(tmp_path):
    """Create a test data file."""
    df = make_df("mini_nav", rows=40, cols=6, seed=42)
    data_file = tmp_path / "test_nav.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


@pytest.fixture
def wide_data_file(tmp_path):
    """Create a wider test dataset to stress horizontal scrolling."""
    df = make_df("mini_nav", rows=40, cols=14, seed=99)
    data_file = tmp_path / "test_nav_wide.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


def test_column_search_across_offscreen_columns(wide_data_file):
    """Column search should consider columns that are not currently visible."""

    runner = SessionRunner(wide_data_file)
    try:
        session = runner.create_session(width=20, height=10)
        viewer = session.viewer
        assert viewer is not None

        screen = Screen(viewer)

        visible = set(viewer.visible_cols)
        assert len(visible) < len(viewer.columns)
        offscreen = [col for col in viewer.columns if col not in visible]
        assert offscreen

        target = offscreen[0]
        assert screen._apply_column_search(target) is True
        assert viewer.columns[viewer.cur_col] == target
    finally:
        runner.close()


def test_down_movement_clamping(test_data_file):
    """Test that down movement properly clamps at the bottom."""
    result = SessionRunner.run(
        test_data_file,
        ["move_down", "move_down", "move_down"],  # Move down a few times
        width=80,
        height=10,
        test_mode=True,
    )

    # Check that cursor moved down
    assert result.state_json["cursor_row"] == 3
    assert result.state_json["cursor_col"] == 0


def test_down_movement_bottom_clamp(test_data_file):
    """Test that down movement clamps at the bottom of the dataset."""
    # Try to move beyond the bottom
    commands = ["G", "move_down", "move_down", "move_down"]  # Go to bottom, then try to go further
    result = SessionRunner.run(test_data_file, commands, width=80, height=10, test_mode=True)

    # Should be at the last row (39 for 40-row dataset)
    assert result.state_json["cursor_row"] == 39


def test_up_movement_clamping(test_data_file):
    """Test that up movement properly clamps at the top."""
    result = SessionRunner.run(
        test_data_file,
        ["move_down", "move_down", "move_down", "move_up", "move_up"],  # Move down then back up
        width=80,
        height=10,
        test_mode=True,
    )

    # Should be at row 1
    assert result.state_json["cursor_row"] == 1


def test_up_movement_top_clamp(test_data_file):
    """Test that up movement clamps at the top of the dataset."""
    result = SessionRunner.run(
        test_data_file,
        ["move_up", "move_up", "move_up"],  # Try to move above top
        width=80,
        height=10,
        test_mode=True,
    )

    # Should be at row 0
    assert result.state_json["cursor_row"] == 0


def test_page_down_movement(test_data_file):
    """Test page down moves by viewport height."""
    viewport_height = 10
    result = SessionRunner.run(
        test_data_file, ["move_page_down"], width=80, height=viewport_height, test_mode=True
    )

    # Should move down by approximately viewport height (accounting for headers/status)
    # Actual viewport rows = height - 5 = 10 - 5 = 5
    expected_viewport_rows = max(1, viewport_height - 5)
    assert result.state_json["cursor_row"] == expected_viewport_rows


def test_page_up_movement(test_data_file):
    """Test page up moves by viewport height."""
    viewport_height = 10
    result = SessionRunner.run(
        test_data_file,
        ["move_page_down", "move_page_down", "move_page_up"],  # Go down then back up
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    # Should be somewhere in the middle after page up
    assert 5 <= result.state_json["cursor_row"] <= 15


def test_half_page_down_moves_within_viewport(test_data_file):
    """Half page down should jump to middle visible row without scrolling."""
    viewport_height = 12
    expected_view_rows = max(1, viewport_height - 5)

    result = SessionRunner.run(
        test_data_file,
        ["move_half_page_down"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    expected_middle = (expected_view_rows - 1) // 2
    assert result.state_json["top_row"] == 0
    assert result.state_json["cursor_row"] == expected_middle


def test_half_page_down_reaches_last_visible_row(test_data_file):
    """Half page down twice should land on the last visible row."""
    viewport_height = 12
    expected_view_rows = max(1, viewport_height - 5)

    result = SessionRunner.run(
        test_data_file,
        ["move_half_page_down", "move_half_page_down"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    expected_last = expected_view_rows - 1
    assert result.state_json["top_row"] == 0
    assert result.state_json["cursor_row"] == expected_last


def test_half_page_right_moves_within_viewport(wide_data_file):
    """Half page right should jump to middle visible column without scrolling."""
    viewport_width = 40
    result = SessionRunner.run(
        wide_data_file,
        ["move_half_page_right"],
        width=viewport_width,
        height=10,
        test_mode=True,
    )

    expected_middle = result.state_json["left_col"] + (result.state_json["n_cols"] - 1) // 2
    assert result.state_json["left_col"] == 0
    assert result.state_json["cursor_col"] == expected_middle


def test_half_page_right_reaches_last_visible_column(wide_data_file):
    """Half page right twice should land on the last visible column."""
    viewport_width = 40
    result = SessionRunner.run(
        wide_data_file,
        ["move_half_page_right", "move_half_page_right"],
        width=viewport_width,
        height=10,
        test_mode=True,
    )

    expected_last = result.state_json["left_col"] + result.state_json["n_cols"] - 1
    assert result.state_json["left_col"] == 0
    assert result.state_json["cursor_col"] == expected_last


def test_half_page_left_returns_to_middle(wide_data_file):
    """Half page left should return to the middle visible column."""
    viewport_width = 40
    result = SessionRunner.run(
        wide_data_file,
        ["move_half_page_right", "move_half_page_right", "move_half_page_left"],
        width=viewport_width,
        height=10,
        test_mode=True,
    )

    expected_middle = result.state_json["left_col"] + (result.state_json["n_cols"] - 1) // 2
    assert result.state_json["left_col"] == 0
    assert result.state_json["cursor_col"] == expected_middle


def test_gg_top_navigation(test_data_file):
    """Test gg command goes to top."""
    result = SessionRunner.run(
        test_data_file,
        ["move_down", "move_down", "move_down", "gg"],  # Move down then go to top
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_row"] == 0
    assert result.state_json["top_row"] == 0


def test_g_bottom_navigation(test_data_file):
    """Test G command goes to bottom."""
    result = SessionRunner.run(test_data_file, ["G"], width=80, height=10, test_mode=True)

    # Should be at the last row
    assert result.state_json["cursor_row"] == 39  # 40 rows, 0-indexed


def test_gg_top_without_echo(test_data_file):
    """Ensure gg jumps instantly and doesn't echo the pressed key."""
    result = SessionRunner.run(
        test_data_file,
        ["G", "gg"],
        width=80,
        height=10,
        test_mode=True,
    )

    first_line = result.frames[-1].splitlines()[0]
    assert not first_line.startswith("g")
    assert result.state_json["cursor_row"] == 0


def test_gh_first_column(test_data_file):
    """Test gh command goes to first column."""
    result = SessionRunner.run(
        test_data_file,
        ["move_right", "move_right", "move_right", "gh"],  # Move right then go to first
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 0


def test_gl_last_column(test_data_file):
    """Test gl command goes to last column."""
    result = SessionRunner.run(test_data_file, ["gl"], width=80, height=10, test_mode=True)

    # Should be at the last column (5 for 6-column dataset)
    assert result.state_json["cursor_col"] == 5


def test_zt_aligns_current_row_to_top(test_data_file):
    """zt should scroll the current row to the top of the viewport."""
    viewport_height = 12
    result = SessionRunner.run(
        test_data_file,
        ["move_page_down", "move_down", "move_down", "zt"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    assert result.state_json["top_row"] == result.state_json["cursor_row"]
    assert result.state_json["top_row"] > 0


def test_zb_aligns_current_row_to_bottom(test_data_file):
    """zb should scroll the current row to the bottom of the viewport."""
    viewport_height = 12
    expected_view_rows = max(1, viewport_height - 5)

    result = SessionRunner.run(
        test_data_file,
        ["move_page_down", "move_down", "move_down", "move_down", "zb"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    expected_row0 = result.state_json["cursor_row"] - expected_view_rows + 1
    assert result.state_json["top_row"] == expected_row0


def test_zt_moves_to_first_visible_row(test_data_file):
    """zT should jump to the first row currently visible on screen."""
    viewport_height = 12
    result = SessionRunner.run(
        test_data_file,
        ["move_page_down", "move_down", "move_down", "zT"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    assert result.state_json["top_row"] > 0
    assert result.state_json["cursor_row"] == result.state_json["top_row"]


def test_zm_moves_to_middle_visible_row(test_data_file):
    """zM should jump to the middle row currently visible on screen."""
    viewport_height = 12
    expected_view_rows = max(1, viewport_height - 5)

    result = SessionRunner.run(
        test_data_file,
        ["move_page_down", "zM"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    expected_middle = result.state_json["top_row"] + (expected_view_rows - 1) // 2
    assert result.state_json["cursor_row"] == expected_middle


def test_zb_moves_to_last_visible_row(test_data_file):
    """zB should jump to the last row currently visible on screen."""
    viewport_height = 12
    expected_view_rows = max(1, viewport_height - 5)

    result = SessionRunner.run(
        test_data_file,
        ["move_page_down", "zB"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    expected_last = result.state_json["top_row"] + expected_view_rows - 1
    assert result.state_json["cursor_row"] == expected_last


def test_zt_reports_insufficient_rows_at_bottom(test_data_file):
    """zt should report when there are not enough rows below to align."""
    viewport_height = 12
    result = SessionRunner.run(
        test_data_file,
        ["G", "zt"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    status_line = strip_ansi(result.frames[-1]).lower()
    assert "not enough rows to move to top" in status_line


def test_zb_reports_insufficient_rows_at_top(test_data_file):
    """zb should report when there are not enough rows above to align."""
    viewport_height = 12
    result = SessionRunner.run(
        test_data_file,
        ["zb"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    status_line = strip_ansi(result.frames[-1]).lower()
    assert "not enough rows to move to bottom" in status_line


def test_zz_reports_insufficient_rows_to_center(test_data_file):
    """zz should report when there are not enough rows to center."""
    viewport_height = 12
    result = SessionRunner.run(
        test_data_file,
        ["zz"],
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    status_line = strip_ansi(result.frames[-1]).lower()
    assert "not enough rows to center" in status_line


def test_slide_column_left_command(test_data_file):
    """H should slide the current column one slot to the left."""
    result = SessionRunner.run(
        test_data_file,
        ["move_right", "move_right", "H"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 1
    assert result.state_json["col_order"][:3] == ["col_00", "col_02", "col_01"]


def test_slide_column_right_command(test_data_file):
    """L should slide the current column one slot to the right."""
    result = SessionRunner.run(
        test_data_file,
        ["move_right", "L"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 2
    assert result.state_json["col_order"][:3] == ["col_00", "col_02", "col_01"]


def test_slide_column_to_left_edge(test_data_file):
    """gH should move the active column to the far left."""
    result = SessionRunner.run(
        test_data_file,
        ["move_right", "move_right", "move_right", "gH"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 0
    assert result.state_json["col_order"][:4] == ["col_03", "col_00", "col_01", "col_02"]


def test_slide_column_to_right_edge(test_data_file):
    """gL should move the active column to the far right."""
    result = SessionRunner.run(
        test_data_file,
        ["move_right", "move_right", "gL"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["col_order"][-1] == "col_02"
    assert result.state_json["cursor_col"] == len(result.state_json["col_order"]) - 1


def test_slide_column_to_right_edge_scrolls_view(wide_data_file):
    """gL should keep the moved column selected and visible."""
    result = SessionRunner.run(
        wide_data_file,
        ["move_right", "move_right", "gL"],
        width=20,
        height=10,
        test_mode=True,
    )

    total_cols = pl.read_parquet(wide_data_file).width
    cursor_col = result.state_json["cursor_col"]
    left_col = result.state_json["left_col"]
    visible_cols = result.state_json["n_cols"]
    assert total_cols > visible_cols
    assert cursor_col == total_cols - 1
    assert left_col > 0
    assert cursor_col == left_col + max(visible_cols - 1, 0)


def test_slide_column_skips_hidden_columns(test_data_file):
    """Sliding should consider only visible columns when reordering."""
    result = SessionRunner.run(
        test_data_file,
        ["move_right", "drop", "H"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["col_order"][:2] == ["col_02", "col_00"]


def test_reset_drop_unhides_all_columns(test_data_file):
    """reset_drop should restore all dropped columns."""

    result = SessionRunner.run(
        test_data_file,
        ["drop", "reset_drop"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_cols"] == 6
    assert result.state_json["col_order"][:6] == [
        "col_00",
        "col_01",
        "col_02",
        "col_03",
        "col_04",
        "col_05",
    ]


def test_right_left_movement(test_data_file):
    """Test right and left movement with clamping."""
    result = SessionRunner.run(
        test_data_file,
        ["move_right", "move_right", "move_left"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 1


def test_right_movement_clamp(test_data_file):
    """Test right movement clamps at last column."""
    result = SessionRunner.run(
        test_data_file,
        [
            "move_right",
            "move_right",
            "move_right",
            "move_right",
            "move_right",
            "move_right",
            "move_right",
        ],  # Move beyond end
        width=80,
        height=10,
        test_mode=True,
    )

    # Should clamp at last column (5 for 6-column dataset)
    assert result.state_json["cursor_col"] == 5


def test_left_movement_clamp(test_data_file):
    """Test left movement clamps at first column."""
    result = SessionRunner.run(
        test_data_file,
        ["move_left", "move_left", "move_left"],  # Try to move before first column
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 0


def test_multiple_navigation_commands(test_data_file):
    """Test a sequence of navigation commands."""
    result = SessionRunner.run(
        test_data_file,
        ["move_down", "move_right", "move_down", "move_right", "move_up", "move_left"],
        width=80,
        height=10,
        test_mode=True,
    )

    # Final position should be row 1, col 1
    assert result.state_json["cursor_row"] == 1
    assert result.state_json["cursor_col"] == 1


@pytest.mark.parametrize(
    "command,expected_change",
    [
        ("move_down", (1, 0)),  # Move down 1 row
        ("move_up", (0, 0)),  # Can't move up from top
        ("move_right", (0, 1)),  # Move right 1 column
        ("move_left", (0, 0)),  # Can't move left from leftmost
    ],
)
def test_individual_navigation_commands(test_data_file, command, expected_change):
    """Test individual navigation commands from starting position."""
    result = SessionRunner.run(test_data_file, [command], width=80, height=10, test_mode=True)

    expected_row, expected_col = expected_change
    assert result.state_json["cursor_row"] == expected_row
    assert result.state_json["cursor_col"] == expected_col


def test_headless_invalid_filter_reports_status(test_data_file):
    """Invalid filter expressions should surface as status messages and continue."""

    result = SessionRunner.run(
        test_data_file,
        ["filter_expr c.col_00 >", "move_down"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert len(result.frames) >= 2
    status_line = strip_ansi(result.frames[1]).lower()
    assert "filter e" in status_line
    assert "nvalid filter syntax" in status_line
    assert result.state_json["cursor_row"] == 1


SQL_SUPPORTED = getattr(pl, "SQLContext", None) is not None


@pytest.mark.skipif(not SQL_SUPPORTED, reason="Polars SQL support not available")
def test_headless_invalid_sql_filter_reports_status(test_data_file):
    """Invalid SQL filters should report errors without aborting the script."""

    result = SessionRunner.run(
        test_data_file,
        ["filter_sql bad syntax", "move_down"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert len(result.frames) >= 2
    status_line = strip_ansi(result.frames[1]).lower()
    assert "sql filter err" in status_line
    assert result.state_json["cursor_row"] == 1


def test_filter_value_appends_current_cell(test_data_file):
    """'+' should append an equality filter for the active cell's value."""

    result = SessionRunner.run(
        test_data_file,
        ["filter_expr c.col_00 > 10", "move_down", "move_right", "+"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 5


def test_filter_value_handles_nulls(test_data_file):
    """'+' should append a filter when the focused value is null."""

    result = SessionRunner.run(
        test_data_file,
        ["move_down", "move_down", "move_down", "move_down", "move_down", "move_right", "+"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 6


def test_filter_value_not_excludes_current_cell(test_data_file):
    """'-' should append a negative filter for the active cell's value."""

    result = SessionRunner.run(
        test_data_file,
        ["-"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 39


def test_filter_value_not_handles_nulls(test_data_file):
    """'-' should exclude null values when focused on a null cell."""

    result = SessionRunner.run(
        test_data_file,
        ["move_right", "move_right", "-"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 34


@pytest.fixture
def long_run_data_file(tmp_path):
    """Create a dataset with long runs of identical values."""

    values = ["same"] * 2000 + ["break"] + ["tail"] * 1999
    df = pl.DataFrame({"col": values})
    data_file = tmp_path / "test_nav_long_runs.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


def test_next_different_scans_full_column(long_run_data_file):
    """> should find the next different value even when far away."""

    result = SessionRunner.run(
        long_run_data_file,
        [">"],
        width=80,
        height=15,
        test_mode=True,
    )

    assert result.state_json["cursor_row"] == 2000


def test_prev_different_scans_full_column(long_run_data_file):
    """< should find the previous different value even when far away."""

    result = SessionRunner.run(
        long_run_data_file,
        ["G", "<"],
        width=80,
        height=15,
        test_mode=True,
    )

    assert result.state_json["cursor_row"] == 2000
