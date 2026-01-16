"""Shared rendering helpers for insight sidecar panels."""

from __future__ import annotations

import textwrap
from typing import Protocol

from prompt_toolkit.formatted_text import StyleAndTextTuples

PanelLine = list[tuple[str, str]]
_HEADER_STYLE = "class:table.header"
_BODY_STYLE = "class:table.cell"


class _InsightPanelBody(Protocol):
    width: int

    def _render_body_lines(self) -> list[PanelLine]: ...


class InsightPanelBase:
    """Base renderer for a right-hand insight panel."""

    def __init__(self, *, title: str, width: int = 32) -> None:
        self.width = max(20, width)
        self._title = title

    def render_text(self) -> str:
        """Return the textual presentation rendered in the TUI."""

        return "\n".join(self._line_text(line) for line in self._render_lines())

    def render_fragments(self) -> StyleAndTextTuples:
        """Return prompt_toolkit fragments with table-themed styling."""

        lines = self._render_lines()
        if not lines:
            return [("", "")]

        fragments: StyleAndTextTuples = []
        for idx, line in enumerate(lines):
            for style, text in line:
                fragments.append((style, text))
            if idx < len(lines) - 1:
                fragments.append(("", "\n"))
        return fragments

    def render_for_recorder(self) -> str:
        """Return snapshot text appended to recorder frames."""

        body = self.render_text()
        if not body:
            return ""
        border_prefix = "│ "
        bordered_lines = [f"{border_prefix}{line}" for line in body.splitlines()]
        return "\n".join(bordered_lines)

    def _render_lines(self: _InsightPanelBody) -> list[PanelLine]:
        body = self._render_body_lines()
        lines: list[PanelLine] = [
            self._plain_line("", _BODY_STYLE),
            self._plain_line(self._title, _HEADER_STYLE),
        ]
        if body:
            lines.append(self._plain_line("", _BODY_STYLE))
            lines.extend(body)
        return lines

    def _render_body_lines(self) -> list[PanelLine]:
        raise NotImplementedError

    def _wrap_text(
        self,
        text: str,
        *,
        initial_indent: str = "",
        subsequent_indent: str | None = None,
    ) -> list[str]:
        indent = initial_indent if subsequent_indent is None else subsequent_indent
        if self.width <= 0:
            return [""]
        wrapped = textwrap.wrap(
            text,
            width=self.width,
            initial_indent=initial_indent,
            subsequent_indent=indent,
            replace_whitespace=False,
            drop_whitespace=False,
        )
        if wrapped:
            return wrapped
        if initial_indent:
            return [initial_indent.rstrip()]
        return [""]

    def _render_message_block(self, title: str, messages: list[str]) -> list[PanelLine]:
        lines: list[PanelLine] = []
        self._append_section_title(lines, title)
        for message in messages:
            wrapped = textwrap.fill(message, width=self.width)
            payload = wrapped.splitlines() or [""]
            for line in payload:
                lines.append(self._plain_line(line, _BODY_STYLE))
        return lines

    def _append_section_title(
        self,
        lines: list[PanelLine],
        title: str,
        *,
        pad_before: bool = False,
    ) -> None:
        if pad_before:
            if not lines or self._line_text(lines[-1]) != "":
                lines.append(self._plain_line("", _BODY_STYLE))
        elif lines and self._line_text(lines[-1]) != "":
            lines.append(self._plain_line("", _BODY_STYLE))
        lines.append(self._plain_line(title, _HEADER_STYLE))
        lines.append(self._plain_line("", _BODY_STYLE))

    def _plain_line(self, text: str, style: str = _BODY_STYLE) -> PanelLine:
        return self._line_from_segments([(style, text)])

    def _line_from_segments(self, segments: list[tuple[str, str]]) -> PanelLine:
        limit = max(0, self.width)
        if limit == 0:
            return []
        remaining = limit
        line: PanelLine = []
        for style, text in segments:
            if not text:
                continue
            if remaining <= 0:
                break
            chunk = text[:remaining]
            if chunk:
                line.append((style, chunk))
                remaining -= len(chunk)
        if not line:
            base_style = segments[0][0] if segments else _BODY_STYLE
            line.append((base_style, ""))
        return line

    def _line_text(self, line: PanelLine) -> str:
        return "".join(part for _, part in line)

    def _clip_text(self, text: str, limit: int | None = None) -> str:
        if limit is None:
            limit = self.width
        if limit <= 0:
            return ""
        if len(text) <= limit:
            return text
        if limit == 1:
            return "…"
        return text[: limit - 1] + "…"


__all__ = ["InsightPanelBase", "PanelLine", "_BODY_STYLE", "_HEADER_STYLE"]
