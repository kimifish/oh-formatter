from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from openhab_formatter.items import VIM_MODELINE, ItemsFormatter
from openhab_formatter.scanner import split_top_level_commas


ROOT = Path(__file__).resolve().parents[1]
MODELINE = f"{VIM_MODELINE}\n"


def fmt(text: str) -> str:
    return ItemsFormatter().format_text(text).text


def test_simple_item_without_config() -> None:
    assert fmt('Switch Test "Test" <switch> (G1) [Tag]\n') == (
        'Switch Test\n'
        '    "Test"\n'
        '    <switch>\n'
        '    (G1)\n'
        '    [Tag]\n'
        f'{MODELINE}'
    )


def test_item_with_channel() -> None:
    assert fmt('Switch Test "Test" <switch> (G1) [Tag] { channel="mqtt:topic:x:y" }\n') == (
        'Switch Test\n'
        '    "Test"\n'
        '    <switch>\n'
        '    (G1)\n'
        '    [Tag]\n'
        '    {\n'
        '        channel="mqtt:topic:x:y"\n'
        '    }\n'
        f'{MODELINE}'
    )


def test_metadata_block() -> None:
    assert fmt('String Test "Test" { ai="state" [ aliases="a,b,c", readable=true, writable=false ] }\n') == (
        'String Test\n'
        '    "Test"\n'
        '    {\n'
        '        ai="state" [\n'
        '            aliases="a,b,c",\n'
        '            readable=true,\n'
        '            writable=false\n'
        '        ]\n'
        '    }\n'
        f'{MODELINE}'
    )


def test_multiple_config_entries() -> None:
    source = 'Number:Temperature T "Temp [%.1f %unit%]" <temperature> (Weather) [Measurement, Temperature] { unit="°C", channel="mqtt:topic:x:y", report="diagnostics" [ priority=35, context=true ] }\n'
    assert fmt(source) == (
        'Number:Temperature T\n'
        '    "Temp [%.1f %unit%]"\n'
        '    <temperature>\n'
        '    (Weather)\n'
        '    [Measurement, Temperature]\n'
        '    {\n'
        '        unit="°C",\n'
        '        channel="mqtt:topic:x:y",\n'
        '\n'
        '        report="diagnostics" [\n'
        '            priority=35,\n'
        '            context=true\n'
        '        ]\n'
        '    }\n'
        f'{MODELINE}'
    )


def test_adjacent_metadata_blocks_have_single_blank_line() -> None:
    source = 'String Test "Test" { ai="state" [ readable=true ], report="diagnostics" [ priority=35 ] }\n'
    assert fmt(source) == (
        'String Test\n'
        '    "Test"\n'
        '    {\n'
        '        ai="state" [\n'
        '            readable=true\n'
        '        ],\n'
        '\n'
        '        report="diagnostics" [\n'
        '            priority=35\n'
        '        ]\n'
        '    }\n'
        f'{MODELINE}'
    )


def test_single_line_config_does_not_consume_next_item() -> None:
    assert fmt('String A "A" {channel="x"}\nString B "B" {channel="y"}\n') == (
        'String A\n'
        '    "A"\n'
        '    {\n'
        '        channel="x"\n'
        '    }\n'
        'String B\n'
        '    "B"\n'
        '    {\n'
        '        channel="y"\n'
        '    }\n'
        f'{MODELINE}'
    )


def test_inline_block_comment_before_config_is_preserved() -> None:
    assert fmt('Number Pressure "Pressure" (G) /*["Measurement", "Pressure"]*/ {channel="x"}\n') == (
        'Number Pressure\n'
        '    "Pressure"\n'
        '    (G)\n'
        '    /*["Measurement", "Pressure"]*/\n'
        '    {\n'
        '        channel="x"\n'
        '    }\n'
        f'{MODELINE}'
    )


def test_trailing_comment_after_config_is_preserved() -> None:
    assert fmt('Group:Switch:OR(ON, OFF) Alarm "Alarm" (G) { ai="equipment" [ readable=true ] } // ["AlarmSystem"]\n') == (
        'Group:Switch:OR(ON, OFF) Alarm\n'
        '    "Alarm"\n'
        '    (G)\n'
        '    {\n'
        '        ai="equipment" [\n'
        '            readable=true\n'
        '        ]\n'
        '    }\n'
        '    // ["AlarmSystem"]\n'
        f'{MODELINE}'
    )


def test_commas_inside_strings_are_not_split() -> None:
    assert split_top_level_commas('aliases="a,b,c", expire="5m,command=OFF"') == [
        'aliases="a,b,c"',
        'expire="5m,command=OFF"',
    ]


def test_comments_preserved_and_unknown_warns() -> None:
    result = ItemsFormatter().format_text('// comment\nnot an item\nSwitch Test "Test"\n')
    assert result.text == f'// comment\nnot an item\nSwitch Test\n    "Test"\n{MODELINE}'
    assert result.warnings == ['line 2: unknown line left unchanged']


def test_modeline_replaces_old_final_modeline() -> None:
    text = 'Switch Test "Test"\n// vim: set fdm=marker:noai:ts=4:sw=4\n'
    assert fmt(text).endswith(MODELINE)
    assert fmt(text).count('// vim:') == 1


def test_fixture_formatting_is_idempotent() -> None:
    for fixture in (ROOT / 'fixtures').glob('*.items'):
        text = fixture.read_text()
        first_result = ItemsFormatter().format_text(text)
        assert first_result.warnings == [], fixture
        first = first_result.text
        second_result = ItemsFormatter().format_text(first)
        assert second_result.warnings == [], fixture
        second = second_result.text
        assert second == first, fixture


def test_cli_stdin_stdout() -> None:
    proc = subprocess.run(
        [sys.executable, '-m', 'openhab_formatter.cli'],
        input='Switch Test "Test"\n',
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )
    assert proc.returncode == 0
    assert proc.stdout == f'Switch Test\n    "Test"\n{MODELINE}'
    assert proc.stderr == ''


def test_cli_check_detects_difference(tmp_path: Path) -> None:
    path = tmp_path / 'test.items'
    path.write_text('Switch Test "Test"\n')
    proc = subprocess.run(
        [sys.executable, '-m', 'openhab_formatter.cli', '--check', str(path)],
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )
    assert proc.returncode == 1
    assert 'needs formatting' in proc.stderr
