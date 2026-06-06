from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path
from typing import Protocol

from .items import ItemsFormatter
from .model import FormatResult


class Formatter(Protocol):
    def format_text(self, text: str) -> FormatResult: ...


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="openhab-items-format")
    parser.add_argument("file", nargs="?")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--diff", action="store_true")
    args = parser.parse_args(argv)

    if sum(bool(flag) for flag in (args.write, args.check, args.diff)) > 1:
        print("--write, --check and --diff are mutually exclusive", file=sys.stderr)
        return 2
    if args.write and not args.file:
        print("--write requires a file argument", file=sys.stderr)
        return 2

    formatter = ItemsFormatter()
    try:
        return run_format_command(formatter, args.file, args.write, args.check, args.diff)
    except OSError as error:
        print(str(error), file=sys.stderr)
        return 1


def run_format_command(formatter: Formatter, file: str | None, write: bool, check: bool, diff: bool) -> int:
    path = Path(file) if file else None
    source = path.read_text() if path else sys.stdin.read()
    result = formatter.format_text(source)

    for warning in result.warnings:
        prefix = f"{path}: " if path else ""
        print(f"{prefix}{warning}", file=sys.stderr)

    if check:
        if source != result.text:
            name = str(path) if path else "<stdin>"
            print(f"{name}: needs formatting", file=sys.stderr)
            return 1
        return 0

    if diff:
        if source == result.text:
            return 0
        fromfile = str(path) if path else "stdin"
        sys.stdout.write(
            "".join(
                difflib.unified_diff(
                    source.splitlines(keepends=True),
                    result.text.splitlines(keepends=True),
                    fromfile=fromfile,
                    tofile=f"{fromfile} (formatted)",
                )
            )
        )
        return 1

    if write:
        assert path is not None
        if source != result.text:
            path.write_text(result.text)
        return 0

    sys.stdout.write(result.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
