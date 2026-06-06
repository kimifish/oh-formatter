if exists('b:current_syntax')
  finish
endif

syn case match

syn region openhabThingComment start='/\*' end='\*/' keepend contains=@Spell
syn match openhabThingComment '//.*$' contains=@Spell

syn region openhabThingString start='"' skip='\\."' end='"' contains=openhabThingTransformName,openhabThingTransformPipe,openhabThingTransformRegex,openhabThingTransformPath
syn match openhabThingNumber '\v<\d+(\.\d+)?>'
syn match openhabThingUID '\v[a-zA-Z0-9_+-]+(:[a-zA-Z0-9_+.-]+){1,}'
syn match openhabThingLocation '@\s*"[^\"]\+"'
syn match openhabThingConfigKey '\<[A-Za-z_][A-Za-z0-9_]*\ze\s*='
syn match openhabThingTransformName '\<\(REGEX\|JSON\|JSONPATH\|MAP\|JS\|XSLT\|EXEC\|CSV\|XPath\|JINJA\)\ze:' contained
syn match openhabThingTransformPipe '∩' contained
syn match openhabThingTransformPipe '|' contained
syn match openhabThingTransformRegex 'REGEX:\zs[^∩|"]*' contained
syn match openhabThingTransformPath '\<\(JSON\|JSONPATH\)\:\zs\$[^∩|"]*' contained

syn keyword openhabThingKeyword Bridge Thing Type Channels channelTypeUID location property retained trigger stateTopic commandTopic transformationPattern transformationPatternOut formatBeforePublish on off min max step
syn keyword openhabThingType switch contact dimmer number string rollershutter color player image location datetime
syn keyword openhabThingBoolean true false

hi def link openhabThingComment Comment
hi def link openhabThingString String
hi def link openhabThingNumber Number
hi def link openhabThingUID Underlined
hi def link openhabThingLocation Special
hi def link openhabThingConfigKey Identifier
hi def link openhabThingTransformName Special
hi def link openhabThingTransformPipe Operator
hi def link openhabThingTransformRegex String
hi def link openhabThingTransformPath Underlined
hi def link openhabThingKeyword Keyword
hi def link openhabThingType Type
hi def link openhabThingBoolean Boolean

let b:current_syntax = 'openhab_things'
