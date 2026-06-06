if exists('b:current_syntax')
  finish
endif

syn case match

syn region openhabRuleComment start='/\*' end='\*/' keepend contains=@Spell
syn match openhabRuleComment '//.*$' contains=@Spell

syn region openhabRuleString start='"' skip='\\."' end='"'
syn match openhabRuleNumber '\v<\d+(\.\d+)?>'
syn match openhabRuleFunction '\<[A-Za-z_][A-Za-z0-9_]*\ze\s*('
syn match openhabRuleTypeName '\<[A-Z][A-Za-z0-9_:<>.]*\>'
syn match openhabRuleOperator '=>\|===\|!==\|==\|!=\|<=\|>=\|&&\|||\|::'

syn keyword openhabRuleTop import rule when then end var val new null
syn keyword openhabRuleFlow if else switch case default for while return try catch finally in
syn keyword openhabRuleTrigger Item Member System Time Channel Thing changed received command update from to or and cron started status
syn keyword openhabRuleSpecial receivedCommand previousState triggeringItem triggeringGroup state newState oldState now
syn keyword openhabRuleState ON OFF OPEN CLOSED UP DOWN STOP PLAY PAUSE NEXT PREVIOUS REWIND FASTFORWARD INCREASE DECREASE MOVE UNDEF NULL REFRESH
syn keyword openhabRuleBoolean true false

hi def link openhabRuleComment Comment
hi def link openhabRuleString String
hi def link openhabRuleNumber Number
hi def link openhabRuleFunction Function
hi def link openhabRuleTypeName Type
hi def link openhabRuleOperator Operator
hi def link openhabRuleTop Keyword
hi def link openhabRuleFlow Conditional
hi def link openhabRuleTrigger Repeat
hi def link openhabRuleSpecial Identifier
hi def link openhabRuleState Constant
hi def link openhabRuleBoolean Boolean

let b:current_syntax = 'openhab_rules'
