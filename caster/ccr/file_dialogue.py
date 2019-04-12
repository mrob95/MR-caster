from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key, MappingRule, Pause, Repeat, Text, Choice)

from caster.lib.merge.mergerule import MergeRule
from caster.lib import control

class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"
    mwith = "Core"

    mapping = {
        "go up [<n>]"        : Key("a-up")*Repeat(extra="n"),
        "go back [<n>]"      : Key("a-left")*Repeat(extra="n"),
        "go forward [<n>]"   : Key("a-right")*Repeat(extra="n"),
        "(files | file list)": Key("a-d, f6:3"),
        "navigation [pane]"  : Key("a-d, f6:2"),
        "file name [<dict>]" : Key("a-d, f6:5") + Text("%(dict)s"),

        "dot <ext>"          : Text(".%(ext)s"),
    }
    extras = [
        IntegerRef("n", 1, 10),
        Dictation("dict"),
        Choice("ext", {
                "batch": "bat",
                "(hyper | HTML)": "html",
                "git ignore": "gitignore",
                "mark [down]": "md",
                "PDF": "pdf",
                "(pie | python)": "py",
                "R": "R",
                "R mark [down]": "Rmd",
                "shell": "sh",
                "tech": "tex",
                "tommel": "toml",
                "yammel": "yml",
            }),
    ]
    defaults = {
        "n": 1,
        "dict": "",
    }

context = AppContext(title="save") | AppContext(title="open") | AppContext(title="select")

control.nexus().merger.add_app_rule(FileDialogueRule(), context=context)