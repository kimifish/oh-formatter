from __future__ import annotations

from dataclasses import replace

from .model import FormatResult, ItemDefinition
from .scanner import bracket_delta, find_matching, find_top_level_char, split_top_level_commas, strip_balanced


ITEM_TYPE_PREFIXES = {
    "Switch",
    "Dimmer",
    "Color",
    "String",
    "Number",
    "DateTime",
    "Contact",
    "Rollershutter",
    "Player",
    "Image",
    "Location",
    "Call",
    "Group",
}

VIM_MODELINE = "// vim: set fdm=indent:noai:ts=4:sw=4:et:"


class ItemsFormatter:
    def format_text(self, text: str) -> FormatResult:
        had_final_newline = text.endswith("\n")
        lines = text.splitlines()
        output: list[str] = []
        warnings: list[str] = []
        index = 0

        while index < len(lines):
            line = lines[index]
            stripped = line.strip()
            if not stripped or _is_comment_start(stripped):
                output.append(line)
                index += 1
                continue
            if not looks_like_item_start(line):
                output.append(line)
                warnings.append(f"line {index + 1}: unknown line left unchanged")
                index += 1
                continue

            block, next_index = _collect_item_block(lines, index)
            original = "\n".join(block)
            try:
                item = parse_item(original)
                output.extend(format_item(item).splitlines())
            except ValueError as error:
                output.extend(block)
                warnings.append(f"line {index + 1}: {error}; block left unchanged")
            index = next_index

        formatted = "\n".join(output)
        if had_final_newline:
            formatted += "\n"
        return FormatResult(_ensure_vim_modeline(formatted), warnings)


def looks_like_item_start(line: str) -> bool:
    stripped = line.lstrip()
    if not stripped or _is_comment_start(stripped):
        return False
    first = stripped.split(maxsplit=1)[0]
    prefix = first.split(":", 1)[0]
    return prefix in ITEM_TYPE_PREFIXES


def _ensure_vim_modeline(text: str) -> str:
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if lines and lines[-1].lstrip().startswith("// vim:"):
        lines.pop()
    return "\n".join([*lines, VIM_MODELINE]) + "\n"


def parse_item(text: str) -> ItemDefinition:
    normalized = " ".join(part.strip() for part in text.splitlines() if part.strip())
    if not normalized:
        raise ValueError("empty item")

    config = None
    trailing_comments: tuple[str, ...] = ()
    header = normalized
    config_start = find_top_level_char(normalized, "{")
    if config_start is not None:
        config_end = find_matching(normalized, config_start, "{", "}")
        if config_end is None:
            raise ValueError("unclosed config block")
        tail = normalized[config_end + 1 :].strip()
        if tail.startswith("//") or tail.startswith("/*"):
            trailing_comments = (tail,)
        elif tail:
            raise ValueError("unexpected text after config block")
        header = normalized[:config_start].strip()
        config = normalized[config_start : config_end + 1]

    item_type, rest = _read_head_token(header)
    name, rest = _read_plain_token(rest.strip())
    if not item_type or not name:
        raise ValueError("cannot parse item type and name")

    item = ItemDefinition(item_type, name, None, None, None, None, (), config, trailing_comments, text)
    rest = rest.strip()
    while rest:
        if rest[0] in {'"', "'"}:
            token, rest = _read_balanced_quote(rest)
            item = replace(item, label=token)
        elif rest[0] == "<":
            token, rest = _read_balanced_delimited(rest, "<", ">")
            item = replace(item, icon=token)
        elif rest[0] == "(":
            token, rest = _read_balanced_delimited(rest, "(", ")")
            item = replace(item, groups=token)
        elif rest[0] == "[":
            token, rest = _read_balanced_delimited(rest, "[", "]")
            item = replace(item, tags=token)
        elif rest.startswith("/*"):
            token, rest = _read_block_comment(rest)
            item = replace(item, comments=(*item.comments, token))
        elif rest.startswith("//"):
            item = replace(item, comments=(*item.comments, rest))
            rest = ""
        else:
            raise ValueError(f"unexpected item part: {rest[:24]}")
        rest = rest.strip()

    return item


def format_item(item: ItemDefinition) -> str:
    lines = [f"{item.item_type} {item.name}"]
    for part in (item.label, item.icon, item.groups, item.tags, *item.comments):
        if part:
            lines.append(f"    {part}")
    if item.config:
        lines.extend(format_config_block(item.config).splitlines())
    for comment in item.trailing_comments:
        lines.append(f"    {comment}")
    return "\n".join(lines)


def format_config_block(config: str) -> str:
    inner = strip_balanced(config, "{", "}")
    if inner is None:
        raise ValueError("invalid config block")
    entries = split_top_level_commas(inner)
    if not entries:
        return "    {\n    }"

    lines = ["    {"]
    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1
        is_metadata = _metadata_bracket_index(entry) is not None
        if is_metadata and lines[-1] not in {"    {", ""}:
            lines.append("")
        lines.extend(_format_config_entry(entry, trailing_comma=not is_last))
        if is_metadata and not is_last:
            lines.append("")
    lines.append("    }")
    return "\n".join(lines)


def _format_config_entry(entry: str, trailing_comma: bool) -> list[str]:
    bracket_index = _metadata_bracket_index(entry)
    suffix = "," if trailing_comma else ""
    if bracket_index is None:
        return [f"        {entry.strip().rstrip(',')}{suffix}"]

    prefix = entry[:bracket_index].strip()
    bracket = entry[bracket_index:].strip().rstrip(",")
    inner = strip_balanced(bracket, "[", "]")
    if inner is None:
        return [f"        {entry.strip().rstrip(',')}{suffix}"]

    lines = [f"        {prefix} ["]
    parts = split_top_level_commas(inner)
    for index, part in enumerate(parts):
        part_suffix = "," if index < len(parts) - 1 else ""
        lines.append(f"            {part}{part_suffix}")
    lines.append(f"        ]{suffix}")
    return lines


def _metadata_bracket_index(entry: str) -> int | None:
    equals = find_top_level_char(entry, "=")
    bracket = find_top_level_char(entry, "[")
    if equals is None or bracket is None:
        return None
    return bracket if equals < bracket else None


def _collect_item_block(lines: list[str], start: int) -> tuple[list[str], int]:
    block = [lines[start]]
    round_depth, square_depth, curly_depth, angle_depth = bracket_delta(lines[start])
    index = start + 1
    saw_curly = "{" in lines[start]

    if saw_curly and round_depth <= 0 and square_depth <= 0 and curly_depth <= 0 and angle_depth <= 0:
        return block, index

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        is_top_level_comment = _is_comment_start(stripped) and line == line.lstrip()
        if not saw_curly and (not stripped or is_top_level_comment or looks_like_item_start(line)):
            break

        block.append(line)
        delta = bracket_delta(line)
        round_depth += delta[0]
        square_depth += delta[1]
        curly_depth += delta[2]
        angle_depth += delta[3]
        saw_curly = saw_curly or "{" in line
        index += 1

        if saw_curly and round_depth <= 0 and square_depth <= 0 and curly_depth <= 0 and angle_depth <= 0:
            break

    return block, index


def _read_head_token(text: str) -> tuple[str, str]:
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char.isspace() and depth == 0:
            return text[:index], text[index + 1 :]
    return text, ""


def _read_plain_token(text: str) -> tuple[str, str]:
    if not text:
        return "", ""
    parts = text.split(maxsplit=1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


def _read_balanced_quote(text: str) -> tuple[str, str]:
    quote = text[0]
    escape = False
    for index in range(1, len(text)):
        char = text[index]
        if escape:
            escape = False
        elif char == "\\":
            escape = True
        elif char == quote:
            return text[: index + 1], text[index + 1 :]
    raise ValueError("unclosed quoted string")


def _read_balanced_delimited(text: str, opener: str, closer: str) -> tuple[str, str]:
    end = find_matching(text, 0, opener, closer)
    if end is None:
        raise ValueError(f"unclosed {opener}{closer} block")
    return text[: end + 1], text[end + 1 :]


def _read_block_comment(text: str) -> tuple[str, str]:
    end = text.find("*/", 2)
    if end == -1:
        raise ValueError("unclosed block comment")
    return text[: end + 2], text[end + 2 :]


def _is_comment_start(stripped: str) -> bool:
    return stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*")
