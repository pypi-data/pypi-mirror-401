from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .utils import lazy_imports

Style = lazy_imports.prompt_toolkit_style_class()

_CONFIG_FILENAMES = (
    "pulka-theme.toml",
    "pulka_theme.toml",
)
_THEME_ENV_VARS = ("PULKA_THEME_PATH",)

_THEME_EPOCH = 0


@dataclass(frozen=True)
class ThemeConfig:
    primary: str
    secondary: str

    def prompt_toolkit_style(self) -> Style:
        from .render.style_resolver import StyleResolver

        resolver = StyleResolver.from_theme(self)
        mapping = resolver.prompt_toolkit_rules()
        return Style.from_dict(mapping) if mapping else Style([])


DEFAULTS: dict[str, str] = {
    "primary": "#f06595",
    "secondary": "#63e6be",
}


def _normalize(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"default", "none", "null"}:
        return None
    return text


def _candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for env_var in _THEME_ENV_VARS:
        env = os.environ.get(env_var)
        if env:
            paths.append(Path(env).expanduser())
    cwd = Path.cwd()
    for name in _CONFIG_FILENAMES:
        paths.append(cwd / name)
    home = Path.home()
    for config_dir in (home / ".config" / "pulka",):
        for name in _CONFIG_FILENAMES:
            paths.append(config_dir / name)
    return paths


def load_theme_document() -> tuple[dict[str, Any], Path | None]:
    """Return the raw parsed theme document and the path it originated from."""

    for path in _candidate_paths():
        if not path.exists():
            continue
        try:
            data = tomllib.loads(path.read_text())
        except Exception:
            continue
        if isinstance(data, dict):
            return data, path
    return {}, None


def _load_overrides() -> dict[str, str]:
    document, _ = load_theme_document()
    section: dict[str, Any] | None = None
    if document:
        maybe_section = document.get("theme") if isinstance(document, dict) else None
        if isinstance(maybe_section, dict):
            section = maybe_section
        elif isinstance(document, dict):
            section = document
    if not section:
        return {}
    return {
        key: str(value) for key, value in section.items() if key in DEFAULTS and value is not None
    }


def load_theme() -> ThemeConfig:
    merged = DEFAULTS.copy()
    overrides = _load_overrides()
    merged.update(overrides)
    normalized: dict[str, str] = {}
    for key, value in merged.items():
        normalized_value = _normalize(value)
        normalized[key] = normalized_value or DEFAULTS[key]
    return ThemeConfig(**normalized)


def _apply_theme(config: ThemeConfig) -> None:
    global THEME, APP_STYLE, _THEME_EPOCH

    THEME = config
    APP_STYLE = THEME.prompt_toolkit_style()
    _THEME_EPOCH += 1


def theme_epoch() -> int:
    """Return the current theme epoch counter."""

    return _THEME_EPOCH


def reload_theme() -> None:
    """Reload theme configuration from disk and bump the epoch."""

    _apply_theme(load_theme())


def set_theme(config: ThemeConfig) -> None:
    """Apply ``config`` as the active theme and bump the epoch."""

    _apply_theme(config)


_apply_theme(load_theme())
