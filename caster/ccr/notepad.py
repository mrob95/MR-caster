from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef, Repeat, Clipboard
from caster.lib.actions import Key, Text, Mouse
from caster.lib.context import AppContext
import markdown2

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule


def CliptoHTML():
    Key("c-c/10").execute()
    cb = Clipboard.get_system_text()
    html = markdown2.markdown(cb)
    Clipboard.set_system_text(html)

class Notepad(MergeRule):
    mwith = "Core"
    mcontext = AppContext(title="notepad")
    mapping = {
        "splat [<splatdir>] [<n>]":
            Key("%(splatdir)s") * Repeat(extra="n") + Key("backspace"),
        "copy HTML": Function(CliptoHTML),

        "select up [<n>]": Function(lambda n: Key("s-up:%s" % str(n-1)).execute()) + Key("s-home"),
        "select down [<n>]": Function(lambda n: Key("s-down:%s" % str(n-1)).execute()) + Key("s-end"),

    }

    extras = [
        IntegerRef("n", 1, 11),
        Choice("splatdir", {
            "lease":"cs-left",
            "ross":"cs-right",
        }),

    ]

    defaults = {
        "nnavi10": 1,
        "splatdir": "cs-left",
    }

control.app_rule(Notepad())