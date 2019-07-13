from caster.imports import *

class VSCodeRule(MergeRule):
    pronunciation = "VSCode"
    mcontext = AppContext(title="Visual Studio Code")

    mapping = {
        "comment block"                  : Key("sa-a"),

        "edit lines"                     : Key("sa-i"),
        "sort lines"                     : Key("f9"),
        "edit next [<n3>]"               : Key("c-d")*Repeat(extra="n3"),
        "skip next [<n3>]"               : Key("c-k, c-d")*Repeat(extra="n3"),
        "edit all"                       : Key("cs-l"),

        "<action> [line] <ln1> [by <ln2>]"  :
            Function(navigation.action_lines),

        "<action> by [line] <ln1>"  :
            Key("c-k, c-space, c-g") + Function(lambda ln1: Text(str(ln1+1)).execute()) + Key("enter, c-k, c-a, %(action)s, c-k, c-g"),

        "new (file | tab)"               : Key("c-n"),
        # {"keys"                        : ["ctrl+alt+n"], "command": "new_window"},
        "new window"                     : Key("cs-n"),
        "open file"                      : Key("c-o"),
        # {"keys"                        : ["ctrl+shift+o"], "command": "prompt_add_folder"},
        "open folder"                    : Key("c-k, c-o"),
        "save as"                        : Key("cs-s"),
        "save all"                        : Key("c-k, s"),
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

        "toggle side bar"                : Key("c-b"),

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

        "configure alignment": Key("f10, p, right, p, right, down, enter"),
    }
    extras = [
        Dictation("dict"),
        ShortIntegerRef("ln1", 1, 1000),
        ShortIntegerRef("ln2", 1, 1000),
        IntegerRef("n2", 1, 9),
        IntegerRef("n3", 1, 21),
        Choice("action", {
            "select": "",
            "copy": "c-c",
            "cut": "c-x",
            "(delete | remove)": "backspace",
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
        "ln2": None,
        "n2": 1,
        "n3": 1,
        "filetype": "",
    }

control.non_ccr_app_rule(VSCodeRule())

#---------------------------------------------------------------------------

class VSCodeCCRRule(MergeRule):
    mwith = ["Core"]
    mcontext = AppContext(title="Visual Studio Code")
    mapping = {
        "line <ln1>"       : Key("c-g") + Text("%(ln1)s") + Key("enter"),
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

        "indent [<n2>]": Key("c-rbracket:%(n2)s"),

        "auto complete": Key("c-space"),

    }
    extras = [
        ShortIntegerRef("ln1", 1, 1000),
        IntegerRef("n2", 1, 9),
        IntegerRef("n11", 1, 20),
        IntegerRef("n12", 0, 10),
        IntegerRef("n13", 0, 10),
    ]
    defaults = {"n12": "", "n13": "", "n2": 1}

control.app_rule(VSCodeCCRRule())

#---------------------------------------------------------------------------
