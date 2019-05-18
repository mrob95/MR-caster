from dragonfly import Grammar, Repeat, IntegerRef
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext
from caster.lib import control

from caster.lib.merge.mergerule import MergeRule


class PhotoshopRule(MergeRule):
    pronunciation = "Photo shop"
    mcontext = AppContext(title="photoshop")

    mapping = {
        "new (file | pane)"   : Key("c-n"),

        "open file"           : Key("c-o"),
        "close file"          : Key("c-w"),

        "transform"           : Key("c-t"),
        "deselect"            : Key("c-d"),

        "new layer"           : Key("cas-n"),

        "open folder"         : Key("cs-o"),
        "save as"             : Key("cs-s"),

        "step backwards [<n>]": Key("ca-z:%(n)s"),
        "step forwards [<n>]" : Key("cs-z:%(n)s"),

        "zoom in [<n>]"       : Key("c-equals:%(n)s"),
        "zoom out [<n>]"      : Key("c-minus:%(n)s"),
        }

    extras = [
        IntegerRef("n", 1, 10),
    ]
    defaults = {
        "n": 1,
    }

control.non_ccr_app_rule(PhotoshopRule())