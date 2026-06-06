# nvim-openhab

Minimal Vim syntax plugin for openHAB text configuration in Neovim.

Supported file types:

- `*.items`
- `*.things`
- `*.rules`
- `*.sitemap`

What it does:

- detects openHAB filetypes automatically
- provides syntax highlighting for common DSL constructs
- sets `//` comments and `/* ... */` block comments in `ftplugin`
- keeps the implementation plain Vim syntax, no Treesitter

## Install with lazy.nvim

Point lazy at the local path after you create your symlink:

```lua
{
  dir = "/path/to/nvim-openhab",
  lazy = false,
}
```

If you symlink this directory directly into your plugin tree, Neovim will pick up `ftdetect/`, `syntax/`, and `ftplugin/` automatically.

## Filetypes

The plugin sets these filetypes:

- `openhab_items`
- `openhab_things`
- `openhab_rules`
- `openhab_sitemap`

## Scope

This is intentionally syntax-only. It focuses on the most common openHAB text patterns:

- item types, tags, metadata, icons, channels
- thing and channel declarations with config keys and transformation chains like `REGEX:...∩JSONPATH:...`
- rule structure, triggers, states, functions, common DSL keywords
- sitemap widgets, attributes, mappings, and chart periods

## Samples

Use the files under `test/` to check detection and highlighting quickly:

```bash
nvim test/sample.items
nvim test/sample.things
nvim test/sample.rules
nvim test/sample.sitemap
```

## Notes

- `openhab_rules` is highlighted as openHAB DSL, not Java.
- The patterns are conservative and aim to be useful rather than exhaustive.
- If you want more coverage later, the easiest extension points are the keyword lists in `syntax/*.vim`.
