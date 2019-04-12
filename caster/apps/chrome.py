from dragonfly import (Grammar, Dictation, Repeat, Choice, Clipboard, Function, IntegerRef)
from caster.lib.actions import Key, Text, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib import control

from caster.lib.merge.mergerule import MergeRule


class ChromeRule(MergeRule):
    pronunciation = "google chrome"

    mapping = { # most keybinds are taken from https://support.google.com/chrome/answer/157179?hl=en
        "[new] incognito window":   Key("cs-n"),
        "new tab [<n>]":            Key("c-t") * Repeat(extra="n"),
        "reopen tab [<n>]":         Key("cs-t") * Repeat(extra="n"),
        "close all tabs":           Key("cs-w"),

        "page back [<n>]":          Key("a-left/20") * Repeat(extra="n"),
        "page forward [<n>]":       Key("a-right/20") * Repeat(extra="n"),
        "zoom in [<n>]":            Key("c-plus/20") * Repeat(extra="n"),
        "zoom out [<n>]":           Key("c-minus/20") * Repeat(extra="n"),
        "zoom reset":               Key("c-0"),
        "refresh":                  Key("c-f5"),
        "switch focus [<n>]":       Key("f6/20") * Repeat(extra="n"),
        "find <dict>": Key("c-f") + Text("%(dict)s"),
        "[find] next match [<n>]":  Key("c-g/20") * Repeat(extra="n"),
        "[find] prior match [<n>]": Key("cs-g/20") * Repeat(extra="n"),
        "[toggle] caret browsing":  Key("f7"),

        "home page":                Key("a-home"),
        "show history":             Key("c-h"),
        "[google] search":          Key("c-l"),
        "show downloads":           Key("c-j"),
        "[add] bookmark":           Key("c-d"),
        "bookmark all tabs":        Key("cs-d"),
        "[toggle] bookmark bar":    Key("cs-b"),
        "show bookmarks":           Key("cs-o"),
        "switch user":              Key("cs-m"),
        "chrome task manager":      Key("s-escape"),
        "[toggle] full-screen":     Key("f11"),
        "focus notification":       Key("a-n"),
        "allow notification":       Key("as-a"),
        "deny notification":        Key("as-a"),

        "developer tools":          Key("f12"),
        "view [page] source":       Key("c-u"),
        "resume":                   Key("f8"),
        "step over":                Key("f10"),
        "step into":                Key("f11"),
        "step out":                 Key("s-f11"),

        "<numberth> tab":
            Key("c-%(numberth)s"),

        "copy all":
            Key("c-a/20, c-c"),

        "go <site>":
            Key("c-l/10") + Text("%(site)s") + Key("del, enter"),
        "search <text>":
            Key("c-l/10") + Text("%(text)s") + Key("enter"),

        "science hub": Key("a-d") + Store() + Key("delete") + Text("https://sci-hub.tw/") + Retrieve() + Key("enter"),

        "split right": Key("w-left/50, W/50, w-right"),

        "google that": Store() + Key("c-t") + Retrieve() + Key("enter"),

        }
    extras = [
        Dictation("dict"),
        Dictation("text"),
        IntegerRef("n", 1, 10),
        Choice("site", {
            "amazon":"smile.amazon.co.uk",
            "exams": "https://www.york.ac.uk/economics/current-students/ug-information/exampapers/#tab-2",
            "facebook":"facebook.com",
            "iPlayer": "https://www.bbc.co.uk/iplayer",
            "math fly": "mathfly.org",
            "scholar":"scholar.google.co.uk",
            "spectator":"spectator.co.uk",
            "times":"thetimes.co.uk",
            "timetable":"timetable.york.ac.uk",
            "twitter":"twitter.com",
            "VLE": "https://vle.york.ac.uk",
            "youtube":"youtube.com",
        }),
        Choice("numberth", {
            "first": "1",
            "second": "2",
            "third": "3",
            "fourth": "4",
            "fifth": "5",
            "sixth": "6",
            "seventh": "7",
            "eighth": "8",
            "(last | ninth)": "9",
            "next":"pgdown",
            "previous":"pgup",
        }),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="chrome")
grammar = Grammar("chrome", context=context)

rule = ChromeRule(name="chrome")
grammar.add_rule(rule)
grammar.load()

class DocsRule(MergeRule):
    mapping = {
        "(insert | edit) link": Key("c-k"),
        "print file": Key("c-p"),
        "find and replace": Key("c-h"),
        "find next": Key("c-g"),
        "find previous": Key("cs-g"),

        "bold text": Key("c-b"),
        "italic text": Key("c-i"),
        "underlined text": Key("c-u"),
        "strikethrough text": Key("as-5"),
        "superscript": Key("c-dot"),
        "subscript": Key("c-comma"),
        "increase font size": Key("cs-rangle"),
        "decrease font size": Key("cs-langle"),

        "normal text style": Key("ca-0"),
        "heading style [<headn>]": Key("ca-%(headn)s"),
        "left align text": Key("cs-l"),
        "centre align text": Key("cs-e"),
        "right align text": Key("cs-r"),
        "justify [align] text": Key("cs-j"),
        "insert numbered list": Key("cs-7"),
        "insert [bulleted] list": Key("cs-8"),

        "move paragraph up": Key("as-up"),
        "move paragraph down": Key("as-down"),

        "(insert | add) comment": Key("ca-m"),
        "open discussion thread": Key("cas-a"),
        "insert footnote": Key("ca-f"),

        "file menu": Key("a-f"),
        "edit menu": Key("a-e"),
        "view menu": Key("a-v"),
        "insert menu": Key("a-i"),
        "format menu": Key("a-o"),
        "tools menu": Key("a-t"),
        "help menu": Key("a-h"),

    }
    extras = [
        IntegerRef("headn", 1, 7),
        ]
    defaults = {"headn": 1}

docscontext = AppContext(title="Google docs")
docsgrammar = Grammar("googledocs", context=docscontext)

rule = DocsRule(name="googledocs")
docsgrammar.add_rule(rule)
docsgrammar.load()
