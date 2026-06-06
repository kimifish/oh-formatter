from __future__ import annotations


PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}


def split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    state = _ScanState()

    for index, char in enumerate(text):
        state.feed(text, index)
        if char == "," and state.is_top_level:
            part = text[start:index].strip()
            if part:
                parts.append(part)
            start = index + 1

    tail = text[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def strip_balanced(text: str, opener: str, closer: str) -> str | None:
    stripped = text.strip()
    if not stripped.startswith(opener) or not stripped.endswith(closer):
        return None
    end = find_matching(stripped, 0, opener, closer)
    if end != len(stripped) - 1:
        return None
    return stripped[1:-1].strip()


def find_matching(text: str, start: int, opener: str, closer: str) -> int | None:
    state = _ScanState()
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        state.feed(text, index)
        if state.in_quote or state.in_comment:
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return index
    return None


def find_top_level_char(text: str, target: str) -> int | None:
    state = _ScanState()
    for index, char in enumerate(text):
        is_top_level = state.is_top_level
        state.feed(text, index)
        if char == target and is_top_level:
            return index
    return None


def bracket_delta(text: str) -> tuple[int, int, int, int]:
    state = _ScanState()
    round_depth = square_depth = curly_depth = angle_depth = 0
    for index, char in enumerate(text):
        state.feed(text, index)
        if state.in_quote or state.in_comment:
            continue
        if char == "(":
            round_depth += 1
        elif char == ")":
            round_depth -= 1
        elif char == "[":
            square_depth += 1
        elif char == "]":
            square_depth -= 1
        elif char == "{":
            curly_depth += 1
        elif char == "}":
            curly_depth -= 1
        elif char == "<":
            angle_depth += 1
        elif char == ">":
            angle_depth -= 1
    return round_depth, square_depth, curly_depth, angle_depth


class _ScanState:
    def __init__(self) -> None:
        self.quote: str | None = None
        self.escape = False
        self.line_comment = False
        self.block_comment = False
        self.round_depth = 0
        self.square_depth = 0
        self.curly_depth = 0
        self.angle_depth = 0

    @property
    def in_quote(self) -> bool:
        return self.quote is not None

    @property
    def in_comment(self) -> bool:
        return self.line_comment or self.block_comment

    @property
    def is_top_level(self) -> bool:
        return (
            not self.in_quote
            and not self.in_comment
            and self.round_depth == 0
            and self.square_depth == 0
            and self.curly_depth == 0
            and self.angle_depth == 0
        )

    def feed(self, text: str, index: int) -> None:
        char = text[index]
        previous = text[index - 1] if index > 0 else ""
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if self.line_comment:
            return
        if self.block_comment:
            if previous == "*" and char == "/":
                self.block_comment = False
            return

        if self.quote:
            if self.escape:
                self.escape = False
            elif char == "\\":
                self.escape = True
            elif char == self.quote:
                self.quote = None
            return

        if char in {'"', "'"}:
            self.quote = char
            return
        if char == "/" and next_char == "/":
            self.line_comment = True
            return
        if char == "/" and next_char == "*":
            self.block_comment = True
            return

        if char == "(":
            self.round_depth += 1
        elif char == ")":
            self.round_depth -= 1
        elif char == "[":
            self.square_depth += 1
        elif char == "]":
            self.square_depth -= 1
        elif char == "{":
            self.curly_depth += 1
        elif char == "}":
            self.curly_depth -= 1
        elif char == "<":
            self.angle_depth += 1
        elif char == ">":
            self.angle_depth -= 1
