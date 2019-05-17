from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef,
                       Repeat, Pause, Function, Choice)

from caster.lib.actions import Store, Retrieve, Key, Text
from caster.lib.merge.mergerule import MergeRule
from subprocess import Popen
from caster.lib import utilities, control

CORE = utilities.load_toml_relative("config/core.toml")

class WERule(MergeRule):
    pronunciation = "explorer"
    mcontext = AppContext(executable="explorer")

    mapping = {
        "address bar"                        : Key("a-d"),
        "new folder"                         : Key("cs-n"),
        "new file"                           : Key("a-f, w, t"),
        "[(show | file | folder)] properties": Key("a-enter"),
        "go up [<n>]"                        : Key("a-up:%(n)s"),
        "go back [<n>]"                      : Key("a-left:%(n)s"),
        "go forward [<n>]"                   : Key("a-right:%(n)s"),
        "terminal here"                      : Key("f6:5, s-f10, g, down, enter"),
        "go <path>"                          : Key("a-d/20") + Text("%(path)s") + Key("enter"),
        "sublime here"                       :
            Key("a-d:50") + Store() + Key("escape:50") + Function(lambda: Popen(["subl", Retrieve.text() + "/"])),
    }
    extras = [
        IntegerRef("n", 1, 10),
        Choice("path", CORE["directories"]),
    ]
    defaults = {"n":1}

control.nexus().merger.add_non_ccr_app_rule(WERule())

