from caster.imports import *

class SublimeRule(MergeRule):
    pronunciation = "sublime"
    mcontext = AppContext(title="Sublime Text")

    mapping = {
        "comment block"                  : Key("cs-slash"),
        "convert indentation"            : Key("f10, v, i, up:2, enter"),

        "edit lines"                     : Key("cs-l"),
        "sort lines"                     : Key("f9"),
        "skip next [<n3>]"               : Key("c-k, c-d")*Repeat("n3"),
        "edit all"                       : Key("c-d, a-f3"),
        "reverse selection"              : Key("as-r"),

        "<action> [line] <ln1> [by <ln2>]"  :
            Function(navigation.action_lines),

        "<action> by [line] <ln1>"  :
            Key("c-k, c-space, c-g") + Function(lambda ln1: Text(str(ln1+1)).execute()) + Key("enter, c-k, c-a, %(action)s, c-k, c-g"),

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
        "join lines [<n3>]"              : Key("c-j")*Repeat("n3"),
        "match bracket"                  : Key("c-m"),
        #
        # "(select | sell) all"          : Key("c-a"),
        # {"keys"                        : ["ctrl+alt+p"], "command": "expand_selection_to_paragraph"},
        "(select | sell) paragraph"      : Key("ca-p"),
        # SelectUntil
        "(select | sell) until"          : Key("as-s"),

        "toggle side bar"                : Key("c-k, c-b"),
        "show key bindings"              : Key("f10, p, right, k"),

        #
        "find"                           : Key("c-f"),
        "find <text>"                    : Key("c-f") + Text("%(text)s") + Key("escape"),
        "find next [<n2>]"               : Key("f3")*Repeat("n2"),
        "find previous [<n2>]"           : Key("s-f3")*Repeat("n2"),
        "find all"                       : Key("a-enter"),
        "replace"                        : Key("c-h"),
        #

        "go to <text> [<filetype>]"      : Key("c-p") + Text("%(text)s" + "%(filetype)s") + Key("enter"),
        "go to word"                     : Key("c-semicolon"),
        "go to symbol"                   : Key("c-r"),
        "go to [symbol in] project"      : Key("cs-r"),

        "command pallette [<text>]"      : Key("cs-p") + Text("%(text)s"),
        "search in directory"            : Key("cs-f"),
        # "go to (that | the)"             : Store() + Key("cs-r") + Retrieve() + Key("enter"),
        "go to (that | the)"             : Key("f12"),
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
        "transform upper": Key("c-k, c-u"),
        "transform lower": Key("c-k, c-l"),
        # {"keys"        : ["ctrl+k", "ctrl+t"], "command": "title_case"},
        "transform title": Key("c-k, c-t"),
        #
        "build it"                       : Key("c-b"),
        "build with"                     : Key("cs-b"),
        # "cancel build"                 : Key("c-break")),
        #
        "record macro"                   : Key("c-q"),
        "play macro [<n3>]"              : Key("cs-q")*Repeat("n3"),
        "(new | create) snippet"         : Key("a-n"),
        #
        "close tab"                      : Key("c-w"),
        "close all tabs"                 : Key("f10, f, up:2, enter"),
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
        "explorer here"                  : Key("ca-e"),

        "zoom in [<n2>]"                 : Key("c-equal")*Repeat("n2"),
        "zoom out [<n2>]"                : Key("c-minus")*Repeat("n2"),

        # wrap plus
        "(wrap | split) lines"           : Key("a-q"),

        "paste from history": Key("c-k, c-v"),

        "format table": Key("cas-t"),

        "configure alignment": Key("f10, p, right, p, right, down, enter"),
    }
    extras = [
        ShortIntegerRef("ln1", 1, 1000),
        ShortIntegerRef("ln2", 1, 1000, 0),
        IntegerRef("n2", 1, 9, 1),
        IntegerRef("n3", 1, 21, 1),
        Choice("action", navigation.actions),
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
            "mark [down]" : "md",
            "tech"        : "tex",
            "tommel"      : "toml",
            }, ""),
    ]

control.non_ccr_app_rule(SublimeRule())

#------------------------------------------------

class SublimeCCRRule(MergeRule):
    mwith = ["Core"]
    mcontext = AppContext(title="Sublime Text")
    mapping = {
        "line <ln1>"                     : Key("c-g") + Text("%(ln1)s") + Key("enter"),

        "edit next [<n3>]"               : Key("c-d")*Repeat("n3"),
        "align that"                     : Key("ca-a"),
        "(go to file | good for | good file)": Key("c-p"),
        "comment line"                   : Key("c-slash"),

        "<action> scope [<n2>]"          : Key("cs-space:%(n2)s, %(action)s"),
        "<action> brackets [<n2>]"       : Key("cs-m:%(n2)s, %(action)s"),
        "<action> (indent | indentation)": Key("cs-j, %(action)s"),

        "indent [<n2>]"                  : Key("c-rbracket:%(n2)s"),

        "auto complete"                  : Key("c-space"),
    }
    extras = [
        ShortIntegerRef("ln1", 1, 1000),
        # TestInteger("ln1", 1, 1000),
        IntegerRef("n2", 1, 9, 1),
        IntegerRef("n3", 1, 21, 1),
        Choice("action", navigation.actions),
    ]

control.app_rule(SublimeCCRRule())

#------------------------------------------------

class SublimeRRule(MergeRule):
    mwith = ["Core", "R"]
    mcontext = AppContext(title=".R") & AppContext(title="Sublime Text")
    mapping = {
        "run (line | that) [<n>]":
            Key("cas-r")*Repeat("n"),
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

control.app_rule(SublimeRRule())

#------------------------------------------------

class SublimeTeXRule(MergeRule):
    mcontext = AppContext(title=[".tex", ".md"]) & AppContext(title="Sublime Text")
    mapping = {
        "go [to] (word | name) <text>":
            Key("c-r") + Text("%(text)s") + Key("enter"),
        "count words": Key("cs-c"),
    }

control.non_ccr_app_rule(SublimeTeXRule())