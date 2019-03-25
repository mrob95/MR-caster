from dragonfly import Grammar, Repeat, IntegerRef
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext

from caster.lib.merge.mergerule import MergeRule


class photoshopRule(MergeRule):
    pronunciation = "Photo shop"

    mapping = {
        "new (file | pane)": Key("c-n"),

        "open file":    Key("c-o"),
        "close file":    Key("c-w"),

        "transform":    Key("c-t"),
        "deselect": Key("c-d"),

        "new layer": Key("cas-n"),

        "open folder":  Key("cs-o"),
        "save as":  Key("cs-s"),

        "step backwards [<n>]": Key("ca-z")*Repeat(extra="n"),
        "step forwards [<n>]": Key("cs-z")*Repeat(extra="n"),

        "zoom in [<n>]": Key("c-equals")*Repeat(extra="n"),
        "zoom out [<n>]": Key("c-minus")*Repeat(extra="n"),

        }

    extras = [
        IntegerRef("n", 1, 10),
    ]
    defaults = {
        "n": 1,
    }


context = AppContext(executable="photoshop", title="photoshop")
grammar = Grammar("photoshop", context=context)
rule = photoshopRule()
grammar.add_rule(photoshopRule(name="photoshop"))
grammar.load()
