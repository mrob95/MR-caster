'''
Mike Roberts 13/09/18
'''

from dragonfly import (Dictation, Grammar, IntegerRef, MappingRule,
                       Pause, Repeat)
from caster.lib.actions import Key, Text, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib.merge.mergerule import MergeRule


class RStudioRule(MergeRule):
    pronunciation = "R studio"

    mapping = {
    "new file"                         :  Key("cs-n"),
    "open file"                        :  Key("c-o"),
    "save all"                         :  Key("ac-s"),
    "select all"                       :  Key("c-a"),
    "find"                             :  Key("c-f"),

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
        Store() + Key("c-2") + Text("library(vtable)") + Key("enter/50") + Retrieve() + Key("space, percent, rangle, percent") + Text(" vtable()") + Key("enter/50, c-1"),
    }
    extras = [
        IntegerRef("n", 1, 10000),
    ]
    defaults = {}

context = AppContext(executable="rstudio")
grammar = Grammar("RStudio", context=context)
rule = RStudioRule()
grammar.add_rule(RStudioRule(name="rstudio"))
grammar.load()
