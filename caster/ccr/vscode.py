from caster.imports import *

def Wait():
    return Pause("50")

def Pallette(command):
    return Key("cs-p") + Wait() + Text(command) + Key("enter")

class VSCodeRule(MergeRule):
    pronunciation = "VSCode"
    mcontext = AppContext(title="Visual Studio Code")

    mapping = {
        "comment block"                  : Key("sa-a"),

        "edit lines"                     : Key("sa-i"),
        "sort lines"                     : Key("f9"),
        "edit next [<n>]"               : Key("c-d")*Repeat("n"),
        "skip next [<n>]"               : Key("c-k, c-d")*Repeat("n"),
        "edit all"                       : Key("cs-l"),

        "<action> [line] <ln1> [by <ln2>]"  :
            Function(navigation.action_lines),

        "<action> by [line] <ln1>"  :
            Key("c-k, c-space, c-g") + Function(lambda ln1: Text(str(ln1+1)).execute()) + Key("enter, c-k, c-a, %(action)s, c-k, c-g"),

        "new (file | tab)"               : Key("c-n"),
        "new window"                     : Key("cs-n"),
        "open file"                      : Key("c-o"),
        "open folder"                    : Key("c-k, c-o"),
        "open recent"                    : Key("c-r"),
        "save as"                        : Key("cs-s"),
        "save all"                       : Key("c-k, s"),
        "revert (file | changes)": Pallette("revert file"),
        "close tab"                      : Key("c-w"),
        "close all tabs"                 : Key("c-k, c-w"),
        "next tab"                       : Key("c-pgdown"),
        "previous tab"                   : Key("c-pgup"),
        "<nth> tab"                      : Key("a-%(nth)s"),
        #
        "find"                           : Key("c-f"),
        "find <text>"                    : Key("c-f") + Wait() + Text("%(text)s") + Key("escape"),
        "find next [<n>]"               : Key("f3")*Repeat("n"),
        "find previous [<n>]"           : Key("s-enter")*Repeat("n"),
        "find all"                       : Key("a-enter"),
        "replace"                        : Key("c-h"),
        #
        "go to <text> [<filetype>]"      : Key("c-p") + Text("%(text)s" + "%(filetype)s") + Wait() + Key("enter"),
        "go to word"                     : Key("c-semicolon"),
        "go to symbol"                   : Key("cs-o"),
        "go to [symbol in] project"      : Key("c-t"),

        "command pallette [<text>]"      : Key("cs-p") + Text("%(text)s"),
        "search in directory"            : Key("cs-f"),
        "go to that"                     : Key("f12"),
        "search [for] that"              : Store() + Key("cs-f") + Retrieve() + Key("enter"),
        "find that"                      : Store() + Key("c-f") + Retrieve() + Key("enter"),
        #
        "fold"                           : Key("cs-lbracket"),
        "unfold"                         : Key("cs-rbracket"),
        "unfold all"                     : Key("c-k, c-j"),
        "fold [level] <n2>"              : Key("c-k, c-%(n2)s"),
        #
        "full screen"                    : Key("f11"),
        "toggle side bar"                : Key("c-b"),
        #
        "build it"                       : Key("c-b"),
        "build with"                     : Key("cs-b"),
        #
        # "record macro"                   : Key("c-q"),
        # "play macro [<n>]"              : Key("cs-q")*Repeat("n"),
        "transform upper": Pallette("uppercase"),
        "transform lower": Pallette("lowercase"),
        "transform title": Pallette("titlecase"),
        #
        "column <cols>"                  : Key("as-%(cols)s"),
        "focus <panel>"                  : Key("c-%(panel)s"),
        "move <panel>"                   : Key("cs-%(panel)s"),
        "split right"                    : Key("c-backslash"),
        #
        "terminal here"                  : Key("cs-c"),
        "open settings": Key("c-comma"),
    }
    extras = [
        ShortIntegerRef("ln1", 1, 1000),
        ShortIntegerRef("ln2", 1, 1000, 0),
        IntegerRef("n2", 1, 9, 1),
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
            }, ""),
    ]

control.non_ccr_app_rule(VSCodeRule())

#------------------------------------------------

class VSCodeCCRRule(MergeRule):
    mwith = ["Core"]
    mcontext = AppContext(title="Visual Studio Code")
    mapping = {
        "line <ln1>"       : Key("c-g") + Wait() + Text("%(ln1)s") + Key("enter"),

        "shunt [<n>]": Key("s-down:%(n)s"),

        "go to file"     : Key("c-p"),
        "comment line"   : Key("c-slash"),

        "(select | sell) scope [<n2>]"   : Key("cs-space")*Repeat("n2"),
        "copy scope"   : Key("cs-space, c-c"),
        "replace scope"   : Key("cs-space, c-v"),

        "indent [<n2>]": Key("c-rbracket:%(n2)s"),

        "auto complete": Key("c-space"),
    }
    extras = [
        ShortIntegerRef("ln1", 1, 1000),
        IntegerRef("n2", 1, 9, 1),
    ]

control.app_rule(VSCodeCCRRule())