from dragonfly import (Grammar, Dictation, IntegerRef)
from caster.lib.dfplus.actions import Key, Text
from caster.lib.dfplus.context import AppContext

from caster.lib import control
from caster.lib.merge.mergerule import MergeRule

class EmacsRule(MergeRule):
    pronunciation = "E max"
    mcontext = AppContext(executable="emacs", title="emacs")

    mapping = {
        "open file":              Key("c-x, c-f"),
        "go to file":              Key("a-m, f, f"),
        "go to project":              Key("a-m, p, f"),
        "cancel":              Key("c-g"),
        "save file":              Key("c-x, c-s"),
        "save as":                Key("c-x, c-w"),
        "save all":               Key("c-x, s"),
        "revert to file":         Key("c-x, c-v"),
        "revert buffer":          Key("a-x"),
        "close buffer":           Key("c-x, c-c"),
        "begin selection":        Key("c-space"),
        "cancel selection":       Key("c-g"),
        "cut selection":          Key("c-w"),
        "paste":                  Key("c-y"),
        "copy number <n>":        Key("c-x, r, s, %(n)d"),
        "paste number <n>":       Key("c-x, r, i, %(n)d"),
        "line <n>":         Key("a-g, g") + Text("%(n)s") + Key("enter"),

        "menu": Key("a-m"),
        "show help": Key("c-h"),
        "shell command": Key("a-m, exclamation"),
        "toggle sidebar": Key("a-m, f, t"),
        "toggle line numbers": Key("a-m, t, n"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRef("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}

control.non_ccr_app_rule(EmacsRule())

#---------------------------------------------------------------------------