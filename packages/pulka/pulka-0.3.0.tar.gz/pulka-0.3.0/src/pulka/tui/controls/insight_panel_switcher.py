"""Switcher for the insight sidecar panels."""

from __future__ import annotations

from typing import Literal

from .column_insight_panel import ColumnInsightPanel
from .transforms_insight_panel import TransformsInsightPanel

InsightMode = Literal["column", "transform"]


class InsightPanelSwitcher:
    """Selects which insight panel to render in the sidecar."""

    def __init__(
        self,
        column_panel: ColumnInsightPanel,
        transforms_panel: TransformsInsightPanel,
        *,
        mode: InsightMode = "column",
    ) -> None:
        self._column_panel = column_panel
        self._transforms_panel = transforms_panel
        self._mode: InsightMode = mode
        self.width = column_panel.width

    @property
    def mode(self) -> InsightMode:
        return self._mode

    def set_mode(self, mode: InsightMode) -> None:
        if mode not in {"column", "transform"}:
            return
        self._mode = mode

    def toggle_mode(self) -> InsightMode:
        next_mode: InsightMode = "transform" if self._mode == "column" else "column"
        self._mode = next_mode
        return next_mode

    def render_text(self) -> str:
        return self._active_panel().render_text()

    def render_fragments(self):
        return self._active_panel().render_fragments()

    def render_for_recorder(self) -> str:
        return self._active_panel().render_for_recorder()

    def _active_panel(self) -> ColumnInsightPanel | TransformsInsightPanel:
        if self._mode == "transform":
            return self._transforms_panel
        return self._column_panel


__all__ = ["InsightPanelSwitcher", "InsightMode"]
