from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key, MappingRule, Pause, Repeat, Choice)

from caster.lib.actions import Text
from caster.lib.context import TitleContext
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

        "go <path>"          : Key("a-d/20") + Text("%(path)s") + Key("enter"),
    }
    extras = [
        IntegerRef("n", 1, 10),
        Dictation("dict"),
        Choice("path", {
               "caster"   : "C:\\Users\\Mike\\Documents\\NatLink\\caster",
               "documents": "C:\\Users\\Mike\\Documents",
               "films"    : "E:\\films",
               "git hub"  : "C:\\Users\\Mike\\Documents\\GitHub",
               "math fly" : "C:\\Users\\Mike\\Documents\\NatLink\\mathfly",
               "pictures" : "C:\\Users\\Mike\\Pictures",
               "queue tea": "C:\\Users\\Mike\\Pictures\\pol\\qt",
               "sea"      : "C:\\",
               "uni work" : "C:\\Users\\Mike\\Documents\\1_uni_work",
            }),
        Choice("ext", {
                "batch"            : "bat",
                "(hyper | HTML)"   : "html",
                "git ignore"       : "gitignore",
                "(mark | markdown)": "md",
                "PDF"              : "pdf",
                "(pie | python)"   : "py",
                "R"                : "R",
                "R mark [down]"    : "Rmd",
                "shell"            : "sh",
                "tech"             : "tex",
                "tommel"           : "toml",
                "yammel"           : "yml",
            }),
    ]
    defaults = {
        "n": 1,
        "dict": "",
    }

context = TitleContext("save", "open", "select")

control.nexus().merger.add_app_rule(FileDialogueRule(), context=context)