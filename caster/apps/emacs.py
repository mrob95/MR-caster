from dragonfly import (Grammar, Dictation, IntegerRef)
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext

from caster.lib import control
from caster.lib.merge.mergerule import t



class EmacsRule(t):
    pronunciation = "E max"

    mapping = {
        "open file":              Key("c-x, c-f"),
        "save file":              Key("c-x, c-s"),
        "save as":                Key("c-x, c-w"),
        "save all":               Key("c-x, s"),
        "revert to file":         Key("c-x, c-v"),
        "revert buffer":          Key("a-x"),
        "close buffer":           Key("c-x, c-c"),
        "undo":                   Key("c-underscore"),
        "begin selection":        Key("c-space"),
        "cancel selection":       Key("c-g"),
        "cut selection":          Key("c-w"),
        "paste":                  Key("c-y"),
        "copy number <n>":        Key("c-x, r, s, %(n)d"),
        "paste number <n>":       Key("c-x, r, i, %(n)d"),
        "forward delete":         Key("c-delete"),
        "delete word":            Key("a-delete"),
        "forward delete word":    Key("a-d"),
        "word forward":           Key("a-f"),
        "word backward":          Key("a-b"),
        "line forward":           Key("c-a"),
        "line backward":          Key("c-e"),
        "paragraph forward":      Key("a-lbrace"),
        "paragraph backward":     Key("a-rbrace"),
        "document forward":       Key("a-langle"),
        "document backward":      Key("a-rangle"),
        "C function forward":     Key("ac-a"),
        "C function backward":    Key("ac-e"),
        "incremental search":     Key("c-s"),
        "incremental reverse":    Key("c-r"),
        "interactive search":     Key("a-percent"),
        "go to line <n>":         Key("a-x, %(n)d"),
        "prior bracket":          Key("escape:down, c-b, escape:up"),
        "next bracket":           Key("escape:down, c-f, escape:up"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRef("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="emacs", title="emacs")
grammar = Grammar("emacs", context=context)

rule = EmacsRule(name="emacs")
grammar.add_rule(rule)
grammar.load()
