# oh-formatter

Formatter and Neovim syntax support for openHAB text configuration files.

The project currently implements a formatter for `.items` files and ships Vim/Neovim syntax files for `.items`, `.things`, `.sitemap`, and `.rules`.

## Features

- CLI command: `openhab-items-format`.
- Safe stdin/stdout mode for `conform.nvim`.
- `--write`, `--check`, and `--diff` modes.
- Idempotent formatting.
- Scanner-based comma splitting that respects strings and nested `()`, `[]`, `{}`, and `<>` blocks.
- Multi-line formatting for openHAB metadata blocks such as `ai="state" [ ... ]`.
- Preserves comments and unknown lines where possible.
- Adds a Vim modeline for indent folds: `fdm=indent`.

## Example

Input:

```java
Number:Temperature Outdoor_Temperature "Temperature [%.1f %unit%]" <temperature> (Weather) ["Measurement", "Temperature"] { unit="°C", channel="mqtt:topic:demo:weather:temperature", ai="state" [ aliases="temperature,outdoor temperature", readable=true, writable=false, safety="read-only" ] }
```

Output:

```java
Number:Temperature Outdoor_Temperature
    "Temperature [%.1f %unit%]"
    <temperature>
    (Weather)
    ["Measurement", "Temperature"]
    {
        unit="°C",
        channel="mqtt:topic:demo:weather:temperature",

        ai="state" [
            aliases="temperature,outdoor temperature",
            readable=true,
            writable=false,
            safety="read-only"
        ]
    }
// vim: set fdm=indent:noai:ts=4:sw=4:et:
```

## CLI

```bash
openhab-items-format file.items
openhab-items-format --write file.items
openhab-items-format --check file.items
openhab-items-format --diff file.items
cat file.items | openhab-items-format
```

Exit codes:

- `0`: success.
- `1`: file/parser error, or `--check`/`--diff` found differences.
- `2`: invalid CLI arguments.

## Install

See [`INSTALL.md`](INSTALL.md).

Quick formatter install:

```bash
uv tool install git+https://github.com/kimifish/oh-formatter.git
```

## Neovim

The `nvim-highlighter/` directory is a regular Vim runtime subtree with `ftdetect/`, `ftplugin/`, and `syntax/` files.

With `lazy.nvim`, add this repo and append `nvim-highlighter` to `runtimepath`. Full config is in [`INSTALL.md`](INSTALL.md).

## Development

```bash
uv run pytest
```

The public fixtures in `fixtures/` are synthetic examples only.
