'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, IntegerRef, Dictation, Repeat, MappingRule, Playback, Clipboard, Mimic

from caster.lib.actions import Key, Text, Mouse
from caster.lib import control, utilities, navigation, textformat, execution
from caster.lib.merge.mergerule import t

from dragonfly.language.en.characters import element_series_wrap_class
import os
_NEXUS = control.nexus()

SETTINGS = utilities.load_toml_relative("config/settings.toml")
CORE = utilities.load_toml_relative("config/core.toml")
PERSONAL = utilities.load_toml_relative("config/personal.toml")

_LETTERS, _DIRECTIONS = "letters", "directions"
if SETTINGS["alternative_letters"]:
	_LETTERS += "_alt"
if SETTINGS["alternative_directions"]:
	_DIRECTIONS += "_alt"

def alphabet(big, letter):
	if big:
		letter = letter.upper()
	Key(letter).execute()

class coreNon(MappingRule):
    mapping = {
        "external notify": Function(utilities.toast_notify, title="external", message="messageAC test"),


        "super hold":        Key("win:down"),
        "super release":     Key("win:up"),
        "shift hold":        Key("shift:down"),
        "shift release":     Key("shift:up"),
        "control hold":      Key("ctrl:down"),
        "control release":   Key("ctrl:up"),
        "(meta|alt) hold":   Key("alt:down"),
        "(meta|alt) release":Key("alt:up"),
        "all release":       Key("win:up, shift:up, ctrl:up, alt:up"),
        "release all":       Key("win:up, shift:up, ctrl:up, alt:up"),

        "volume up [<n>]": Key("volumeup/5:%(n)d"),
        "volume down [<n>]": Key("volumedown/5:%(n)d"),
        "volume (mute|unmute)": Key("volumemute"),
        "music next": Key("tracknext"),
        "music previous": Key("trackprev"),
        "music (pause|play)": Key("playpause"),

        "context menu": Key("s-f10"),

        "show work [spaces]": Key("w-tab"),
        "(create | new) work [space]": Key("wc-d"),
        "close work [space]": Key("wc-f4"),
        "next work [space] [<n>]": Key("wc-right")*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]": Key("wc-left")*Repeat(extra="n"),

        "go work [space] <n>": Function(lambda n: navigation.go_to_desktop_number(n)),
        "send work [space] <n>": Function(lambda n: navigation.move_current_window_to_desktop(n)),
        "move work [space] <n>": Function(lambda n: navigation.move_current_window_to_desktop(n, True)),
        "send work [space] new": Function(navigation.move_current_window_to_new_desktop, follow=False),
        "move work [space] new": Function(navigation.move_current_window_to_new_desktop, follow=True),
        "close all work [spaces]": Function(navigation.close_all_workspaces),

        "take screenshot": Key("ws-s"),

        "squat": Mouse("left:down"),
        "bench": Mouse("left:up"),
        "kick": Playback([(["mouse", "click"], 0.0)]),
        "shift right click":
            Key("shift:down") + Mouse("right") + Key("shift:up"),
        "colic":
            Key("control:down") + Mouse("left") + Key("control:up"),
        "millick":
            Mouse("middle"),
        "window <direction> [<direction2>]":
            Key("win:down, %(direction)s/15, %(direction2)s, win:up"),
        'minimize':
            Playback([(["minimize", "window"], 0.0)]),
        'maximize':
            Playback([(["maximize", "window"], 0.0)]),
        "configure " + CORE["pronunciation"]: Function(utilities.load_config, config_name="core.toml"),

        "undo [<n>]":
            Key("c-z")*Repeat(extra="n"),
        "redo [<n>]":
            Key("c-y")*Repeat(extra="n"),

        "close all notepads": Function(utilities.kill_notepad),

        "paste as text":
            Function(lambda: Text(Clipboard.get_system_text()).execute()),

        "paste as administrator": Function(execution.paste_as_admin),

        "google that":
            Function(utilities.browser_search, site="google"),
        "(wiki | wikipedia) that":
            Function(utilities.browser_search, site="wikipedia"),
        "google <dict>":
            Function(lambda dict: utilities.browser_search(dict, site="google")),
        "wikipedia <dict>":
            Function(lambda dict: utilities.browser_search(dict, site="wikipedia")),

        "open terminal":
            Function(lambda: utilities.terminal("C:/Users/Mike/Documents")),

        "<misc_core_keys_noCCR>": Key("%(misc_core_keys_noCCR)s"),

        }
    extras = [
        Dictation("dict"),
        IntegerRef("n", 1, 20),
        Choice("direction", CORE[_DIRECTIONS]),
        Choice("direction2", CORE[_DIRECTIONS]),
        Choice("misc_core_keys_noCCR", CORE["misc_core_keys_noCCR"]),
    ]
    defaults = {
        "n": 1,
        "direction2": "",
    }

class core(t):
    non = coreNon

    pronunciation = CORE["pronunciation"]

    mapping = {
    	"[<big>] <letter>": Function(alphabet),
    	# CORE["numbers_prefix"] + " <numbers>": Text("%(numbers)s"),
        CORE["numbers_prefix"] + " <wnKK> [<wnKK2>] [<wnKK3>] [<wnKK4>] [<wnKK5>]":
            Text("%(wnKK)s" + "%(wnKK2)s" + "%(wnKK3)s" + "%(wnKK4)s" + "%(wnKK5)s"),

    	"<punctuation>": Key("%(punctuation)s"),

        "(<direction> | <modifier> [<direction>]) [(<nnavi50> | <extreme>)]":
            Function(navigation.text_nav),

    	"<key> [<n>]": Key("%(key)s")*Repeat(extra="n"),

        'tabby [<tabdir>] [<nnavi10>]':
            Key("%(tabdir)s" + "tab")*Repeat(extra="nnavi10"),
        "splat [<splatdir>] [<nnavi10>]":
            Key("c-%(splatdir)s") * Repeat(extra="nnavi10"),

    	"<misc_core_keys>": Key("%(misc_core_keys)s"),

        CORE["dictation_prefix"] + " <text> [brunt]":
            Function(textformat.master_format_text, capitalization=0, spacing=0),

        "(shift click | shifty)": Key("shift:down") + Mouse("left") + Key("shift:up"),

        "stoosh [<nnavi500>]":
            Function(navigation.stoosh, nexus=_NEXUS),
        "cutter [<nnavi500>]":
            Function(navigation.stoosh, nexus=_NEXUS, key="x"),
        "duple [<nnavi50>]":
            Function(navigation.duple),


        "spark [<nnavi500>] [(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel)]":
            Function(navigation.drop, nexus=_NEXUS),

        "(<capitalization> <spacing> | <capitalization> | <spacing>) (bow|bowel) <text>":
            Function(textformat.master_format_text),
        "hug <enclosure>":
            Function(navigation.enclose_selected),

        "<personal>": Text("%(personal)s"),

    	}

    extras = [
        Dictation("text"),
    	IntegerRef("n", 1, 10),
        IntegerRef("wnKK", 0, 10),
        IntegerRef("wnKK2", 0, 10),
        IntegerRef("wnKK3", 0, 10),
        IntegerRef("wnKK4", 0, 10),
        IntegerRef("wnKK5", 0, 10),
        IntegerRef("nnavi10", 1, 11),
        IntegerRef("nnavi50", 1, 20),
        IntegerRef("nnavi500", 1, 500),
        Choice("big", {CORE["capitals_prefix"]: True}),
    	Choice("letter", CORE[_LETTERS]),
    	Choice("punctuation", CORE["punctuation"]),
    	Choice("key", CORE["keys"]),
    	Choice("misc_core_keys", CORE["misc_core_keys"]),
    	Choice("direction", CORE[_DIRECTIONS]),
    	Choice("modifier", CORE["modifiers"]),
        Choice("extreme", {CORE["extreme"]: True}),
        Choice("enclosure", CORE["enclosures"]),
        Choice("capitalization", CORE["capitalization"]),
        Choice("spacing", CORE["spacing"]),
        Choice("personal", PERSONAL),
        Choice("splatdir", {
            "ross":"delete",
        }),
        Choice("tabdir", {
            "lease": "s-",
            }),
    ]

    defaults = {
        "big": False,
        "extreme": False,
        "capitalization": 0,
        "spacing": 0,
        "nnavi10": 1,
        "nnavi50": 1,
        "nnavi500": 1,
    	"n": 1,
        "direction": "left",
    	"modifier": "",
        "wnKK2": "",
        "wnKK3": "",
        "wnKK4": "",
        "wnKK5": "",
        "tabdir": "",
        "splatdir": "backspace",
    }


control.nexus().merger.add_global_rule(core())