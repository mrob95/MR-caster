from dragonfly import (Grammar, Dictation, Choice, Repeat, Dictation, AppContext, Function, Pause, IntegerRef, ShortIntegerRef)
from caster.lib.actions import Key, Text, Store, Retrieve
import sys
from caster.lib import control
# from caster.lib.integers import IntegerRefMF
from caster.lib.merge.mergerule import MergeRule

def action_lines(action, n, nn):
    if nn:
        num_lines = int(nn)-int(n)+1 if nn>n else int(n)-int(nn)+1
        top_line = min(int(nn), int(n))
    else:
        num_lines = 1
        top_line = int(n)
    command = Key("c-g") + Text(str(top_line)) + Key("enter, s-down:" + str(num_lines) + ", " + action)
    command.execute()

class SublimeRule(MergeRule):
    pronunciation = "sublime"
    mcontext = AppContext(title="Sublime Text")

    mapping = {
        "comment block"                  : Key("cs-slash"),
        "convert indentation"            : Key("f10, v, i, up:2, enter"),

        "edit lines"                     : Key("cs-l"),
        "sort lines"                     : Key("f9"),
        "edit next [<n3>]"               : Key("c-d")*Repeat(extra="n3"),
        "skip next [<n3>]"               : Key("c-k, c-d")*Repeat(extra="n3"),
        "edit all"                       : Key("c-d, a-f3"),
        "reverse selection"              : Key("as-r"),

        "<action> [line] <n> [to <nn>]"  : Function(action_lines),

        "new (file | tab)"               : Key("c-n"),
        # {"keys"                        : ["ctrl+alt+n"], "command": "new_window"},
        "new window"                     : Key("ca-n"),
        "open file"                      : Key("c-o"),
        # {"keys"                        : ["ctrl+shift+o"], "command": "prompt_add_folder"},
        "open folder"                    : Key("cs-o"),
        "open recent"                    : Key("f10, down:4, right, down:9"),
        "save as"                        : Key("cs-s"),
        "save all"                        : Key("f10, f, up:8, enter"),
        "revert (file | [unsaved] changes)": Key("f10, f, up:3, enter"),

        #
        "outdent lines"                  : Key("c-lbracket"),
        "join lines [<n3>]"              : Key("c-j")*Repeat(extra="n3"),
        "match bracket"                  : Key("c-m"),
        #
        # "(select | sell) all"          : Key("c-a"),
        "(select | sell) brackets [<n2>]": Key("cs-m")*Repeat(extra="n2"),
        "(select | sell) indent"         : Key("cs-j"),
        # {"keys"                        : ["ctrl+alt+p"], "command": "expand_selection_to_paragraph"},
        "(select | sell) paragraph"      : Key("ca-p"),
        # SelectUntil
        "(select | sell) until"          : Key("as-s"),

        "toggle side bar"                : Key("c-k, c-b"),
        "show key bindings"              : Key("f10, p, right, k"),

        #
        "find"                           : Key("c-f"),
        "find <dict>"                    : Key("c-f") + Text("%(dict)s") + Key("escape"),
        "find next [<n2>]"               : Key("f3")*Repeat(extra="n2"),
        "find previous [<n2>]"           : Key("s-f3")*Repeat(extra="n2"),
        "find all"                       : Key("a-enter"),
        "replace"                        : Key("c-h"),
        #

        "go to <dict> [<filetype>]"      : Key("c-p") + Text("%(dict)s" + "%(filetype)s") + Key("enter"),
        "go to word"                     : Key("c-semicolon"),
        "go to symbol"                   : Key("c-r"),
        "go to [symbol in] project"      : Key("cs-r"),

        "command pallette [<dict>]"      : Key("cs-p") + Text("%(dict)s"),
        "search in directory"            : Key("cs-f"),
        "go to that"                     : Store() + Key("cs-r") + Retrieve() + Key("enter"),
        "search [for] that"              : Store() + Key("cs-f") + Retrieve() + Key("enter"),
        "find that"                      : Store() + Key("c-f") + Retrieve() + Key("enter"),
        #
        "fold"                           : Key("cs-lbracket"),
        "unfold"                         : Key("cs-rbracket"),
        "unfold all"                     : Key("c-k, c-j"),
        "fold [level] <n2>"              : Key("c-k, c-%(n2)s"),
        #
        "full screen"                    : Key("f11"),
        "(set | add) bookmark"           : Key("c-f2"),
        "next bookmark"                  : Key("f2"),
        "previous bookmark"              : Key("s-f2"),
        "clear bookmarks"                : Key("cs-f2"),
        #
        "build it"                       : Key("c-b"),
        "build with"                     : Key("cs-b"),
        # "cancel build"                 : Key("c-break")),
        #
        "record macro"                   : Key("c-q"),
        "play macro [<n3>]"              : Key("cs-q")*Repeat(extra="n3"),
        "(new | create) snippet"         : Key("a-n"),
        #
        "close tab"                      : Key("c-w"),
        "next tab"                       : Key("c-pgdown"),
        "previous tab"                   : Key("c-pgup"),
        "<nth> tab"                      : Key("a-%(nth)s"),
        #
        "column <cols>"                  : Key("as-%(cols)s"),
        "focus <panel>"                  : Key("c-%(panel)s"),
        "move <panel>"                   : Key("cs-%(panel)s"),

        # {"keys"                        : ["ctrl+alt+v"], "command": "clone_file"}
        "duplicate (tab | file)"         : Key("ca-v"),
        "split right"                    : Key("as-2, c-1, cs-2"),
        #
        "terminal here"                  : Key("cs-t"),

        "zoom in [<n2>]"                 : Key("c-equal")*Repeat(extra="n2"),
        "zoom out [<n2>]"                : Key("c-minus")*Repeat(extra="n2"),

        # wrap plus
        "(wrap | split) lines"           : Key("a-q"),

        "paste from history": Key("c-k, c-v"),

        "format table": Key("cas-t"),


    }
    extras = [
        Dictation("dict"),
        ShortIntegerRef("n",1, 1000),
        # IntegerRef("n",1, 1000),
        # IntegerRef("nn", 1, 1000),
        ShortIntegerRef("nn", 1, 1000),
        IntegerRef("n2", 1, 9),
        IntegerRef("n3", 1, 21),
        Choice("action", {
            "select": "",
            "copy": "c-c",
            "cut": "c-x",
            "delete": "backspace",
            "replace": "c-v",
            }),
        Choice("nth", {
            "first"  : "1",
            "second" : "2",
            "third"  : "3",
            "fourth" : "4",
            "fifth"  : "5",
            "sixth"  : "6",
            "seventh": "7",
            "eighth" : "8",
            "ninth"  : "9",
            }),
        Choice("cols", {"one": "1", "two": "2", "three": "3", "grid": "5",}),
        Choice("panel", {"one": "1", "left": "1", "two": "2", "right": "2", }),
        Choice("filetype", {
            "pie | python": "py",
            "mark [down]": "md",
            "tech": "tex",
            "tommel": "toml",
            }),
    ]
    defaults = {
        "dict": "",
        "nn": None,
        "n2": 1,
        "n3": 1,
        "filetype": "",
    }

control.nexus().merger.add_non_ccr_app_rule(SublimeRule())

#---------------------------------------------------------------------------

class SublimeCCRRule(MergeRule):
    mwith = ["Core"]
    mcontext = AppContext(title="Sublime Text")
    mapping = {
        "line <n>"       : Key("c-g") + Text("%(n)s") + Key("enter, end"),
        # "line <n11> [<n12>] [<n13>]"     : Key("c-g") + Text("%(n11)s" + "%(n12)s" + "%(n13)s") + Key("enter, end"),

        "align that"     : Key("ca-a"),
        "go to file"     : Key("c-p"),
        "comment line"   : Key("c-slash"),

        "transform upper": Key("c-k, c-u"),
        "transform lower": Key("c-k, c-l"),
        # {"keys"        : ["ctrl+k", "ctrl+t"], "command": "title_case"},
        "transform title": Key("c-k, c-t"),

        "(select | sell) scope [<n2>]"   : Key("cs-space")*Repeat(extra="n2"),
        "copy scope"   : Key("cs-space, c-c"),
        "replace scope"   : Key("cs-space, c-v"),

    }
    extras = [
        ShortIntegerRef("n", 1, 1000),
        # IntegerRef("n", 1, 1000),
        IntegerRef("n2", 1, 9),
        IntegerRef("n11", 1, 20),
        IntegerRef("n12", 0, 10),
        IntegerRef("n13", 0, 10),
    ]
    defaults = {"n12": "", "n13": "", "n2": 1}

control.nexus().merger.add_app_rule(SublimeCCRRule())

#---------------------------------------------------------------------------

class SublimeRRule(MergeRule):
    mwith = ["Core", "R"]
    mcontext = AppContext(title=".R") & AppContext(title="Sublime Text")
    mapping = {
        "run (line | that) [<n>]":
            Key("cas-r")*Repeat(extra="n"),
        "open are terminal":
            Key("ca-r"),
        "terminal right":
            Key("ca-r/50, as-2, c-1, cs-2, c-1"),
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
        IntegerRef("n", 1, 9),
    ]
    default = {
        "n": 1,
    }

control.nexus().merger.add_app_rule(SublimeRRule())

#---------------------------------------------------------------------------

class SublimeTeXRule(MergeRule):
    mcontext = AppContext(title=".tex") & AppContext(title="Sublime Text")
    mapping = {
        "go [to] (word | name) <dict>":
            Key("c-r") + Text("%(dict)s") + Key("enter"),
        "count words": Key("cs-c"),

    }
    extras = [
        Dictation("dict"),
    ]
    default = {
        "n": 1,
    }

control.nexus().merger.add_non_ccr_app_rule(SublimeTeXRule())

#---------------------------------------------------------------------------