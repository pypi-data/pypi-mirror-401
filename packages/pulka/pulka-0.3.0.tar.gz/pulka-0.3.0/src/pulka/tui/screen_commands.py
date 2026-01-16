"""Command dispatch helpers for the TUI screen."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import nullcontext
from typing import Any

from ..command.parser import CommandDispatchResult
from ..command.registry import CommandContext
from ..command.runtime import CommandRuntimeResult


class CommandDispatcher:
    """Centralize command runtime invocation and result handling."""

    def __init__(
        self,
        *,
        screen: Any,
        runtime: Any,
        get_recorder: Callable[[], Any],
        get_viewer: Callable[[], Any],
        apply_insight_state: Callable[[], None],
        clear_column_search: Callable[[], None],
    ) -> None:
        self._screen = screen
        self._runtime = runtime
        self._get_recorder = get_recorder
        self._get_viewer = get_viewer
        self._apply_insight_state = apply_insight_state
        self._clear_column_search = clear_column_search

    def mutate_context(self, context: CommandContext) -> None:
        context.screen = self._screen
        context.ui = self._screen

    def finalise_runtime_result(self, result: CommandRuntimeResult) -> CommandDispatchResult | None:
        viewer = self._get_viewer()
        if viewer is not None and result.message:
            viewer.status_message = result.message
        dispatch = result.dispatch
        if dispatch and dispatch.spec.name == "search":
            self._clear_column_search()
        return dispatch

    def execute_command(
        self, name: str, args: list[str] | None = None, *, repeat: int = 1
    ) -> CommandDispatchResult | None:
        invocation_args = list(args or [])
        recorder = self._get_recorder()
        recorder = recorder if recorder and getattr(recorder, "enabled", False) else None
        perf_ctx = (
            recorder.perf_timer(
                "input.command",
                payload={"context": "tui", "command": name},
            )
            if recorder
            else nullcontext()
        )
        with perf_ctx:
            result = self._runtime.invoke(
                name,
                args=invocation_args,
                repeat=repeat,
                source="tui",
                context_mutator=self.mutate_context,
            )
        self._apply_insight_state()
        return self.finalise_runtime_result(result)
