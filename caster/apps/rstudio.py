'''
Mike Roberts 13/09/18
'''

from dragonfly import (Dictation, Grammar, IntegerRef, MappingRule,
                       Pause, Repeat, ShortIntegerRef, Choice, Function)
from caster.lib.actions import Key, Text, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib.merge.mergerule import MergeRule
from caster.lib import control, navigation


class RStudioRule(MergeRule):
    pronunciation = "R studio"
    mcontext = AppContext(executable="rstudio")

    mapping = {
        "new (file | tab)"                 :  Key("cs-n"),
        "open file"                        :  Key("c-o"),
        "save all"                         :  Key("ac-s"),
        "select all"                       :  Key("c-a"),
        "find"                             :  Key("c-f"),
        "align that"                       :  Key("c-i"),

        "[go to] line <n>"                 :  Key("as-g/10") + Text("%(n)s") + Key("enter"),

        "focus (console | terminal)"       :  Key("c-2"),
        "focus (main | editor)"            :  Key("c-1"),

        "next tab"                         :  Key("c-f12"),
        "first tab"                        :  Key("cs-f11"),
        "previous tab"                     :  Key("c-f11"),
        "last tab"                         :  Key("cs-f12"),
        "close tab"                        :  Key("c-w"),

        "run (line | that)"                :  Key("c-enter"),
        "run document"                     :  Key("ac-r"),
        "comment (line | selected | block)":  Key("cs-c"),
        "knit (document | file)"           :  Key("cs-k"),

        "next plot"                        :  Key("ac-f12"),
        "previous plot"                    :  Key("ac-f11"),

        "help that":
            Store() + Key("c-2, question") + Retrieve() + Key("enter/50, c-1"),
        "glimpse that":
            Store() + Key("c-2") + Retrieve() + Key("space, percent, rangle, percent") + Text(" glimpse()") + Key("enter/50, c-1"),
        "head that":
            Store() + Key("c-2") + Retrieve() + Key("space, percent, rangle, percent") + Text(" head()") + Key("enter/50, c-1"),
        "vee table that":
            Store() + Key("c-2") + Text("library(vtable)") + Key("enter/50") + Retrieve() + Text(" %>% vtable()", static=True) + Key("enter/50, c-1"),

        "<action> [line] <n> [(by | to) <nn>]"  :
            Function(navigation.action_lines, go_to_line="as-g/10", select_line_down="s-down", wait="/3"),

    }
    extras = [
        ShortIntegerRef("n", 1, 1000),
        ShortIntegerRef("nn", 1, 1000),
        Choice("action", {
            "select": "",
            "copy": "c-c",
            "cut": "c-x",
            "(delete | remove)": "backspace",
            "replace": "c-v",
            }),
    ]
    defaults = {
        "nn": None,
    }

control.nexus().merger.add_non_ccr_app_rule(RStudioRule())