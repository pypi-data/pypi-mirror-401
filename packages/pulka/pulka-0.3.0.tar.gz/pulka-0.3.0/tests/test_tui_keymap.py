from pathlib import Path

import pytest

from pulka.api.runtime import Runtime
from pulka.testing.data import make_df, write_df
from pulka.tui.keymap import KEY_ONLY_ACTION_SPECS
from pulka.tui.screen import Screen


@pytest.fixture
def sample_dataset(tmp_path: Path) -> str:
    df = make_df("mini_nav", rows=8, cols=3, seed=123)
    path = tmp_path / "runtime.parquet"
    write_df(df, path, "parquet")
    return str(path)


def _session_without_entrypoints(path: str):
    runtime = Runtime(load_entry_points=False)
    return runtime.open(path, viewport_rows=6)


def test_key_only_help_entries_match_spec(sample_dataset: str) -> None:
    session = _session_without_entrypoints(sample_dataset)
    screen = Screen(session.viewer)
    try:
        help_entries = screen.commands_help_entries()
        expected = {
            (spec.help_keys, spec.help_action, spec.help_description)
            for spec in KEY_ONLY_ACTION_SPECS
            if spec.add_help
        }
        expected.add(("rt<id>", "Remove transform", "Remove transform by id"))
        actual = {(entry.aliases, entry.command, entry.description) for entry in help_entries}
        assert actual == expected
    finally:
        unsubscribe = getattr(screen, "_view_stack_unsubscribe", None)
        if unsubscribe is not None:
            unsubscribe()
        session.close()
