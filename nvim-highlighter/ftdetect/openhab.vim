augroup openhab_ftdetect
  autocmd!
  autocmd BufRead,BufNewFile *.items set ft=openhab_items
  autocmd BufRead,BufNewFile *.things set ft=openhab_things
  autocmd BufRead,BufNewFile *.rules set ft=openhab_rules
  autocmd BufRead,BufNewFile *.sitemap set ft=openhab_sitemap
augroup END
