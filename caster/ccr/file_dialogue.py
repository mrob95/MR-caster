from dragonfly import (Dictation, Grammar, IntegerRef, Pause, Repeat, Choice)

from caster.lib.dfplus.actions import Text, Key
from caster.lib.dfplus.context import AppContext
from caster.lib.merge.mergerule import MergeRule
from caster.lib import control, utilities

CORE = utilities.load_toml_relative("config/core.toml")

class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"
    mwith = "Core"
    mcontext = AppContext(title=["save", "open", "select", "choose directory"])

    mapping = {
        "go up [<n>]"        : Key("a-up:%(n)s"),
        "go back [<n>]"      : Key("a-left:%(n)s"),
        "go forward [<n>]"   : Key("a-right:%(n)s"),
        "(files | file list)": Key("a-d, f6:3"),
        "navigation [pane]"  : Key("a-d, f6:2"),
        "file name [<text>]" : Key("a-d, f6:5") + Text("%(text)s"),

        "dot <ext>"          : Text(".%(ext)s"),

        "go <directory>"     : Key("a-d/20") + Text("%(directory)s") + Key("enter"),
    }
    extras = [
        Dictation("text"),
        Choice("directory", CORE["directories"]),
        Choice("ext", {
            "batch"         : "bat",
            "(hyper | HTML)": "html",
            "git ignore"    : "gitignore",
            "mark [down]"   : "md",
            "PDF"           : "pdf",
            "(pie | python)": "py",
            "R"             : "R",
            "R mark [down]" : "Rmd",
            "shell"         : "sh",
            "tech"          : "tex",
            "text"          : "txt",
            "tommel"        : "toml",
            "yammel"        : "yml",
        }),
    ]
    defaults = {
        "text": "",
    }

control.app_rule(FileDialogueRule())