from caster.imports import *
from caster.lib.dfplus.recorder import recorder

_NEXUS = control.nexus()

SETTINGS = utilities.load_toml_relative("config/settings.toml")
CORE     = utilities.load_toml_relative("config/core.toml")
PERSONAL = utilities.load_toml_relative("config/personal.toml")
LATEX    = utilities.load_toml_relative("config/latex.toml")

_LETTERS    = "letters_alt" if SETTINGS["alternative_letters"] else "letters"
_DIRECTIONS = "directions_alt" if SETTINGS["alternative_directions"] else "directions"

def windowinfo():
    wd = Window.get_foreground()
    print(wd.title)
    print(wd.executable)

class CoreNon(MergeRule):
    mapping = {

        "start recording": Function(recorder.start_recording),

        "stop recording": Function(recorder.stop_recording),

        "play recording": Function(recorder.execute),

        #-------------------------------------------------

        "configure " + CORE["pronunciation"]:
            Function(utilities.load_config, config_name="core.toml"),

        #-----------------------------------------------

        "copy mouse position":
            Function(lambda: Clipboard.set_system_text("[%d, %d]" % get_cursor_position())),
        "squat"              : Mouse("left:down"),
        "bench"              : Mouse("left:up"),
        "kick"               : Playback([(["mouse", "click"], 0.0)]),
        "shift right click"  : Key("shift:down") + Mouse("right") + Key("shift:up"),
        "colic"              : Key("control:down") + Mouse("left") + Key("control:up"),
        "millick"            : Mouse("middle"),

        #-----------------------------------------------

        "super hold"          : Key("win:down"),
        "super release"       : Key("win:up"),
        "shift hold"          : Key("shift:down"),
        "shift release"       : Key("shift:up"),
        "control hold"        : Key("ctrl:down"),
        "control release"     : Key("ctrl:up"),
        "(meta|alt) hold"     : Key("alt:down"),
        "(meta|alt) release"  : Key("alt:up"),
        "all release"         : Key("win:up, shift:up, ctrl:up, alt:up"),
        "release all"         : Key("win:up, shift:up, ctrl:up, alt:up"),
        "context menu"        : Key("s-f10"),

        "volume up [<n>]"     : Key("volumeup/5:%(n)d"),
        "volume down [<n>]"   : Key("volumedown/5:%(n)d"),
        "volume (mute|unmute)": Key("volumemute"),
        "music next [<n>]"    : Key("tracknext/5:%(n)d"),
        "music previous [<n>]": Key("trackprev/5:%(n)d"),
        "music (pause|play)"  : Key("playpause"),

        #-----------------------------------------------

        "window <direction> [<direction2>]":
            Key("win:down, %(direction)s/15, %(direction2)s, win:up"),
        'minimize': Playback([(["minimize", "window"], 0.0)]),
        'maximize': Playback([(["maximize", "window"], 0.0)]),

        "show work [spaces]"         : Key("w-tab"),
        "(create | new) work [space]": Key("wc-d"),
        "close work [space]"         : Key("wc-f4"),
        "next work [space] [<n>]"    : Key("wc-right")*Repeat("n"),
        "(previous | prior) work [space] [<n>]": Key("wc-left")*Repeat("n"),

        "go work [space] <n>":
            Function(lambda n: navigation.go_to_desktop_number(n)),
        "send work [space] <n>":
            Function(lambda n: navigation.move_current_window_to_desktop(n)),
        "move work [space] <n>":
            Function(lambda n: navigation.move_current_window_to_desktop(n, True)),
        "send work [space] new":
            Function(navigation.move_current_window_to_new_desktop, follow=False),
        "move work [space] new":
            Function(navigation.move_current_window_to_new_desktop, follow=True),
        "close all work [spaces]":
            Function(navigation.close_all_workspaces),

        "show window information":
            Function(windowinfo),

        #-----------------------------------------------

        "<search> that":
            Function(lambda search: utilities.browser_search(url=search)),
        "<search> <text>":
            Function(lambda search, text: utilities.browser_search(text, url=search)),

        "tiny URL that":
            Function(utilities.tinyurl),

        "get word count": ContextAction(Function(utilities.word_count),
            [(AppContext(".tex"), Function(tex_funcs.word_count_from_string))]),

        "add <ref_type> to bibliography":
            Function(tex_funcs.selection_to_bib, bib_path=LATEX["bibliography_path"]),

        "open diary": Function(utilities.diary),
        "close all notepads": Function(utilities.kill_notepad),
        "paste as text":
            Function(lambda: Text(Clipboard.get_system_text()).execute()),

        "paste as administrator": Function(execution.paste_as_admin),

        "open terminal":
            Function(lambda: utilities.terminal("C:/Users/Mike/Documents")),

        "switch to math fly": Function(utilities.mathfly_switch),

        #-----------------------------------------------

        "take screenshot": Key("ws-s"),

        "undo [<n>]": ContextAction(Key("c-z:%(n)s"),
            [(AppContext(title="emacs"), Key("c-slash")*Repeat("n"))]),
        "redo [<n>]": Key("c-y:%(n)s"),

        "<misc_core_keys_noCCR>": Key("%(misc_core_keys_noCCR)s"),
        }
    extras = [
        Choice("direction",            CORE[_DIRECTIONS]),
        Choice("direction2",           CORE[_DIRECTIONS], default=""),
        Choice("misc_core_keys_noCCR", CORE["misc_core_keys_noCCR"]),
        Choice("search", CORE["search"]),
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
    	"[<big>] <letter>":
            Function(lambda big, letter: Key(letter.upper() if big else letter).execute()),

        CORE["numbers_prefix"] + " <num_seq>":
            Function(lambda num_seq: Text("".join([str(i) for i in num_seq])).execute()),

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

        "(<direction> | <modifier> [<direction>]) [(<nnavi50> | <extreme>)]":
            Function(navigation.text_nav),

    	"<key> [<n>]": Key("%(key)s")*Repeat("n"),

        'tabby [<tabdir>] [<nnavi10>]':
            Key("%(tabdir)s" + "tab")*Repeat("nnavi10"),
        "splat [<splatdir>] [(<nnavi10> | <extreme>)]":
            ContextAction(Function(navigation.splat),
                [(AppContext("notepad"),
                    Function(navigation.splat, manual=True))]),
        "check [<n>]":
            ContextAction(Key("c-enter:%(n)s"),
                [(AppContext(title=["notepad", "scientific notebook", "jupyter notebook"]), Key("end, enter:%(n)s")),
                (AppContext(title="emacs"), Key("a-m, i, j, down")*Repeat("n"))]),

    	"<misc_core_keys>": Key("%(misc_core_keys)s"),
        "(shift click | shifty)": Key("shift:down") + Mouse("left") + Key("shift:up"),

        #-----------------------------------------------

        CORE["dictation_prefix"] + " <text> [brunt]":
            Function(textformat.master_format_text, capitalization=0, spacing=0),

        "(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel) <text>":
            Function(textformat.master_format_text),

        #-----------------------------------------------

        "stoosh [<nnavi500>]":
            ContextAction(Function(navigation.stoosh, nexus=_NEXUS),
                [(AppContext(executable=["\\sh.exe", "\\bash.exe", "\\cmd.exe", "\\mintty.exe"]),
                    Function(navigation.stoosh, nexus=_NEXUS, copy_key="c-insert"))]),
        "cutter [<nnavi500>]":
            Function(navigation.stoosh, nexus=_NEXUS, copy_key="c-x"),
        "duple [<nnavi50>]":
            ContextAction(Function(navigation.duple),
                [(AppContext(title="Sublime Text"), Key("cs-d:%(nnavi50)s")),
                (AppContext(title="jupyter notebook"), Function(navigation.duple, esc=False)),
                (AppContext(title="pycharm"), Key("c-d:%(nnavi50)s")),
                (AppContext(executable=["\\sh.exe", "\\bash.exe", "\\cmd.exe", "\\mintty.exe"]), Key(""))]),

        "spark [<nnavi500>] [(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel)]":
            ContextAction(Function(navigation.drop, nexus=_NEXUS),
                [(AppContext(executable=["\\sh.exe", "\\bash.exe", "\\cmd.exe", "\\mintty.exe"]),
                    Function(navigation.drop, nexus=_NEXUS, paste_key="s-insert"))]),

        "hug <enclosure>":
            Function(navigation.enclose_selected),

        #-----------------------------------------------

        "<personal>": Text("%(personal)s"),
    	}

    extras = [
        Repetition(IntegerRef("wnKK", 0, 10), min=1, max=5, name="num_seq"),
        ShortIntegerRefNo8("nnavi10", 1, 11, 1),
        # IntegerRef("nnavi10", 1, 11),
        IntegerRef("nnavi50", 1, 20, 1),
        IntegerRef("nnavi500", 1, 500, 1),
        Boolean("big",        CORE["capitals_prefix"]),
        Boolean("extreme",    CORE["extreme"]),
        Boolean("long"),
        Boolean("equal"),
        Choice("letter",         CORE[_LETTERS]),
        Choice("punctuation",    CORE["punctuation"]),
        Choice("punctuation2",   CORE["punctuation2"]),
        Choice("key",            CORE["keys"]),
        Choice("misc_core_keys", CORE["misc_core_keys"]),
        Choice("direction",      CORE[_DIRECTIONS], "left"),
        Choice("modifier",       CORE["modifiers"], ""),
        Choice("enclosure",      CORE["enclosures"]),
        Choice("capitalization", CORE["capitalization"], 0),
        Choice("spacing",        CORE["spacing"], 0),
        Choice("personal",       PERSONAL),
        Choice("splatdir", {
            "ross": "right",
        }, "left"),
        Choice("tabdir", {
            "lease": "s-",
        }, ""),
    ]

control.global_rule(Core())