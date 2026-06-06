from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FormatResult:
    text: str
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ItemDefinition:
    item_type: str
    name: str
    label: str | None
    icon: str | None
    groups: str | None
    tags: str | None
    comments: tuple[str, ...]
    config: str | None
    trailing_comments: tuple[str, ...]
    original: str
