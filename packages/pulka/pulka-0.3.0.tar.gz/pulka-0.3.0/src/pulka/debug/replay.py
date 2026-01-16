from __future__ import annotations

import io
import json
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from ..api import Session
from ..core.viewer import Viewer
from ..render.status_bar import render_status_line_text
from ..render.table import render_table
from ..tui.screen import Screen

_JSONL_SUFFIXES = {".jsonl", ".ndjson"}


@dataclass
class ReplayStep:
    """Normalized replay step for legacy or structured recorder logs."""

    kind: Literal["legacy_key", "command"]
    key: str | None = None
    name: str | None = None
    args: list[str] = field(default_factory=list)
    repeat: int = 1
    raw: str | None = None
    expected_state: dict[str, Any] | None = None


@dataclass
class ReplayState:
    """Captured state at a replay step."""

    step_index: int
    cursor_row: int
    cursor_col: int
    viewport_start_row: int
    viewport_start_col: int
    visible_columns: list[str]
    rendered_output: str
    status_message: str


class TUIReplayTool:
    """Tool for replaying flight recorder sessions in TUI."""

    def __init__(self):
        self.session_data: list[ReplayStep] = []
        self.current_step: int = 0
        self.viewer: Viewer | None = None
        self.screen: Screen | None = None
        self.session: Session | None = None

    def load_session(self, json_path: Path) -> None:
        """Load flight recorder JSON or JSONL file."""
        if not json_path.exists():
            raise FileNotFoundError(f"Flight recorder JSON file not found: {json_path}")

        if _is_jsonl_path(json_path):
            events = _load_jsonl_events(json_path)
            self.session_data = _steps_from_jsonl(events)
        else:
            data = _load_legacy_json(json_path)
            self.session_data = _steps_from_legacy(data)
        self.current_step = 0

    def setup_tui(self, data_file: Path) -> None:
        """Initialize TUI components for replay."""
        if not data_file.exists():
            raise FileNotFoundError(f"Data file not found: {data_file}")

        # Create a recorder with recording disabled for replay mode
        from ..logging import Recorder, RecorderConfig

        config = RecorderConfig(enabled=False)  # Disable recording during replay
        recorder = Recorder(config)

        # Create a session with the disabled recorder
        self.session = Session(str(data_file), recorder=recorder)
        self.viewer = self.session.viewer
        self.session.command_runtime.prepare_viewer(self.viewer)
        # Note: Screen is typically created when running the TUI app,
        # for replay we might not need it or we create a minimal one
        self.screen = (
            self.session.viewer
        )  # Use viewer as placeholder, will be set properly when needed

    def simulate_keypress(self, key: str) -> None:
        """Simulate a single keypress in the TUI."""
        if self.viewer is None:
            raise RuntimeError("TUI not initialized. Call setup_tui() first.")

        # Skip flight recorder toggle key during replay to avoid recursive recording
        if key == "@":
            return

        # Map key presses and commands to appropriate viewer method calls
        if key == "j" or key == "down":
            self.viewer.move_down()
        elif key == "k" or key == "up":
            self.viewer.move_up()
        elif key == "h" or key == "left":
            self.viewer.move_left()
        elif key == "l" or key == "right":
            self.viewer.move_right()
        elif key == " ":
            self.viewer.page_down()
        elif key == "b" or key == "B":  # vi-style page up
            self.viewer.page_up()
        elif key == "g":
            # This would be part of 'gg' sequence, but we handle single 'g' as go to top
            # For true 'gg' detection we'd need sequence tracking
            self.viewer.go_top()
        elif key == "G":
            # Go to bottom
            self.viewer.go_bottom()
        elif key == "$":
            # Move to last visible column
            self.viewer.last_col()
        elif key == "0":
            # Move to first visible column
            self.viewer.first_col()
        elif key == "[":
            # Sort descending by current column
            self.viewer.set_sort_direction(desc=True, stack=False)
        elif key == "]":
            # Sort ascending by current column
            self.viewer.set_sort_direction(desc=False, stack=False)
        elif key == "{":
            # Stack descending sort by current column
            self.viewer.set_sort_direction(desc=True, stack=True)
        elif key == "}":
            # Stack ascending sort by current column
            self.viewer.set_sort_direction(desc=False, stack=True)
        elif key == "r":
            # Reset filters - this would involve clearing the filter_text
            self.viewer.filter_text = None
        elif key == "f":
            # For filter, we can't simulate without a filter string
            # Just show a warning or skip
            pass
        elif key == "F":
            # Frequency table - this would change the viewer context
            pass
        elif key == "C":
            # Column summary - this would change the viewer context
            pass
        elif key == "T":
            # Transpose - this would change the viewer context
            pass
        elif key == "?":
            # Schema - this would change the viewer context
            pass
        elif key == "_":
            # Maximize current column
            self.viewer.toggle_maximize_current_col()
        elif key == "g_":
            # Maximize all columns
            self.viewer.toggle_maximize_all_cols()
        elif key == "q":
            # Quit - just ignore in replay mode
            pass
        else:
            # For now, just warn about unhandled keys
            # In a full implementation, we'd want to map all the key bindings
            print(f"Warning: Unhandled key command: {key}")

        # Refresh the viewer after command execution
        # Note: No refresh_needed attribute in Viewer class - the state is immediately updated
        # The viewer state is directly modified by the methods above

        # For screen refresh (if needed), we don't have a real screen in replay mode
        # but we ensure the viewer state is consistent
        self.viewer.clamp()  # Ensure state consistency

    def capture_current_state(self) -> ReplayState:
        """Capture current TUI state."""
        if self.viewer is None:
            raise RuntimeError("TUI not initialized. Call setup_tui() first.")

        # Extract current state from viewer
        cursor_row = self.viewer.cur_row
        cursor_col = self.viewer.cur_col

        # In the viewer class, row0 and col0 represent the viewport start
        viewport_start_row = self.viewer.row0
        viewport_start_col = self.viewer.col0

        # Calculate visible columns using same logic as flight recorder
        visible_columns = self.viewer.visible_cols

        # Capture rendered output
        table_output = render_table(self.viewer)
        status_output = render_status_line_text(self.viewer)
        self.viewer.acknowledge_status_rendered()
        rendered_output = table_output + "\n" + status_output

        # Capture status message if available
        status_message = getattr(self.viewer, "status_message", "")

        return ReplayState(
            step_index=self.current_step,
            cursor_row=cursor_row,
            cursor_col=cursor_col,
            viewport_start_row=viewport_start_row,
            viewport_start_col=viewport_start_col,
            visible_columns=visible_columns,
            rendered_output=rendered_output,
            status_message=status_message,
        )

    def replay_step(self) -> ReplayState:
        """Execute next command and return resulting state."""
        if self.current_step >= len(self.session_data):
            raise IndexError(f"Reached end of session data at step {self.current_step}")

        step = self.session_data[self.current_step]

        # Skip flight recorder toggle commands
        if step.kind == "legacy_key":
            command = step.key or ""
            if command == "@":
                self.current_step += 1
                return self.capture_current_state()
            self.simulate_keypress(command)
        else:
            if step.name:
                self._execute_command(step)

        # Increment step index
        self.current_step += 1

        # Return the resulting state
        return self.capture_current_state()

    def replay_until(self, step: int) -> ReplayState:
        """Replay commands up to specified step."""
        if step > len(self.session_data):
            raise ValueError(
                f"Requested step {step} exceeds session length {len(self.session_data)}"
            )

        # Replay commands from current step to target step
        while self.current_step < step:
            self.replay_step()

        # Return the final state
        return self.capture_current_state()

    def compare_states(self, expected: dict, actual: ReplayState) -> dict:
        """Compare expected vs actual state, return differences."""
        differences = {}
        normalized_expected = _normalize_expected_state(expected)

        # Compare each field and collect differences
        if normalized_expected.get("cursor_row") != actual.cursor_row:
            differences["cursor_row"] = {
                "expected": normalized_expected.get("cursor_row"),
                "actual": actual.cursor_row,
            }

        if normalized_expected.get("cursor_col") != actual.cursor_col:
            differences["cursor_col"] = {
                "expected": normalized_expected.get("cursor_col"),
                "actual": actual.cursor_col,
            }

        if normalized_expected.get("viewport_start_row") != actual.viewport_start_row:
            differences["viewport_start_row"] = {
                "expected": normalized_expected.get("viewport_start_row"),
                "actual": actual.viewport_start_row,
            }

        if normalized_expected.get("viewport_start_col") != actual.viewport_start_col:
            differences["viewport_start_col"] = {
                "expected": normalized_expected.get("viewport_start_col"),
                "actual": actual.viewport_start_col,
            }

        # Compare visible columns (list comparison)
        expected_visible = normalized_expected.get("visible_columns", [])
        actual_visible = actual.visible_columns
        if expected_visible != actual_visible:
            differences["visible_columns"] = {
                "expected": expected_visible,
                "actual": actual_visible,
            }

        # Compare status message
        expected_status = normalized_expected.get("status_message", "")
        actual_status = actual.status_message
        if expected_status != actual_status:
            differences["status_message"] = {"expected": expected_status, "actual": actual_status}

        return differences

    def expected_state_for_step(self, index: int) -> dict[str, Any] | None:
        if index < 0 or index >= len(self.session_data):
            return None
        return self.session_data[index].expected_state

    def _execute_command(self, step: ReplayStep) -> None:
        if self.session is None or self.viewer is None:
            raise RuntimeError("TUI not initialized. Call setup_tui() first.")
        result = self.session.command_runtime.invoke(
            step.name,
            args=step.args,
            repeat=step.repeat,
            source="replay",
            viewer=self.viewer,
        )
        if result.message:
            self.viewer.status_message = result.message
        self.viewer.clamp()


def _is_jsonl_path(path: Path) -> bool:
    suffixes = path.suffixes
    if not suffixes:
        return False
    if suffixes[-1] == ".zst":
        suffixes = suffixes[:-1]
    return bool(suffixes and suffixes[-1] in _JSONL_SUFFIXES)


def _load_legacy_json(path: Path) -> list[dict[str, Any]]:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise json.JSONDecodeError(
            f"Invalid JSON in flight recorder file: {exc}", exc.doc, exc.pos
        ) from None

    if not isinstance(data, list):
        raise ValueError("Flight recorder file must contain a JSON array")
    return data


def _steps_from_legacy(data: list[dict[str, Any]]) -> list[ReplayStep]:
    steps: list[ReplayStep] = []
    for i, record in enumerate(data):
        if not isinstance(record, dict):
            raise ValueError(f"Record {i} is not a JSON object")
        if "user_command" not in record or "viewer_state" not in record:
            raise ValueError(
                f"Record {i} missing required fields: 'user_command' or 'viewer_state'"
            )
        steps.append(
            ReplayStep(
                kind="legacy_key",
                key=str(record.get("user_command", "")),
                expected_state=record.get("viewer_state"),
            )
        )
    return steps


def _load_jsonl_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_no, line in enumerate(_iter_jsonl_lines(path), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL line {line_no}: {exc}") from None
        if not isinstance(payload, dict):
            raise ValueError(f"JSONL line {line_no} is not an object")
        events.append(payload)
    return events


def _iter_jsonl_lines(path: Path) -> Iterable[str]:
    if path.suffix == ".zst":
        try:
            import zstandard as zstd
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("zstandard is required to read .jsonl.zst recordings") from exc
        with (
            path.open("rb") as handle,
            zstd.ZstdDecompressor().stream_reader(handle) as reader,
            io.TextIOWrapper(reader, encoding="utf-8") as text_reader,
        ):
            yield from text_reader
    else:
        with path.open(encoding="utf-8") as handle:
            yield from handle


def _steps_from_jsonl(events: Iterable[dict[str, Any]]) -> list[ReplayStep]:
    steps: list[ReplayStep] = []
    last_state_step: ReplayStep | None = None
    for event in events:
        event_type = event.get("type")
        payload = event.get("payload", {})
        if event_type == "command":
            if not isinstance(payload, dict):
                continue
            name = payload.get("name")
            if not isinstance(name, str) or not name:
                continue
            raw = payload.get("raw")
            args = payload.get("args") if isinstance(payload.get("args"), list) else []
            args = [str(arg) for arg in args]
            repeat_value = payload.get("repeat", 1)
            try:
                repeat = max(1, int(repeat_value))
            except (TypeError, ValueError):
                repeat = 1
            step = ReplayStep(
                kind="command",
                name=name,
                args=args,
                repeat=repeat,
                raw=raw if isinstance(raw, str) else None,
            )
            steps.append(step)
            last_state_step = None
        elif event_type == "key":
            if not isinstance(payload, dict):
                continue
            sequence = payload.get("sequence")
            data = payload.get("data")
            keys: list[str] = []
            if isinstance(sequence, list):
                keys = [str(item) for item in sequence if item is not None]
            if not keys and isinstance(data, list):
                keys = [str(item) for item in data if item is not None]
            for key in keys:
                step = ReplayStep(kind="legacy_key", key=key)
                steps.append(step)
                last_state_step = None
        elif event_type == "state":
            if not steps or not isinstance(payload, dict):
                continue
            normalized = _normalize_expected_state(payload)
            steps[-1].expected_state = normalized
            last_state_step = steps[-1]
        elif event_type == "status":
            if last_state_step is None or last_state_step.expected_state is None:
                continue
            if not isinstance(payload, dict):
                continue
            text = payload.get("text")
            if isinstance(text, str):
                last_state_step.expected_state["status_message"] = text
    return steps


def _normalize_expected_state(expected: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(expected, dict):
        return {}
    if "cursor_row" in expected and "cursor_col" in expected:
        return dict(expected)
    cursor = expected.get("cursor", {})
    viewport = expected.get("viewport", {})
    normalized: dict[str, Any] = {}
    if isinstance(cursor, dict):
        normalized["cursor_row"] = cursor.get("row")
        normalized["cursor_col"] = cursor.get("col")
    if isinstance(viewport, dict):
        normalized["viewport_start_row"] = viewport.get("row0")
        normalized["viewport_start_col"] = viewport.get("col0")
    if "visible_cols" in expected:
        normalized["visible_columns"] = expected.get("visible_cols")
    elif "visible_columns" in expected:
        normalized["visible_columns"] = expected.get("visible_columns")
    if "status_message" in expected:
        normalized["status_message"] = expected.get("status_message")
    return normalized
