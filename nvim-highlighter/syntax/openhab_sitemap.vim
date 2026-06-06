if exists('b:current_syntax')
  finish
endif

syn case match

syn region openhabSiteComment start='/\*' end='\*/' keepend contains=@Spell
syn match openhabSiteComment '//.*$' contains=@Spell

syn region openhabSiteString start='"' skip='\\."' end='"' contains=openhabSiteFormat
syn match openhabSiteNumber '\v<\d+(\.\d+)?>'
syn match openhabSiteAssignment '\<[A-Za-z_][A-Za-z0-9_]*\ze\s*='
syn match openhabSiteItemRef '\<item\s*=\s*\zs[A-Za-z_][A-Za-z0-9_]*'
syn match openhabSiteFormat '%\(\d\+\)\=\.\=\d*[dfs%]'

syn keyword openhabSiteKeyword sitemap Frame Group Text Switch Slider Selection Setpoint Color Mapview Video Webview Image Chart Input Default List
syn keyword openhabSiteAttr item label icon mappings visibility valuecolor labelcolor command release period refresh height staticIcon url service step minValue maxValue sendFrequency switchSupport
syn keyword openhabSiteState ON OFF OPEN CLOSED UP DOWN STOP PLAY PAUSE NEXT PREVIOUS REWIND FASTFORWARD INCREASE DECREASE MOVE
syn keyword openhabSitePeriod D W M Y h

hi def link openhabSiteComment Comment
hi def link openhabSiteString String
hi def link openhabSiteNumber Number
hi def link openhabSiteAssignment Identifier
hi def link openhabSiteItemRef Identifier
hi def link openhabSiteFormat Special
hi def link openhabSiteKeyword Keyword
hi def link openhabSiteAttr Type
hi def link openhabSiteState Constant
hi def link openhabSitePeriod Constant

let b:current_syntax = 'openhab_sitemap'
