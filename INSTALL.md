# Install on Another Host

This repo contains two pieces:

- `openhab-items-format`: Python CLI formatter for openHAB `.items` files.
- `nvim-highlighter`: Vim/Neovim syntax files for openHAB `.items`, `.things`, `.sitemap`, and `.rules`.

## Formatter

Install the CLI with `uv`:

```bash
uv tool install git+https://github.com/kimifish/oh-formatter.git
```

Verify:

```bash
openhab-items-format --help
```

Update later:

```bash
uv tool install --force git+https://github.com/kimifish/oh-formatter.git
```

## Neovim Highlighter

Add the repo as a `lazy.nvim` plugin:

```lua
{
  "kimifish/oh-formatter",
  ft = { "openhab_items", "openhab_things", "openhab_sitemap", "openhab_rules" },
  config = function(plugin)
    vim.opt.runtimepath:append(plugin.dir .. "/nvim-highlighter")
  end,
}
```

Add filetype detection if it is not configured elsewhere:

```lua
vim.filetype.add({
  extension = {
    items = "openhab_items",
    things = "openhab_things",
    sitemap = "openhab_sitemap",
    rules = "openhab_rules",
  },
})
```

## conform.nvim

Configure formatting for `.items` files:

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

The formatter writes formatted content to stdout and diagnostics to stderr, so it is safe for `conform.nvim` stdin mode.
