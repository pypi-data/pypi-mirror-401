from __future__ import annotations

from dataclasses import dataclass

from pulka.core.engine.contracts import TableColumn, TableSlice
from pulka.core.plan import QueryPlan
from pulka.core.viewer.search import SearchController


@dataclass
class _FakeSheet:
    data: list[str | None]
    starts: list[int]

    def fetch_slice(self, start: int, count: int, columns: list[str]):
        self.starts.append(start)
        if not columns:
            return TableSlice.empty()
        column = columns[0]
        if start < 0 or count <= 0:
            return TableSlice.empty(columns=[column], schema={column: None})
        slice_data = self.data[start : start + count] if start < len(self.data) else []
        null_count = sum(1 for val in slice_data if val is None)
        table_column = TableColumn(column, slice_data, None, null_count)
        return TableSlice((table_column,), {column: None}, start_offset=start)


@dataclass
class _FakeNav:
    sheet: _FakeSheet
    plan: QueryPlan

    columns: list[str]
    cur_row: int
    cur_col: int
    row0: int
    status_message: str | None = None

    @property
    def row_provider(self):
        return None

    def clamp(self) -> None:
        self.cur_row = max(0, min(self.cur_row, len(self.sheet.data) - 1))
        self.row0 = max(0, self.row0)

    def center_current_row(self) -> None:
        half = max(1, self._body_view_height()) // 2
        self.row0 = max(self._effective_frozen_row_count(), self.cur_row - half)

    def _body_view_height(self) -> int:
        return 10

    def _effective_frozen_row_count(self) -> int:
        return 0

    def _current_plan(self) -> QueryPlan | None:
        return self.plan

    def _ensure_total_rows(self) -> int | None:
        return len(self.sheet.data)


def test_search_uses_cached_chunks_for_next_match() -> None:
    data = ["x"] * 30
    data[10] = "foo"
    data[20] = "foo"
    sheet = _FakeSheet(data=data, starts=[])
    nav = _FakeNav(
        sheet=sheet,
        plan=QueryPlan(),
        columns=["col"],
        cur_row=0,
        cur_col=0,
        row0=0,
    )
    search = SearchController(nav)
    search.set_search("foo")

    assert search.search(forward=True, include_current=False, center=False, wrap=True) is True
    assert nav.cur_row == 10
    assert sheet.starts == [1, 11]

    assert search.search(forward=True, include_current=False, center=False, wrap=True) is True
    assert nav.cur_row == 20
    assert sheet.starts.count(11) == 1
