"""Sheet-enter intent helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .viewer import Viewer


@dataclass(frozen=True, slots=True)
class SheetEnterAction:
    kind: Literal["open-path", "apply-selection", "open-db-table"]
    path: Path | None = None
    open_as: Literal["dataset", "directory", "database"] | None = None
    columns: tuple[str, ...] = ()
    pop_viewer: bool = True
    db_scheme: str | None = None
    db_connection_uri: str | None = None
    db_table: str | None = None
    db_path: Path | None = None


def resolve_enter_action(viewer: Viewer) -> SheetEnterAction | None:
    sheet = getattr(viewer, "sheet", None)
    if sheet is None:
        return None

    action_fn = getattr(sheet, "enter_action", None)
    if callable(action_fn):
        try:
            action = action_fn(viewer)
        except Exception:
            return None
        if isinstance(action, SheetEnterAction):
            return action
        return None

    fallback = getattr(sheet, "action_for_row", None)
    if not callable(fallback):
        return None
    try:
        legacy_action = fallback(getattr(viewer, "cur_row", 0))
    except Exception:
        return None
    if legacy_action is None:
        return None
    action_type = getattr(legacy_action, "type", None)
    action_path = getattr(legacy_action, "path", None)
    if not action_type or action_path is None:
        return None
    try:
        path = Path(action_path)
    except Exception:
        return None
    if action_type == "enter-directory":
        return SheetEnterAction(kind="open-path", path=path, open_as="directory")
    if action_type == "open-file":
        return SheetEnterAction(kind="open-path", path=path, open_as="dataset")
    return None


__all__ = ["SheetEnterAction", "resolve_enter_action"]
