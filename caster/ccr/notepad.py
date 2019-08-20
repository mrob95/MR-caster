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

        "<action> up <n>": 
            Function(lambda action, n: 
                Key("up:%s, home, s-down:%s, s-end, %s" % (n-1, n, action)).execute()),
        "<action> down [<n>]": 
            Function(lambda action, n: 
                Key("home, s-down:%s, s-end, %s" % (n-1, action)).execute()),
    }
    extras = [
        Choice("action", navigation.actions),
        Choice("splatdir", {
            "lease":"cs-left",
            "ross":"cs-right",
        }, "cs-left"),
    ]

control.app_rule(Notepad())