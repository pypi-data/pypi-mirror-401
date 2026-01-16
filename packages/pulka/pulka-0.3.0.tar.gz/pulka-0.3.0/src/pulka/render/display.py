"""Display width helpers with grapheme-aware truncation and padding."""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from functools import lru_cache
from typing import cast

from wcwidth import wcswidth, wcwidth  # type: ignore[import-untyped]

_ZWJ = "\u200d"


@lru_cache(maxsize=2048)
def _is_variation_selector(codepoint: int) -> bool:
    return (0xFE00 <= codepoint <= 0xFE0F) or (0xE0100 <= codepoint <= 0xE01EF)


@lru_cache(maxsize=2048)
def _is_regional_indicator(codepoint: int) -> bool:
    return 0x1F1E6 <= codepoint <= 0x1F1FF


@lru_cache(maxsize=2048)
def _is_emoji_modifier(codepoint: int) -> bool:
    return 0x1F3FB <= codepoint <= 0x1F3FF


def display_width(text: str) -> int:
    """Return the terminal column width for ``text`` using wcwidth semantics."""

    if not text:
        return 0

    if text.isascii():
        for ch in text:
            code = ord(ch)
            if code < 32 or code >= 127:
                break
        else:
            return len(text)

    width = cast(int, wcswidth(text))
    if width >= 0:
        return width

    total = 0
    for ch in text:
        ch_width = wcwidth(ch)
        total += ch_width if ch_width > 0 else 0
    return total


def _trailing_regional_count(grapheme: str) -> int:
    count = 0
    for ch in reversed(grapheme):
        if _is_regional_indicator(ord(ch)):
            count += 1
        else:
            break
    return count


def _should_extend(grapheme: str, char: str) -> bool:
    if not grapheme:
        return False

    last = grapheme[-1]
    codepoint = ord(char)

    if last == _ZWJ:
        return True
    if char == _ZWJ:
        return True
    if unicodedata.combining(char):
        return True
    if _is_variation_selector(codepoint):
        return True
    if unicodedata.category(char) == "Me":
        return True
    if _is_emoji_modifier(codepoint):
        return True
    if _is_regional_indicator(codepoint):
        return _trailing_regional_count(grapheme) % 2 == 1
    return False


def iter_graphemes(text: str) -> Iterable[str]:
    grapheme = ""
    for char in text:
        if not grapheme:
            grapheme = char
            continue
        if _should_extend(grapheme, char):
            grapheme += char
        else:
            yield grapheme
            grapheme = char
    if grapheme:
        yield grapheme


def truncate_grapheme_safe(text: str, max_cols: int) -> str:
    """Truncate ``text`` to ``max_cols`` display columns without splitting graphemes."""

    if max_cols <= 0 or not text:
        return ""

    if text.isascii():
        for ch in text:
            code = ord(ch)
            if code < 32 or code >= 127:
                break
        else:
            if max_cols >= len(text):
                return text
            return text[:max_cols]

    if display_width(text) <= max_cols:
        return text

    parts: list[str] = []
    used = 0
    for grapheme in iter_graphemes(text):
        width = display_width(grapheme)
        if used + width > max_cols:
            break
        parts.append(grapheme)
        used += width
        if used >= max_cols:
            break
    return "".join(parts)


def truncate_grapheme_safe_from_end(text: str, max_cols: int) -> str:
    """Truncate ``text`` from the end to ``max_cols`` display columns.

    Avoid splitting graphemes when trimming.
    """

    if max_cols <= 0 or not text:
        return ""

    if text.isascii():
        if max_cols >= len(text):
            return text
        return text[-max_cols:]

    if display_width(text) <= max_cols:
        return text

    graphemes = list(iter_graphemes(text))
    parts: list[str] = []
    used = 0
    for grapheme in reversed(graphemes):
        width = display_width(grapheme)
        if used + width > max_cols:
            break
        parts.append(grapheme)
        used += width
        if used >= max_cols:
            break
    return "".join(reversed(parts))


def truncate_middle_grapheme_safe(
    text: str,
    max_cols: int,
    *,
    back_preference: str | None = None,
) -> str:
    """Truncate ``text`` around the middle to fit ``max_cols`` display columns."""

    if max_cols <= 0 or not text:
        return ""

    if display_width(text) <= max_cols:
        return text

    ellipsis = "…"
    ellipsis_width = display_width(ellipsis)
    if max_cols <= ellipsis_width:
        return ellipsis[:max_cols]

    available = max_cols - ellipsis_width
    if available <= 0:
        return ellipsis[:max_cols]
    if available == 1:
        if back_preference:
            tail = truncate_grapheme_safe_from_end(text, 1)
            return f"{ellipsis}{tail}"
        head = truncate_grapheme_safe(text, 1)
        return f"{head}{ellipsis}"

    min_front = 1
    max_back = max(1, available - min_front)
    back_width = max(1, available // 2)
    if back_preference:
        pref_width = display_width(back_preference)
        back_width = max(back_width, min(pref_width, max_back))
    back_width = min(max_back, back_width)
    front_width = max(1, available - back_width)

    front = truncate_grapheme_safe(text, front_width)
    back = truncate_grapheme_safe_from_end(text, back_width)
    return f"{front}{ellipsis}{back}"


def pad_right_display(text: str, width: int) -> str:
    """Pad ``text`` on the right to reach ``width`` display cells."""

    current = display_width(text)
    if current >= width:
        return text
    return text + " " * (width - current)


def pad_left_display(text: str, width: int) -> str:
    """Pad ``text`` on the left to reach ``width`` display cells."""

    current = display_width(text)
    if current >= width:
        return text
    return " " * (width - current) + text
