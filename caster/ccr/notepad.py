from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef, Repeat, Clipboard
from caster.lib.actions import Key, Text, Mouse
from caster.lib.context import AppContext
import markdown2

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import t


def CliptoHTML():
    Key("c-c/10").execute()
    cb = Clipboard.get_system_text()
    html = markdown2.markdown(cb)
    Clipboard.set_system_text(html)

class Notepad(t):
    mwith = "Core"
    mcontext = AppContext(title="notepad")
    mapping = {
        "splat [<splatdir>] [<nnavi10>]":
            Key("%(splatdir)s") * Repeat(extra="nnavi10") + Key("backspace"),
        "copy HTML": Function(CliptoHTML),
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