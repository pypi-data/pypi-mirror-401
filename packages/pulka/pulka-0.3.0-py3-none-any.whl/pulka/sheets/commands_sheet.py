"""Sheet implementation exposing available runtime commands."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import ClassVar

import polars as pl

from ..command.registry import CommandRegistry
from ..core.interfaces import JobRunnerProtocol
from ..core.plan import QueryPlan
from ..core.sheet import Sheet
from .data_sheet import DataSheet


@dataclass(frozen=True, slots=True)
class CommandsHelpEntry:
    """Declarative help entry rendered in the commands sheet."""

    domain: str
    command: str
    aliases: str = ""
    args: str = "none"
    repeatable: bool = False
    provider: str = "tui"
    description: str = ""
    example: str = ""


def key_only_entry(key: str, action: str, *, description: str | None = None) -> CommandsHelpEntry:
    """Return a commands sheet entry for a key-only action."""

    return CommandsHelpEntry(
        domain="Contextual",
        command=action,
        aliases=key,
        args="none",
        repeatable=False,
        provider="tui",
        description=description if description is not None else action,
        example="",
    )


class CommandsSheet(DataSheet):
    """Read-only sheet listing the registered runtime commands."""

    _COLUMNS: ClassVar[tuple[str, ...]] = (
        "domain",
        "command",
        "aliases",
        "args",
        "repeatable",
        "provider",
        "description",
        "example",
    )
    _SCHEMA: ClassVar[dict[str, pl.DataType]] = {
        "domain": pl.Utf8,
        "command": pl.Utf8,
        "aliases": pl.Utf8,
        "args": pl.Utf8,
        "repeatable": pl.Boolean,
        "provider": pl.Utf8,
        "description": pl.Utf8,
        "example": pl.Utf8,
    }

    def __init__(
        self,
        base_sheet: Sheet,
        *,
        commands: CommandRegistry,
        help_entries: Sequence[CommandsHelpEntry] | None = None,
        runner: JobRunnerProtocol,
    ) -> None:
        self.base_sheet = base_sheet
        self.is_insight_soft_disabled = True
        df = self._build_dataframe(commands, help_entries=help_entries)
        super().__init__(df.lazy(), columns=list(self._COLUMNS), runner=runner)
        self.source_sheet = self

    def _build_dataframe(
        self,
        commands: CommandRegistry,
        *,
        help_entries: Sequence[CommandsHelpEntry] | None = None,
    ) -> pl.DataFrame:
        records: list[dict[str, object]] = []
        for spec in commands.iter_specs():
            domain = (getattr(spec, "domain", None) or "Other").strip() or "Other"
            if domain == "Other" and getattr(spec, "provider", "core") not in {"core", "builtin"}:
                domain = "Plugin"

            description = (getattr(spec, "description", "") or "").strip()
            if not description:
                doc = getattr(getattr(spec, "handler", None), "__doc__", None)
                if isinstance(doc, str):
                    description = (doc.strip().splitlines() or [""])[0].strip()

            hints = getattr(spec, "ui_hints", None) or {}
            if isinstance(hints, Mapping) and hints.get("hidden"):
                continue

            aliases = tuple(dict.fromkeys(getattr(spec, "aliases", ()) or ()))
            alias_text = ", ".join(
                _format_alias(alias, command_only=alias in _COMMAND_ONLY_ALIASES)
                for alias in aliases
            )
            example: str = ""
            if isinstance(hints, Mapping):
                raw = hints.get("example")
                if raw is not None:
                    example = str(raw)

            records.append(
                {
                    "domain": domain,
                    "command": spec.name,
                    "aliases": alias_text,
                    "args": spec.argument_mode,
                    "repeatable": bool(spec.repeatable),
                    "provider": getattr(spec, "provider", "core"),
                    "description": description,
                    "example": example,
                }
            )

        for entry in help_entries or ():
            records.append(
                {
                    "domain": entry.domain,
                    "command": entry.command,
                    "aliases": entry.aliases,
                    "args": entry.args,
                    "repeatable": bool(entry.repeatable),
                    "provider": entry.provider,
                    "description": entry.description,
                    "example": entry.example,
                }
            )

        records.sort(
            key=lambda row: (str(row["domain"]).casefold(), str(row["command"]).casefold())
        )
        if not records:
            return pl.DataFrame(
                {col: pl.Series(col, [], dtype=self._SCHEMA[col]) for col in self._COLUMNS}
            )
        return pl.DataFrame(records, schema=self._SCHEMA)

    def with_plan(self, plan: QueryPlan) -> CommandsSheet:
        if plan == self.plan:
            return self
        sheet = self.__class__.__new__(self.__class__)
        DataSheet.__init__(
            sheet,
            self._physical_source_handle,
            plan=plan,
            schema=self.schema,
            columns=self.columns,
            sheet_id=self.sheet_id,
            generation=self._runner.bump_generation(self.sheet_id),
            compiler=self._compiler,
            materializer=self._materializer,
            runner=self._runner,
        )
        sheet.base_sheet = self.base_sheet
        sheet.is_insight_soft_disabled = True
        sheet.source_sheet = sheet
        return sheet


_COMMAND_ONLY_ALIASES = {
    "b",
    "browser",
    "browse",
    "cp",
    "help",
    "commands",
    "pal",
    "print",
    "rd",
    "repro",
    "w",
    "columns",
    "summary",
    "freq",
    "transpose",
    "transpose_row",
    "mv",
}


def _format_alias(alias: str, *, command_only: bool) -> str:
    if alias in {"page_down", "page_up", "pagedown", "pageup"}:
        rendered = f"<{alias}>"
    elif any(char.isspace() for char in alias):
        rendered = "".join("<space>" if char.isspace() else char for char in alias)
    else:
        rendered = alias
    return f":{rendered}" if command_only else rendered
