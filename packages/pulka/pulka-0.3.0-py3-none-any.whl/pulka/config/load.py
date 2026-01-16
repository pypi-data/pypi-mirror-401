"""Load Pulka configuration from ``pulka.toml`` files."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_CONFIG_FILENAMES = ("pulka.toml",)
_CONFIG_ENV_VARS = ("PULKA_CONFIG",)


@dataclass(frozen=True)
class PluginsConfig:
    """User-configurable plugin settings."""

    modules: list[str] = field(default_factory=list)
    disable: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class JobsConfig:
    """Job runner configuration exposed to :class:`pulka.api.runtime.Runtime`."""

    max_workers: int | None = None


@dataclass(frozen=True)
class StatusDurationConfig:
    """Default status message durations by severity (seconds)."""

    info: float | None = None
    warn: float | None = None
    error: float | None = None
    success: float | None = None
    debug: float | None = None


@dataclass(frozen=True)
class StatusConfig:
    """Status message configuration."""

    duration: StatusDurationConfig = StatusDurationConfig()


@dataclass(frozen=True)
class RecorderSettings:
    """User-configurable flight recorder defaults."""

    enabled: bool | None = None
    buffer_size: int | None = None
    output_dir: str | None = None
    compression: str | None = None
    compression_level: int | None = None
    auto_flush_on_exit: bool | None = None
    cell_redaction: str | None = None


@dataclass(frozen=True)
class ColumnWidthConfig:
    """Tuning values for column-width sampling heuristics."""

    sample_max_rows: int | None = None
    sample_batch_rows: int | None = None
    sample_budget_ms: float | None = None
    target_percentile: float | None = None
    padding: int | None = None


@dataclass(frozen=True)
class ViewerConfig:
    """Viewer layout and rendering defaults."""

    min_col_width: int | None = None
    default_col_width_cap_compact: int | None = None
    default_col_width_cap_wide: int | None = None
    sep_overhead: int | None = None
    hscroll_fetch_overscan_cols: int | None = None
    status_large_number_threshold: int | None = None
    column_width: ColumnWidthConfig = field(default_factory=ColumnWidthConfig)


@dataclass(frozen=True)
class TuiConfig:
    """TUI runtime settings."""

    max_steps_per_frame: int | None = None


@dataclass(frozen=True)
class DataConfig:
    """Data scan defaults."""

    csv_infer_rows: int | None = None
    browser_strict_extensions: bool | None = None


@dataclass(frozen=True)
class UserConfig:
    """Full user configuration for a session."""

    plugins: PluginsConfig = PluginsConfig()
    jobs: JobsConfig = JobsConfig()
    status: StatusConfig = StatusConfig()
    recorder: RecorderSettings = RecorderSettings()
    viewer: ViewerConfig = ViewerConfig()
    tui: TuiConfig = TuiConfig()
    data: DataConfig = DataConfig()


def _candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for env_var in _CONFIG_ENV_VARS:
        env = os.environ.get(env_var)
        if env:
            paths.append(Path(env).expanduser())
    cwd = Path.cwd()
    for name in _CONFIG_FILENAMES:
        paths.append(cwd / name)
    home = Path.home()
    for directory in (home / ".config" / "pulka",):
        for name in _CONFIG_FILENAMES:
            paths.append(directory / name)
    return paths


def _ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, (list, tuple, set)):
        result: list[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                result.append(text)
        return result
    return []


def _parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return None


def _parse_int(value: Any, *, min_value: int | None = None) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    if min_value is not None and parsed < min_value:
        return None
    return parsed


def _parse_float(value: Any, *, min_value: float | None = None) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if min_value is not None and parsed < min_value:
        return None
    return parsed


def _parse_plugins(section: Any) -> PluginsConfig:
    if not isinstance(section, dict):
        return PluginsConfig()
    modules = _ensure_list(section.get("modules"))
    disable = _ensure_list(section.get("disable"))
    return PluginsConfig(modules=modules, disable=disable)


def _parse_jobs(section: Any) -> JobsConfig:
    if not isinstance(section, dict):
        return JobsConfig()
    parsed = _parse_int(section.get("max_workers"), min_value=1)
    if parsed is None:
        return JobsConfig()
    return JobsConfig(max_workers=parsed)


def _parse_duration(value: Any) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if parsed <= 0:
        return None
    return parsed


def _parse_status(section: Any) -> StatusConfig:
    if not isinstance(section, dict):
        return StatusConfig()
    duration_section = section.get("duration")
    if not isinstance(duration_section, dict):
        return StatusConfig()
    durations = {
        "info": _parse_duration(duration_section.get("info")),
        "warn": _parse_duration(duration_section.get("warn")),
        "error": _parse_duration(duration_section.get("error")),
        "success": _parse_duration(duration_section.get("success")),
        "debug": _parse_duration(duration_section.get("debug")),
    }
    return StatusConfig(duration=StatusDurationConfig(**durations))


def _parse_recorder(section: Any) -> RecorderSettings:
    if not isinstance(section, dict):
        return RecorderSettings()
    compression = section.get("compression")
    if compression is not None:
        compression = str(compression).strip().lower()
    return RecorderSettings(
        enabled=_parse_bool(section.get("enabled")),
        buffer_size=_parse_int(section.get("buffer_size"), min_value=1),
        output_dir=str(section["output_dir"]) if section.get("output_dir") is not None else None,
        compression=compression or None,
        compression_level=_parse_int(section.get("compression_level"), min_value=1),
        auto_flush_on_exit=_parse_bool(section.get("auto_flush_on_exit")),
        cell_redaction=str(section["cell_redaction"]).strip()
        if section.get("cell_redaction") is not None
        else None,
    )


def _parse_column_width(section: Any) -> ColumnWidthConfig:
    if not isinstance(section, dict):
        return ColumnWidthConfig()
    target_percentile = _parse_float(section.get("target_percentile"), min_value=0.0)
    if target_percentile is not None and target_percentile > 1.0:
        target_percentile = None
    return ColumnWidthConfig(
        sample_max_rows=_parse_int(section.get("sample_max_rows"), min_value=1),
        sample_batch_rows=_parse_int(section.get("sample_batch_rows"), min_value=1),
        sample_budget_ms=_parse_float(section.get("sample_budget_ms"), min_value=0.0),
        target_percentile=target_percentile,
        padding=_parse_int(section.get("padding"), min_value=0),
    )


def _parse_viewer(section: Any) -> ViewerConfig:
    if not isinstance(section, dict):
        return ViewerConfig()
    column_width = _parse_column_width(section.get("column_width"))
    return ViewerConfig(
        min_col_width=_parse_int(section.get("min_col_width"), min_value=1),
        default_col_width_cap_compact=_parse_int(
            section.get("default_col_width_cap_compact"), min_value=1
        ),
        default_col_width_cap_wide=_parse_int(
            section.get("default_col_width_cap_wide"), min_value=1
        ),
        sep_overhead=_parse_int(section.get("sep_overhead"), min_value=0),
        hscroll_fetch_overscan_cols=_parse_int(
            section.get("hscroll_fetch_overscan_cols"), min_value=0
        ),
        status_large_number_threshold=_parse_int(
            section.get("status_large_number_threshold"), min_value=1
        ),
        column_width=column_width,
    )


def _parse_tui(section: Any) -> TuiConfig:
    if not isinstance(section, dict):
        return TuiConfig()
    return TuiConfig(
        max_steps_per_frame=_parse_int(section.get("max_steps_per_frame"), min_value=1)
    )


def _parse_data(section: Any) -> DataConfig:
    if not isinstance(section, dict):
        return DataConfig()
    return DataConfig(
        csv_infer_rows=_parse_int(section.get("csv_infer_rows"), min_value=1),
        browser_strict_extensions=_parse_bool(section.get("browser_strict_extensions")),
    )


def load_user_config() -> UserConfig:
    """Load ``pulka.toml`` configuration from the usual locations."""

    for path in _candidate_paths():
        if not path.exists():
            continue
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        plugins_section: Any
        if "plugins" in data and isinstance(data["plugins"], dict):
            plugins_section = data["plugins"]
        else:
            plugins_section = {key: data[key] for key in ("modules", "disable") if key in data}
        plugins = _parse_plugins(plugins_section)
        jobs = _parse_jobs(data.get("jobs"))
        status = _parse_status(data.get("status"))
        recorder = _parse_recorder(data.get("recorder"))
        viewer = _parse_viewer(data.get("viewer"))
        tui = _parse_tui(data.get("tui"))
        data_section = _parse_data(data.get("data"))
        return UserConfig(
            plugins=plugins,
            jobs=jobs,
            status=status,
            recorder=recorder,
            viewer=viewer,
            tui=tui,
            data=data_section,
        )

    return UserConfig()


__all__ = [
    "ColumnWidthConfig",
    "DataConfig",
    "JobsConfig",
    "PluginsConfig",
    "RecorderSettings",
    "StatusConfig",
    "StatusDurationConfig",
    "TuiConfig",
    "UserConfig",
    "ViewerConfig",
    "load_user_config",
]
