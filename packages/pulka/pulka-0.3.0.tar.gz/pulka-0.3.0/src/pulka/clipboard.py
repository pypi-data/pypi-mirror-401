"""Clipboard helpers for Pulka.

This module provides a small extensible abstraction for copying text to the
system clipboard. The default implementation prioritises the Windows clipboard
bridge available inside WSL (`clip.exe`) but exposes a backend protocol so other
platform specific integrations (macOS `pbcopy`, Linux utilities, etc.) can be
added without touching call sites. The :func:`copy_to_clipboard` helper iterates
through registered backends until one succeeds, keeping the implementation easy
to extend.
"""

from __future__ import annotations

import base64
import os
import platform
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol


class ClipboardBackend(Protocol):
    """Protocol implemented by clipboard backends."""

    name: str

    def is_supported(self) -> bool:
        """Return ``True`` when the backend is viable on the current system."""

    def copy(self, text: str) -> bool:
        """Attempt to copy ``text`` to the clipboard, returning success state."""


@dataclass(frozen=True, slots=True)
class _CommandClipboardBackend:
    """Run a shell command to forward text into the system clipboard."""

    name: str
    command: tuple[str, ...]
    predicate: Callable[[], bool] | None = None

    def is_supported(self) -> bool:  # pragma: no cover - trivial
        if self.predicate is None:
            return True
        return bool(self.predicate())

    def copy(self, text: str) -> bool:
        try:
            subprocess.run(self.command, input=text, text=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError, OSError):
            return False
        return True


@dataclass(frozen=True, slots=True)
class _TmuxClipboardBackend:
    """Use tmux to set the client clipboard (OSC52 via tmux)."""

    name: str = "tmux:set-buffer"

    def is_supported(self) -> bool:  # pragma: no cover - trivial
        return bool(os.environ.get("TMUX"))

    def copy(self, text: str) -> bool:
        try:
            subprocess.run(
                ("tmux", "load-buffer", "-w", "-"),
                input=text,
                text=True,
                check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError, OSError):
            return False
        return True


def _is_windows() -> bool:
    return os.name == "nt"


def _is_wsl() -> bool:
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    release = platform.release().lower()
    return "microsoft" in release or "wsl" in release


def _is_macos() -> bool:
    return platform.system().lower() == "darwin"


def _is_linux() -> bool:
    return platform.system().lower() == "linux"


def _has_x11_display() -> bool:
    return bool(os.environ.get("DISPLAY") or os.environ.get("XAUTHORITY"))


def _has_wayland_display() -> bool:
    return bool(os.environ.get("WAYLAND_DISPLAY"))


def _osc52_output():
    return getattr(sys, "__stdout__", sys.stdout)


def _supports_osc52() -> bool:
    term = os.environ.get("TERM", "")
    if term in ("", "dumb"):
        return False
    output = _osc52_output()
    if output.isatty():
        return True
    return bool(os.environ.get("TMUX") or os.environ.get("SSH_TTY"))


def _osc52_sequences(payload: str) -> tuple[str, ...]:
    sequence_bel = f"\x1b]52;c;{payload}\x07"
    sequence_st = f"\x1b]52;c;{payload}\x1b\\"

    sequences = [sequence_bel, sequence_st]

    # In tmux, applications can either let tmux handle OSC52 directly (unwrapped),
    # or use the DCS passthrough wrapper. Which one works depends on tmux options
    # (`set-clipboard`, `allow-passthrough`) and terminal quirks, so emit both.
    if "TMUX" in os.environ:
        sequences.extend(
            (
                f"\x1bPtmux;\x1b{sequence_bel}\x1b\\",
                f"\x1bPtmux;\x1b{sequence_st}\x1b\\",
            )
        )
    elif os.environ.get("TERM", "").startswith("screen"):
        sequences.extend((f"\x1bP{sequence_bel}\x1b\\", f"\x1bP{sequence_st}\x1b\\"))

    return tuple(sequences)


@dataclass(frozen=True, slots=True)
class _Osc52ClipboardBackend:
    """Use the OSC52 escape sequence to copy text via the terminal."""

    name: str = "osc52"

    def is_supported(self) -> bool:  # pragma: no cover - trivial
        return _supports_osc52()

    def _write_payload(self, payload: str) -> bool:
        output = _osc52_output()
        try:
            for sequence in _osc52_sequences(payload):
                output.write(sequence)
            output.flush()
        except OSError:
            return False
        return True

    def copy(self, text: str) -> bool:
        payload = base64.b64encode(text.encode("utf-8", "replace")).decode("ascii")
        return self._write_payload(payload)


def _supports_clip_exe() -> bool:
    return _is_windows() or _is_wsl()


_DEFAULT_BACKENDS: tuple[ClipboardBackend, ...] = (
    _CommandClipboardBackend("clip.exe", ("clip.exe",), predicate=_supports_clip_exe),
    _CommandClipboardBackend("clip", ("clip",), predicate=_is_windows),
    _CommandClipboardBackend("pbcopy", ("pbcopy",), predicate=_is_macos),
    _CommandClipboardBackend(
        "wl-copy", ("wl-copy",), predicate=lambda: _is_linux() and _has_wayland_display()
    ),
    _CommandClipboardBackend(
        "xclip",
        ("xclip", "-selection", "clipboard"),
        predicate=lambda: _is_linux() and _has_x11_display(),
    ),
    _CommandClipboardBackend(
        "xsel",
        ("xsel", "--clipboard", "--input"),
        predicate=lambda: _is_linux() and _has_x11_display(),
    ),
    _TmuxClipboardBackend(),
    _Osc52ClipboardBackend(),
)


def copy_to_clipboard(
    text: str,
    *,
    backends: Sequence[ClipboardBackend] | None = None,
    max_osc52_bytes: int | None = None,
) -> bool:
    """Copy ``text`` to the clipboard using the first working backend.

    Args:
        text: The text payload to copy. Non-string input is coerced using ``str``.
        backends: Optional explicit backend list. When omitted, the module's
            default backends are used.
        max_osc52_bytes: When set, skip OSC52 for payloads larger than this
            byte count.

    Returns:
        ``True`` when a backend reported success, ``False`` otherwise.
    """

    payload = text if isinstance(text, str) else str(text)
    candidates = backends or _DEFAULT_BACKENDS
    payload_bytes = len(payload.encode("utf-8", "replace"))

    for backend in candidates:
        try:
            if not backend.is_supported():
                continue
        except Exception:
            continue

        try:
            if (
                isinstance(backend, _Osc52ClipboardBackend)
                and max_osc52_bytes is not None
                and payload_bytes > max_osc52_bytes
            ):
                continue
            if backend.copy(payload):
                return True
        except Exception:
            continue

    return False
