from caster.imports import *

_NEXUS = control.nexus()

SETTINGS = utilities.load_toml_relative("config/settings.toml")
CORE     = utilities.load_toml_relative("config/core.toml")
PERSONAL = utilities.load_toml_relative("config/personal.toml")
LATEX    = utilities.load_toml_relative("config/latex.toml")

class CoreNon(MergeRule):
    mapping = {
        "configure " + CORE["pronunciation"]:
            Function(utilities.load_config, config_name="core.toml"),

        #-----------------------------------------------
        # Mouse

        "copy mouse position":
            Function(lambda: Clipboard.set_system_text("[%d, %d]" % get_cursor_position())),
        "squat"              : Mouse("left:down"),
        "bench"              : ContextAction(Mouse("left:up"), [(AppContext("ShellExperienceHost.exe"), Mouse("left:up/100") + Function(utilities.save_clipboard_image))]),
        "kick"               : Mouse("left"),
        "shift right click"  : Key("shift:down") + Mouse("right") + Key("shift:up"),
        "colic"              : Key("control:down") + Mouse("left") + Key("control:up"),
        "millick"            : Mouse("middle"),

        #-----------------------------------------------
        # Keys
        "undo [<n>]": ContextAction(Key("c-z:%(n)s"),
            [(AppContext(title="emacs"), Key("c-slash")*Repeat("n"))]),
        "redo [<n>]": Key("c-y:%(n)s"),

        "<misc_core_keys_noCCR>": Key("%(misc_core_keys_noCCR)s"),

        "context menu"        : Key("s-f10"),

        "volume up [<n>]"     : Key("volumeup/5:%(n)d"),
        "volume down [<n>]"   : Key("volumedown/5:%(n)d"),
        "volume (mute|unmute)": Key("volumemute"),
        "music next [<n>]"    : Key("tracknext/5:%(n)d"),
        "music previous [<n>]": Key("trackprev/5:%(n)d"),
        "music (pause|play)"  : Key("playpause"),

        "zoom in [<n>]"       : Key("c-equal:%(n)s"),
        "zoom out [<n>]"      : Key("c-minus:%(n)s"),
        #-----------------------------------------------
        # Window management
        "window <direction> [<direction2>]":
            Key("win:down, %(direction)s/15, %(direction2)s, win:up"),
        "minimize":
            Function(lambda: Window.get_foreground().minimize()),
        "maximize":
            Function(lambda: Window.get_foreground().maximize()),
        "close window":
            Key("a-f4"),

        "show work [spaces]"         : Key("w-tab"),
        "(create | new) work [space]": Key("wc-d"),
        "close work [space]"         : Key("wc-f4"),
        "next work [space] [<n>]"    : Key("wc-right")*Repeat("n"),
        "(previous | prior) work [space] [<n>]": Key("wc-left")*Repeat("n"),

        "go work [space] <n>":
            Function(lambda n: workspace.go_to_n(n)),
        "send work [space] <n>":
            Function(lambda n: workspace.move_current_to_n(n)),
        "move work [space] <n>":
            Function(lambda n: workspace.move_current_to_n(n, True)),
        "move everything to work [space] <n>":
            Function(workspace.move_desktop_to),
        "send work [space] new":
            Function(workspace.move_current_to_new, follow=False),
        "move work [space] new":
            Function(workspace.move_current_to_new, follow=True),
        "close all work [spaces]":
            Function(workspace.close_all),

        "show window information":
            Function(utilities.windowinfo),

        #-----------------------------------------------
        # Web, misc

        "<search> search that":
            Function(lambda search: utilities.browser_search(url=search)),
        "<search> search <text>":
            Function(lambda search, text: utilities.browser_search(text, url=search)),

        "tiny URL that":
            Function(utilities.tinyurl),

        "show word count": ContextAction(Function(utilities.word_count),
            [(AppContext(".tex"), Function(tex_funcs.word_count_from_string))]),

        "add <ref_type> to bibliography":
            Function(tex_funcs.selection_to_bib, bib_path=LATEX["bibliography_path"]),

        "open diary": Function(utilities.diary),
        "close all notepads": Function(utilities.kill_notepad),

        "open terminal":
            Function(lambda: utilities.terminal("C:/Users/Mike/Documents")),

        "switch to math fly": Function(utilities.mathfly_switch),

        #-----------------------------------------------
        # Clipboard
        "paste as text":
            Function(lambda: Text(Clipboard.get_system_text()).execute()),

        "paste as administrator": Function(execution.paste_as_admin),

        "take screenshot": Key("ws-s"),
        "save clipboard image": Function(utilities.save_clipboard_image),
        "fix clipboard path":
            Function(lambda: Clipboard.set_system_text(Clipboard.get_system_text().replace("\\", "/"))),
    }
    extras = [
        Choice("direction",            CORE["directions_alt"]),
        Choice("direction2",           CORE["directions_alt"], default=""),
        Choice("misc_core_keys_noCCR", CORE["misc_core_keys_noCCR"]),
        Choice("search",               CORE["search"]),
        Choice("ref_type", {
                "book" : "book",
                "link" : "link",
                "paper": "paper",
                }),
    ]

class Core(MergeRule):
    non = CoreNon
    pronunciation = CORE["pronunciation"]

    mapping = {
        # Alphanumeric
    	"[<big>] <letter>":
            Function(lambda big, letter: Key(letter.upper() if big else letter).execute()),

        CORE["numbers_prefix"] + " <num_seq>":
            Text("%(num_seq)s"),

        "[<long>] <punctuation>":
            Function(lambda long, punctuation:
                Key("space, %s, space" % punctuation if long else punctuation)
                .execute()),

        "[<long>] <punctuation2> [<equal>]":
            Function(lambda long, punctuation2, equal:
                Key(("space, " if long else "") +
                punctuation2 + (", =, " if equal else "") +
                (", space" if long else ""))
                .execute()),

        #-----------------------------------------------
        # Keys
        "(<direction> | <modifier> [<direction>]) [(<n> | <extreme>)]":
            Function(navigation.text_nav),

    	"<key> [<n>]": Key("%(key)s")*Repeat("n"),

        "tabby [<tabdir>] [<n>]":
            Key("%(tabdir)s" + "tab")*Repeat("n"),
        "(splat | spat) [<splatdir>] [(<n> | <extreme>)]":
            ContextAction(Function(navigation.splat),
                [(AppContext("notepad"),
                    Function(navigation.splat, manual=True))]),
        "check [<n>]":
            ContextAction(Key("c-enter:%(n)s"),
                [(AppContext(title=["notepad", "scientific notebook", "jupyter"]), Key("end, enter:%(n)s")),
                (AppContext(title="emacs"), Key("a-m, i, j, down")*Repeat("n"))]),

    	"<misc_core_keys>": Key("%(misc_core_keys)s"),
        "(shift click | shifty)":
            Key("shift:down") + Mouse("left") + Key("shift:up"),

        #-----------------------------------------------
        # Text
        CORE["dictation_prefix"] + " <text> [brunt]":
            Function(textformat.master_format_text, capitalisation=0, spacing=0),

        "(<capitalisation> <spacing> | <capitalisation> | <spacing>) (bow|bowel) <text> [brunt]":
            Function(textformat.master_format_text),

        #-----------------------------------------------
        # Clipboard
        "stoosh [<nnavi500>]":
            ContextAction(Function(navigation.stoosh, nexus=_NEXUS),
                [(AppContext(executable=["\\sh.exe", "\\bash.exe", "\\cmd.exe", "\\mintty.exe"]),
                    Function(navigation.stoosh, nexus=_NEXUS, copy_key="c-insert")),
                (AppContext(executable="windowsterminal.exe"),
                    Function(navigation.stoosh, nexus=_NEXUS, copy_key="cs-c"))]),
        "cutter [<nnavi500>]":
            Function(navigation.stoosh, nexus=_NEXUS, copy_key="c-x"),
        "duple [<n>]":
            ContextAction(Function(navigation.duple),
                [(AppContext(title="Sublime Text"), Key("cs-d:%(n)s")),
                (AppContext(title="visual studio code"), Key("sa-down")),
                (AppContext(title="jupyter"), Function(navigation.duple, esc=False)),
                (AppContext(title="pycharm"), Key("c-d:%(n)s")),
                (AppContext(executable=["\\sh.exe", "\\bash.exe", "\\cmd.exe", "\\mintty.exe", "windowsterminal"]), Key(""))]),

        "spark [<nnavi500>] [(<capitalisation> <spacing> | <capitalisation> | <spacing>) (bow|bowel)]":
            ContextAction(Function(navigation.drop, nexus=_NEXUS),
                [(AppContext(executable=["\\sh.exe", "\\bash.exe", "\\cmd.exe", "\\mintty.exe"]),
                    Function(navigation.drop, nexus=_NEXUS, paste_key="s-insert")),
                (AppContext("windowsterminal.exe"),
                    Function(navigation.drop, nexus=_NEXUS, paste_key="cs-v"))]),

        "hug <enclosure>":
            Function(navigation.enclose_selected),

        #-----------------------------------------------

        "<personal>": Text("%(personal)s"),
    	}

    extras = [
        Modifier(Repetition(IntegerRef("", 0, 10), min=1, max=5, name="num_seq"),
            lambda r: "".join(map(str, r))),
        IntegerRef("nnavi500", 1, 500, 1),
        Boolean("big",        CORE["capitals_prefix"]),
        Boolean("extreme",    CORE["extreme"]),
        Boolean("long"),
        Boolean("equal"),
        Choice("letter",         CORE["letters_alt"]),
        Choice("punctuation",    CORE["punctuation"]),
        Choice("punctuation2",   CORE["punctuation2"]),
        Choice("key",            CORE["keys"]),
        Choice("misc_core_keys", CORE["misc_core_keys"]),
        Choice("direction",      CORE["directions_alt"], "left"),
        Choice("modifier",       CORE["modifiers"], ""),
        Choice("enclosure",      CORE["enclosures"]),
        Choice("capitalisation", CORE["capitalisation"], 0),
        Choice("spacing",        CORE["spacing"], 0),
        Choice("personal",       PERSONAL),
        Choice("splatdir", {"ross": "right"}, "left"),
        Choice("tabdir",   {"lease": "s-"}, ""),
    ]

control.global_rule(Core())