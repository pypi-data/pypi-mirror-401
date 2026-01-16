from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from pulka.command.builtins import handle_move_file
from pulka.command.registry import CommandContext


class _FakeScreen:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, list[Path] | None]] = []

    def _request_file_transfer(
        self, operation: str, dest: str, *, source_paths: list[Path] | None = None
    ) -> None:
        self.calls.append((operation, dest, source_paths))


def test_move_command_parses_source_and_destination(tmp_path) -> None:
    src = tmp_path / "test.csv"
    src.write_text("a\n1\n")

    sheet = SimpleNamespace(is_file_browser=True, directory=tmp_path)
    viewer = SimpleNamespace(sheet=sheet, status_message=None)
    screen = _FakeScreen()

    context = CommandContext(sheet, viewer)
    context.screen = screen

    handle_move_file(context, ["test.csv data/"])

    assert screen.calls == [("move", "data/", [src.resolve()])]
