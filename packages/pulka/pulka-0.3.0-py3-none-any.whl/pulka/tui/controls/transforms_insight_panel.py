"""Rendering helper for the transforms insight sidecar."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from ...core.plan import FilterClause, Predicate
from ...core.predicate import render_predicate_text
from .insight_panel_base import _BODY_STYLE, InsightPanelBase, PanelLine

_STATUS_DISABLED: Literal["disabled"] = "disabled"
_STATUS_UNAVAILABLE: Literal["unavailable"] = "unavailable"
_STATUS_READY: Literal["ready"] = "ready"


class TransformsInsightPanel(InsightPanelBase):
    """Text-only panel for active filters and sorts."""

    def __init__(self, *, width: int = 32) -> None:
        super().__init__(title="Transforms", width=width)
        self._status: Literal["disabled", "unavailable", "ready"] = _STATUS_READY
        self._status_message: str = ""
        self._filters: tuple[FilterClause, ...] = ()
        self._predicates: tuple[Predicate, ...] = ()
        self._sorts: tuple[tuple[str, bool], ...] = ()
        self._identifiers: tuple[str, ...] = ()
        self._rendered_filters: tuple[str, ...] = ()
        self._rendered_predicates: tuple[str, ...] = ()
        self._rendered_sorts: tuple[str, ...] = ()

    def set_disabled(self, reason: str) -> None:
        self._status = _STATUS_DISABLED
        self._status_message = reason
        self._title = "Transforms"

    def set_unavailable(self, reason: str) -> None:
        self._status = _STATUS_UNAVAILABLE
        self._status_message = reason
        self._title = "Transforms"

    def set_transforms(
        self,
        *,
        filters: tuple[FilterClause, ...],
        predicates: tuple[Predicate, ...],
        sorts: tuple[tuple[str, bool], ...],
        identifiers: tuple[str, ...] = (),
        rendered_filters: tuple[str, ...] = (),
        rendered_predicates: tuple[str, ...] = (),
        rendered_sorts: tuple[str, ...] = (),
    ) -> None:
        self._status = _STATUS_READY
        self._status_message = ""
        self._filters = filters
        self._predicates = predicates
        self._sorts = sorts
        self._identifiers = identifiers
        self._rendered_filters = rendered_filters
        self._rendered_predicates = rendered_predicates
        self._rendered_sorts = rendered_sorts
        count = len(filters) + len(predicates) + len(sorts)
        self._title = f"Transforms ({count})" if count else "Transforms"

    def _render_body_lines(self) -> list[PanelLine]:
        status = self._status
        if status == _STATUS_DISABLED:
            return self._render_message_block(
                "Status",
                [
                    self._status_message or "Insight panel hidden.",
                    "Toggle with `i` or :insight.",
                ],
            )
        if status == _STATUS_UNAVAILABLE:
            return self._render_message_block(
                "Status",
                [self._status_message or "Insight unavailable for this view."],
            )

        lines: list[PanelLine] = []
        identifiers = iter(self._identifiers)
        lines.extend(self._render_filters_section(identifiers))
        lines.extend(self._render_sorts_section(identifiers))
        return lines

    def _render_filters_section(self, identifiers: Iterator[str]) -> list[PanelLine]:
        lines: list[PanelLine] = []
        self._append_section_title(lines, "Filters")
        if not self._filters and not self._predicates:
            lines.append(self._plain_line("—", _BODY_STYLE))
            return lines
        for idx, clause in enumerate(self._filters):
            label = next(identifiers, "")
            text = self._rendered_filters[idx] if idx < len(self._rendered_filters) else clause.text
            lines.extend(self._wrap_labeled_line(f"{label}. ", text))
        for idx, predicate in enumerate(self._predicates):
            label = next(identifiers, "")
            text = (
                self._rendered_predicates[idx]
                if idx < len(self._rendered_predicates)
                else render_predicate_text(predicate)
            )
            lines.extend(self._wrap_labeled_line(f"{label}. ", text))
        return lines

    def _render_sorts_section(self, identifiers: Iterator[str]) -> list[PanelLine]:
        lines: list[PanelLine] = []
        self._append_section_title(lines, "Sorts", pad_before=True)
        if not self._sorts:
            lines.append(self._plain_line("—", _BODY_STYLE))
            return lines
        for idx, (column, desc) in enumerate(self._sorts):
            label = next(identifiers, "")
            if idx < len(self._rendered_sorts):
                text = self._rendered_sorts[idx]
            else:
                direction = "desc" if desc else "asc"
                text = f"{column} {direction}"
            lines.extend(self._wrap_labeled_line(f"{label}. ", text))
        return lines

    def _wrap_labeled_line(self, label: str, text: str) -> list[PanelLine]:
        indent = " " * len(label)
        wrapped = self._wrap_text(
            text,
            initial_indent=label,
            subsequent_indent=indent,
        )
        return [self._plain_line(line, _BODY_STYLE) for line in wrapped]


__all__ = ["TransformsInsightPanel"]
