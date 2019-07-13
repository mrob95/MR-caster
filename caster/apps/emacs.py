from caster.imports import *

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
        "copy number <ln1>":        Key("c-x, r, s, %(ln1)d"),
        "paste number <ln1>":       Key("c-x, r, i, %(ln1)d"),
        "line <ln1>":         Key("a-g, g") + Text("%(ln1)s") + Key("enter"),

        "menu": Key("a-m"),
        "show help": Key("c-h"),
        "shell command": Key("a-m, exclamation"),
        "toggle sidebar": Key("a-m, f, t"),
        "toggle line numbers": Key("a-m, t, n"),
    }
    extras = [
        Dictation("mim"),
        IntegerRef("ln1", 1, 1000),
    ]
    defaults = {"ln1": 1, "mim": ""}

control.non_ccr_app_rule(EmacsRule())

#---------------------------------------------------------------------------