from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef, Key, Text,
                       Repeat, Pause, Function)

from caster.lib.actions import Store, Retrieve
from caster.lib.merge.mergerule import MergeRule
from subprocess import Popen
from caster.lib import utilities

def terminal_here():
    Key("a-d:50").execute()
    _, text = utilities.read_selected(True)
    Key("escape:50").execute()
    utilities.terminal(text)

class IERule(MergeRule):
    pronunciation = "explorer"

    mapping = {
        "address bar":                        Key("a-d"),
        "new folder":                         Key("cs-n"),
        "new file":                           Key("a-f, w, t"),
        "[(show | file | folder)] properties":  Key("a-enter"),
        "go up [<n>]":                        Key("a-up")* Repeat(extra="n"),
        "go back [<n>]":                      Key("a-left")* Repeat(extra="n"),
        "go forward [<n>]":                   Key("a-right")* Repeat(extra="n"),
        "terminal here":
            Key("a-d:50") + Store() + Key("escape:50") + Function(lambda: utilities.terminal(Retrieve.text())),
    }
    extras = [
        IntegerRef("n", 1, 10)
    ]
    defaults = {"n":1}


#---------------------------------------------------------------------------

context = AppContext(executable="explorer")
grammar = Grammar("Windows Explorer", context=context)
rule = IERule(name="explorer")
grammar.add_rule(rule)
grammar.load()


