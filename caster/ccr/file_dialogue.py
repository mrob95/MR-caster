from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Pause, Repeat, Choice)

from caster.lib.actions import Text, Key
from caster.lib.context import TitleContext
from caster.lib.merge.mergerule import MergeRule
from caster.lib import control, utilities

CORE = utilities.load_toml_relative("config/core.toml")

class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"
    mwith = "Core"
    mcontext = TitleContext("save", "open", "select")

    mapping = {
        "go up [<n>]"        : Key("a-up")*Repeat(extra="n"),
        "go back [<n>]"      : Key("a-left")*Repeat(extra="n"),
        "go forward [<n>]"   : Key("a-right")*Repeat(extra="n"),
        "(files | file list)": Key("a-d, f6:3"),
        "navigation [pane]"  : Key("a-d, f6:2"),
        "file name [<dict>]" : Key("a-d, f6:5") + Text("%(dict)s"),

        "dot <ext>"          : Text(".%(ext)s"),

        "go <directory>"     : Key("a-d/20") + Text("%(directory)s") + Key("enter"),
    }
    extras = [
        IntegerRef("n", 1, 10),
        Dictation("dict"),
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
            "tommel"        : "toml",
            "yammel"        : "yml",
        }),
    ]
    defaults = {
        "n"   : 1,
        "dict": "",
    }


control.nexus().merger.add_app_rule(FileDialogueRule())