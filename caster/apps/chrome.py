from caster.imports import *

BRING = utilities.load_toml_relative("config/bringme.toml")

class ChromeRule(MergeRule):

    pronunciation = "google chrome"
    mcontext = AppContext(executable="chrome")

    mapping = { # most keybinds are taken from https://support.google.com/chrome/answer/157179?hl=en

        "[new] incognito window"  : Key("cs-n"),
        "new tab [<n>]"           : Key("c-t:%(n)s"),
        "next tab [<n>]"          : Key("c-tab:%(n)s"),
        "previous tab [<n>]"      : Key("cs-tab:%(n)s"),
        "close tab [<n>]"         : Key("c-w/5:%(n)s"),
        "reopen tab [<n>]"        : Key("cs-t:%(n)s"),
        "<numberth> tab"          : Key("c-%(numberth)s"),

        "page back [<n>]"         : Key("a-left:%(n)s"),
        "page forward [<n>]"      : Key("a-right:%(n)s"),

        "zoom reset"              : Key("c-0"),
        "refresh"                 : Key("c-f5"),
        "switch focus [<n>]"      : Key("f6:%(n)s"),
        "find <text>"             : Key("c-f/20") + Text("%(text)s"),
        "[find] next match [<n>]" : Key("c-g:%(n)s"),
        "[find] prior match [<n>]": Key("cs-g:%(n)s"),
        "[toggle] caret browsing" : Key("f7"),

        "home page"               : Key("a-home"),
        # "show history"            : Key("c-h"),
        "show history"            : Key("c-t") + Text("chrome://history/\n"),
        "[google] search"         : Key("c-l"),
        "show downloads"          : Key("c-j"),
        "[add] bookmark"          : Key("c-d"),
        "bookmark all tabs"       : Key("cs-d"),
        "[toggle] bookmark bar"   : Key("cs-b"),
        "show bookmarks"          : Key("cs-o"),
        "switch user"             : Key("cs-m"),
        "chrome task manager"     : Key("s-escape"),
        "[toggle] full-screen"    : Key("f11"),
        "focus notification"      : Key("a-n"),
        "allow notification"      : Key("as-a"),
        "deny notification"       : Key("as-a"),

        "developer tools"         : Key("f12"),
        "view [page] source"      : Key("c-u"),
        "resume"                  : Key("f8"),
        "step over"               : Key("f10"),
        "step into"               : Key("f11"),
        "step out"                : Key("s-f11"),

        "copy all"                : Key("c-a/20, c-c"),

        "go <site>":
            Key("c-l/10") + Text("%(site)s") + Key("enter"),

        "search <text>":
            Key("c-l/10") + Text("%(text)s") + Key("enter"),

        "science hub":
            # Key("a-d") + Store() + Key("delete") + Text("https://sci-hub.tw/") + Retrieve() + Key("enter"),
            Key("c-l/10, left/10") + Text("https://sci-hub.tw/") + Key("enter"),

        "save image": Function(utilities.chrome_save_image),

        #------------------------------------------------
        # Modeless navigation
        # map <a-w> moveTabToNewWindow
        # map <a-m> toggleMuteTab
        # map <a-r> goToRoot
        # map <a-i> focusInput
        # map <a-u> duplicateTab
        # map <a-t> closeTabsOnRight
        # map <a-l> closeTabsOnLeft
        # map <a-left> scrollLeft
        # map <a-right> scrollRight

        # "split right"       : Key("w-left/50, a-w/50, w-right"),
        # "toggle mute"       : Key("a-m"),
        # "duplicate tab"     : Key("a-u"),
        # "show links"        : Key("c-comma"),
        # "go to root"        : Key("a-r"),
        # "focus input"       : Key("a-i"),
        # "close tabs right"  : Key("a-t"),
        # "close tabs left"   : Key("a-l"),
        # "scroll left [<n>]" : Key("a-left:%(n)s"),
        # "scroll right [<n>]": Key("a-right:%(n)s"),

        #------------------------------------------------
        # Surfing
        "(toggle) surfing keys": Key("a-s"),
        "split right"       : Key("w-left/50, W/50, w-right"),
        "duplicate tab"     : Key("y, t"),
        "go to root"        : Key("g, U"),
        "scroll left [<n>]" : Key("h:%(n)s"),
        "scroll right [<n>]": Key("l:%(n)s"),

        "copy current url":
            Function(lambda: Clipboard.set_system_text(utilities.chrome_get_url())),
    }
    extras = [
        Choice("site", BRING["website"]),
        Choice("numberth", {
            "first"         : "1",
            "second"        : "2",
            "third"         : "3",
            "fourth"        : "4",
            "fifth"         : "5",
            "sixth"         : "6",
            "seventh"       : "7",
            "eighth"        : "8",
            "(last | ninth)": "9",
            "next"          :"pgdown",
            "previous"      :"pgup",
        }),
    ]

control.non_ccr_app_rule(ChromeRule())

#------------------------------------------------

class DocsRule(MergeRule):
    mcontext = AppContext(title="Google docs")

    mapping = {
        "(insert | edit) link"   : Key("c-k"),
        "print file"             : Key("c-p"),
        "find and replace"       : Key("c-h"),
        "find next"              : Key("c-g"),
        "find previous"          : Key("cs-g"),

        "bold text"              : Key("c-b"),
        "italic text"            : Key("c-i"),
        "underlined text"        : Key("c-u"),
        "strikethrough text"     : Key("as-5"),
        "superscript"            : Key("c-dot"),
        "subscript"              : Key("c-comma"),
        "increase font size"     : Key("cs-rangle"),
        "decrease font size"     : Key("cs-langle"),

        "normal text style"      : Key("ca-0"),
        "heading style [<headn>]": Key("ca-%(headn)s"),
        "left align text"        : Key("cs-l"),
        "centre align text"      : Key("cs-e"),
        "right align text"       : Key("cs-r"),
        "justify [align] text"   : Key("cs-j"),
        "insert numbered list"   : Key("cs-7"),
        "insert [bulleted] list" : Key("cs-8"),

        "move paragraph up"      : Key("as-up"),
        "move paragraph down"    : Key("as-down"),

        "(insert | add) comment" : Key("ca-m"),
        "open discussion thread" : Key("cas-a"),
        "insert footnote"        : Key("ca-f"),

        "file menu"              : Key("a-f"),
        "edit menu"              : Key("a-e"),
        "view menu"              : Key("a-v"),
        "insert menu"            : Key("a-i"),
        "format menu"            : Key("a-o"),
        "tools menu"             : Key("a-t"),
        "help menu"              : Key("a-h"),
    }
    extras = [
        IntegerRef("headn", 1, 7, 1),
    ]

control.non_ccr_app_rule(DocsRule())