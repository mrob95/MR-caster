from caster.imports import *

class fmanRule(MergeRule):
    pronunciation = "F man"
    mcontext = AppContext(executable="fman", title="fman")

    mapping = {
        "copy"                       : Key("f5"),
        "deselect"                   : Key("c-d"),
        "edit"                       : Key("f4"),
        "end"                        : Key("end"),
        "explorer"                   : Key("f10"),
        "go <fav>"                   : Key("c-0/15") + Text("%(fav)s") + Key("enter"),
        "go see"                     : Key("c-p/15") + Text("c") + Key("enter"),
        "go external"                : Key("c-p/15") + Text("e") + Key("enter"),
        "go to"                      : Key("c-p"),
        "move"                       : Key("f6"),
        "new file"                   : Key("s-f4"),
        "new folder"                 : Key("f7"),
        "open left"                  : Key("c-left"),
        "open right"                 : Key("c-right"),
        "properties"                 : Key("a-enter"),
        "refresh"                    : Key("c-r"),
        "rename"                     : Key("s-f6"),
        "search"                     : Key("cs-f"),
        "(set | add) favourite"      : Key("s-f"),
        "show favourites"            : Key("c-0"),
        "(show | hide) hidden"       : Key("c-dot"),
        "sort [by] name"             : Key("c-f1"),
        "sort [by] size"             : Key("c-f2"),
        "sort [by] (modified | date)": Key("c-f3"),
        "stoosh path"                : Key("f11"),
        "terminal"                   : Key("f9"),
        "command pallette"           : Key("cs-p"),
    }

    extras = [
        IntegerRef("num", 1, 4, 1),
        Choice("fav", {
            "advent": "adv",
            "(docks | documents)":"docs",
            "(downs | download)":"downs",
            "git caster":"gcast",
            "mike":"mike",
            "math fly": "mf",
            "user caster":"ucast",
            "uni [work]":"uni",
        }),
    ]

control.non_ccr_app_rule(fmanRule())