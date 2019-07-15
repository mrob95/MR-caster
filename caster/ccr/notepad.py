from caster.imports import *

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
            Key("%(splatdir)s") * Repeat("n") + Key("backspace"),
        "copy HTML":
            Function(CliptoHTML),
        "select up [<n>]":
            Function(lambda n: Key("s-up:%s" % str(n-1)).execute()) + Key("s-home"),
        "select down [<n>]":
            Function(lambda n: Key("s-down:%s" % str(n-1)).execute()) + Key("s-end"),
    }
    extras = [
        Choice("splatdir", {
            "lease":"cs-left",
            "ross":"cs-right",
        }, "cs-left"),
    ]

control.app_rule(Notepad())