"""Unit tests for Viewer.move_rows invariants."""

from __future__ import annotations

import polars as pl

from pulka.core.viewer.viewer import Viewer
from pulka.sheets.data_sheet import DataSheet


def _make_viewer(df: pl.DataFrame, job_runner, *, rows: int = 10, width: int = 80) -> Viewer:
    sheet = DataSheet(df.lazy(), runner=job_runner)
    viewer = Viewer(sheet, viewport_rows=rows, runner=job_runner)
    viewer.configure_terminal(width, rows)
    return viewer


def test_move_rows_keeps_cursor_visible_known_total(job_runner) -> None:
    df = pl.DataFrame({"a": list(range(50))})
    viewer = _make_viewer(df, job_runner, rows=10)

    total_rows = viewer._ensure_total_rows()
    assert total_rows == 50

    body_height = viewer._body_view_height()
    viewer.move_rows(body_height + 2)

    assert viewer.cur_row == body_height + 2
    expected_row0 = max(
        viewer._effective_frozen_row_count(),
        viewer.cur_row - body_height + 1,
    )
    assert viewer.row0 == expected_row0
    assert viewer.row0 <= viewer.cur_row < viewer.row0 + body_height


def test_move_rows_respects_frozen_rows(job_runner) -> None:
    df = pl.DataFrame({"a": list(range(50))})
    viewer = _make_viewer(df, job_runner, rows=12)

    viewer.set_frozen_rows(2)
    frozen_min = viewer._effective_frozen_row_count()
    body_height = viewer._body_view_height()

    assert viewer.row0 >= frozen_min

    viewer.move_rows(1)
    assert viewer.cur_row == 1
    assert viewer.row0 == frozen_min

    viewer.move_rows(body_height + 3)
    expected_row0 = max(frozen_min, viewer.cur_row - body_height + 1)
    assert viewer.row0 == expected_row0
    assert viewer.row0 >= frozen_min


def test_move_rows_unknown_total_rows(job_runner) -> None:
    df = pl.DataFrame({"a": list(range(20))})
    viewer = _make_viewer(df, job_runner, rows=10)

    viewer._total_rows = None
    viewer._row_count_stale = True

    body_height = viewer._body_view_height()
    viewer.move_rows(100)

    assert viewer.cur_row == 100
    expected_row0 = max(
        viewer._effective_frozen_row_count(),
        viewer.cur_row - body_height + 1,
    )
    assert viewer.row0 == expected_row0
