"""Shared utilities for Pulka."""

from __future__ import annotations

import os
import sys
import time
from contextlib import contextmanager

__all__ = ["_get_int_env", "_boot_trace", "_boot_trace_silenced"]

_BOOT_TRACE_ENABLED = None
_BOOT_TRACE_START = time.monotonic()


def _get_int_env(primary: str, legacy: str | None, default: int) -> int:
    """Return an integer environment variable with optional legacy fallback."""

    keys = [primary]
    if legacy:
        keys.append(legacy)
    for key in keys:
        value = os.environ.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except ValueError:
            continue
    return default


def _boot_trace(message: str) -> None:
    """Emit timestamped boot trace lines when enabled via env."""

    global _BOOT_TRACE_ENABLED
    if _BOOT_TRACE_ENABLED is None:
        _BOOT_TRACE_ENABLED = _get_int_env("PULKA_BOOT_TRACE", None, 1) != 0
    if not _BOOT_TRACE_ENABLED:
        return
    elapsed_ms = int((time.monotonic() - _BOOT_TRACE_START) * 1000)
    print(f"[boot +{elapsed_ms:>6}ms] {message}", file=sys.stderr)


@contextmanager
def _boot_trace_silenced():
    """Temporarily disable boot trace output."""

    global _BOOT_TRACE_ENABLED
    previous = _BOOT_TRACE_ENABLED
    _BOOT_TRACE_ENABLED = False
    try:
        yield
    finally:
        _BOOT_TRACE_ENABLED = previous
