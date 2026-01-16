"""
Test command parity between TUI and headless modes.

This module ensures that all TUI keybindings have corresponding headless commands
and that they use the same command registry.
"""

import re
from pathlib import Path

import pytest

from pulka.command.registry import REGISTRY


def extract_tui_keybindings():
    """Extract all keybinding command names from TUI screen.py."""
    screen_py = Path("src/pulka/tui/screen.py").read_text(encoding="utf-8")

    # Find all _execute_command calls
    execute_command_pattern = r'self\._execute_command\(["\']([^"\']+)["\']'
    registry_execute_pattern = r'REGISTRY\.execute\(["\']([^"\']+)["\']'

    commands = set()

    # Extract from _execute_command calls
    for match in re.finditer(execute_command_pattern, screen_py):
        commands.add(match.group(1))

    # Extract from direct REGISTRY.execute calls (legacy)
    for match in re.finditer(registry_execute_pattern, screen_py):
        commands.add(match.group(1))

    return commands


def extract_headless_commands():
    """Extract all commands supported by headless runner."""
    # Since headless now uses registry exclusively, all registry commands are available
    registry_commands = {cmd[0] for cmd in REGISTRY.list_commands()}

    # Add special headless-only commands
    headless_special = {"quit", "exit", "q", "help", "render", "print"}

    return registry_commands | headless_special


def test_all_tui_commands_available_in_headless():
    """Ensure every TUI command is available in headless mode."""
    tui_commands = extract_tui_keybindings()
    headless_commands = extract_headless_commands()
    registry_commands = {cmd[0] for cmd in REGISTRY.list_commands()}

    # All TUI commands should either be in registry or be special cases
    missing_commands = tui_commands - headless_commands - registry_commands

    if missing_commands:
        pytest.fail(
            f"TUI commands not available in headless mode: {missing_commands}\n"
            f"TUI commands: {sorted(tui_commands)}\n"
            f"Headless commands: {sorted(headless_commands)}\n"
            f"Registry commands: {sorted(registry_commands)}"
        )


def test_registry_has_core_commands():
    """Ensure registry contains all expected core commands."""
    registry_commands = {cmd[0] for cmd in REGISTRY.list_commands()}

    expected_commands = {
        # Movement
        "move_down",
        "move_up",
        "move_left",
        "move_right",
        "move_page_down",
        "move_page_up",
        "move_top",
        "move_bottom",
        "move_first_column",
        "move_last_column",
        "move_column_first_overall",
        "move_column_last_overall",
        # Data operations
        "sort_asc",
        "sort_asc_stack",
        "sort_desc",
        "sort_desc_stack",
        "filter_expr",
        "filter_value",
        "filter_value_not",
        "filter_sql",
        "reset",
        "reset_expr_filter",
        "reset_sql_filter",
        "reset_sort",
        "move_to_column",
        # Column operations
        "drop",
        "reset_drop",
        "select_row",
        "select_same_value",
        "select_contains",
        "undo",
        "redo",
        "maximize_column",
        "maximize_all_columns",
        "schema",
        "transform_expr",
        # Search
        "search",
        "search_next_match",
        "search_prev_match",
        "search_value_next",
        "search_value_prev",
        # Navigation
        "move_center_row",
        "move_next_different_value",
        "move_prev_different_value",
        # Utility
        "render",
        "repro_export",
        "help_sheet",
        "frequency_sheet",
    }

    missing_commands = expected_commands - registry_commands

    if missing_commands:
        pytest.fail(
            f"Registry missing expected commands: {missing_commands}\n"
            f"Available commands: {sorted(registry_commands)}"
        )


def test_command_aliases_work():
    """Test that common aliases are properly registered."""
    aliases_to_test = [
        ("?", "help_sheet"),
        ("/", "search"),
        ("\\", "filter_contains"),
        ("_", "maximize_column"),
        ("h", "move_left"),
        ("j", "move_down"),
        ("k", "move_up"),
        ("l", "move_right"),
        ("[", "sort_desc"),
        ("]", "sort_asc"),
        ("{", "sort_desc_stack"),
        ("}", "sort_asc_stack"),
        ("e", "filter_expr"),
        ("f", "filter_sql"),
        ("c", "move_to_column"),
        ("E", "transform_expr"),
        ("F", "frequency_sheet"),
        ("u", "undo"),
        ("U", "redo"),
        ("g_", "maximize_all_columns"),
        ("gg", "move_top"),
        ("G", "move_bottom"),
        ("0", "move_first_column"),
        ("$", "move_last_column"),
        ("-", "filter_value_not"),
        ("d", "drop"),
        ("rd", "reset_drop"),
        ("yy", "yank_cell"),
        ("yp", "yank_path"),
        ("yc", "yank_column"),
        ("yac", "yank_all_columns"),
        ("ys", "yank_schema"),
        (",", "select_same_value"),
        ("|", "select_contains"),
        ("+", "filter_value"),
        ("*", "search_value_next"),
        ("#", "search_value_prev"),
        ("w", "write"),
    ]

    for alias, expected_command in aliases_to_test:
        cmd = REGISTRY.get_command(alias)
        if cmd is None:
            pytest.fail(f"Alias '{alias}' not found in registry")

        # The command name should be the canonical name, not the alias
        assert cmd.name == expected_command, (
            f"Alias '{alias}' should resolve to '{expected_command}', got '{cmd.name}'"
        )


def test_no_direct_viewer_calls_in_tui():
    """Ensure TUI keybindings use registry instead of direct viewer calls."""
    screen_py = Path("src/pulka/tui/screen.py").read_text(encoding="utf-8")

    # Look for patterns that suggest direct viewer method calls in keybindings
    # We'll look for specific patterns that indicate bypassing the registry
    forbidden_patterns = [
        r"self\.viewer\.toggle_sort\(",  # Direct sort calls should use registry
        r"self\.viewer\.go_\w+\(\)",  # Direct navigation calls should use registry
    ]

    violations = []
    for pattern in forbidden_patterns:
        matches = list(re.finditer(pattern, screen_py))
        if matches:
            for match in matches:
                # Get line number for better error reporting
                line_start = screen_py.rfind("\n", 0, match.start()) + 1
                line_num = screen_py.count("\n", 0, line_start) + 1

                # Skip if this is in _apply_pending_moves which is legitimate
                context_start = max(0, line_start - 100)
                context = screen_py[context_start : match.end() + 100]
                if "_apply_pending_moves" in context:
                    continue

                violations.append(f"Line {line_num}: {match.group(0)}")

    if violations:
        pytest.fail(
            "TUI contains direct viewer calls that should use registry:\n" + "\n".join(violations)
        )


def test_headless_runner_uses_registry():
    """Ensure headless runner uses registry for command execution."""
    runner_py = Path("src/pulka/headless/runner.py").read_text(encoding="utf-8")

    # Check that apply_script_command delegates to the session runtime
    assert "session.command_runtime" in runner_py, (
        "Headless runner should use the session-bound command runtime"
    )
    assert "dispatch_raw" in runner_py, (
        "Headless runner should dispatch raw commands through the runtime"
    )
    assert "REGISTRY.bind" not in runner_py, "Headless runner should not bind the global registry"

    # Check that we removed the massive hardcoded command switch
    # The old version had many lines like 'if cmd in {"move_down", "j"}'
    hardcoded_patterns = [
        r'if cmd in \{["\']move_down["\']',
        r'if cmd in \{["\']move_up["\']',
    ]

    for pattern in hardcoded_patterns:
        if re.search(pattern, runner_py):
            pytest.fail(f"Found hardcoded command pattern in runner: {pattern}")


if __name__ == "__main__":
    # Run tests manually for debugging
    print("TUI commands:", sorted(extract_tui_keybindings()))
    print("Headless commands:", sorted(extract_headless_commands()))
    print("Registry commands:", sorted({cmd[0] for cmd in REGISTRY.list_commands()}))
