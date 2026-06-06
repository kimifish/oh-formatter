# openHAB Neovim Highlighter

Minimal Vim syntax runtime for openHAB text configuration files.

This directory is part of [`kimifish/oh-formatter`](https://github.com/kimifish/oh-formatter). The repository also provides the `openhab-items-format` CLI formatter.

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

## Install With lazy.nvim

Add the parent repository as a plugin and append this subdirectory to `runtimepath`:

```lua
{
  "kimifish/oh-formatter",
  ft = { "openhab_items", "openhab_things", "openhab_rules", "openhab_sitemap" },
  config = function(plugin)
    vim.opt.runtimepath:append(plugin.dir .. "/nvim-highlighter")
  end,
}
```

The runtime subtree contains `ftdetect/`, `syntax/`, and `ftplugin/` files. If you copy or symlink `nvim-highlighter/` directly into a plugin directory, Neovim can also load it without the `runtimepath:append` line.

## Formatter Integration

Install the formatter separately:

```bash
uv tool install git+https://github.com/kimifish/oh-formatter.git
```

Then configure `conform.nvim` for `.items` files:

```lua
require("conform").setup({
  formatters_by_ft = {
    openhab_items = { "openhab_items_format" },
  },
  formatters = {
    openhab_items_format = {
      command = "openhab-items-format",
      stdin = true,
    },
  },
})
```

## Filetypes

The plugin sets these filetypes:

- `openhab_items`
- `openhab_things`
- `openhab_rules`
- `openhab_sitemap`

## Scope

This is intentionally syntax-only. It focuses on the most common openHAB text patterns:

- item types, tags, metadata, icons, channels
- Number dimensions such as `Number:Temperature`, `Number:Pressure`, and `Number:Speed`
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
- The `.items` formatter appends a Vim modeline with `fdm=indent`, so formatted item blocks fold naturally by indentation.
