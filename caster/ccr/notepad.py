from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef, Repeat
from caster.lib.actions import Key, Text, Mouse
from caster.lib.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule


class Notepad(MergeRule):
    mwith = "Core"
    mcontext = AppContext(title="notepad")
    mapping = {
        "splat [<splatdir>] [<nnavi10>]":
            Key("%(splatdir)s") * Repeat(extra="nnavi10") + Key("backspace"),
    }

    extras = [
        IntegerRef("nnavi10", 1, 11),
        Choice("splatdir", {
            "lease":"cs-left",
            "ross":"cs-right",
        }),

    ]

    defaults = {
        "nnavi10": 1,
        "splatdir": "cs-left",
    }

control.nexus().merger.add_app_rule(Notepad())