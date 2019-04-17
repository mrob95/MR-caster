from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef,
                       Repeat, Pause, Function, Choice)

from caster.lib.actions import Store, Retrieve, Key, Text
from caster.lib.merge.mergerule import MergeRule
from subprocess import Popen
from caster.lib import utilities

CORE = utilities.load_toml_relative("config/core.toml")

class IERule(MergeRule):
    pronunciation = "explorer"

    mapping = {
        "address bar"                        : Key("a-d"),
        "new folder"                         : Key("cs-n"),
        "new file"                           : Key("a-f, w, t"),
        "[(show | file | folder)] properties": Key("a-enter"),
        "go up [<n>]"                        : Key("a-up")* Repeat(extra="n"),
        "go back [<n>]"                      : Key("a-left")* Repeat(extra="n"),
        "go forward [<n>]"                   : Key("a-right")* Repeat(extra="n"),
        "terminal here"                      :
            Key("f6:5, s-f10, g, down, enter"),
            # Key("a-d:50") + Store() + Key("escape:50") + Function(lambda: utilities.terminal(Retrieve.text())),
        "sublime here"                       :
            Key("a-d:50") + Store() + Key("escape:50") + Function(lambda: Popen(["subl", Retrieve.text() + "/"])),

        "go <path>"          : Key("a-d/20") + Text("%(path)s") + Key("enter"),

    }
    extras = [
        IntegerRef("n", 1, 10),
        Choice("path", CORE["directories"]),
    ]
    defaults = {"n":1}


#---------------------------------------------------------------------------

context = AppContext(executable="explorer")
grammar = Grammar("Windows Explorer", context=context)
rule = IERule(name="explorer")
grammar.add_rule(rule)
grammar.load()


