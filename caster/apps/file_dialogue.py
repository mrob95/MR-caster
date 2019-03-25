from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key, MappingRule,
                       Pause, Repeat, Text)

from caster.lib.merge.mergerule import MergeRule


class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"

    mapping = {
        "go up [<n>]":      Key("a-up")*Repeat(extra="n"),
        "go back [<n>]":    Key("a-left")*Repeat(extra="n"),
        "go forward [<n>]": Key("a-right")*Repeat(extra="n"),
        "(files | file list)": Key("a-d, f6:3"),
        "navigation [pane]":   Key("a-d, f6:2"),
        "file name":         Key("a-d, f6:5"),
    }
    extras = [IntegerRef("n", 1, 10)]
    defaults = {
        "n": 1,
    }



dialogue_names = ["open",
				"select",
				]

context = AppContext(title="save") 
for name in dialogue_names:
	context = context | AppContext(title=name)

grammar = Grammar("FileDialogue", context=context)
rule = FileDialogueRule()
grammar.add_rule(FileDialogueRule(name="filedialogue"))
grammar.load()
