from dragonfly import (Grammar, Pause, Choice, Function, IntegerRef, Repeat)
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext
from caster.lib.merge.mergerule import MergeRule
from caster.lib import control

class SpotifyRule(MergeRule):
    pronunciation = "Spotify"
    mcontext = AppContext("Spotify")

    mapping = {
        "new playlist"         : Key("c-n"),
        "select all"           : Key("c-a"),
        "deselect items"       : Key("cs-a"),
        "(play | pause)"       : Key("space"),
        "next [track]"         : Key("c-right"),
        "previous [track]"     : Key("c-left"),
        "volume up"            : Key("c-up"),
        "volume down"          : Key("c-down"),
        "(mute | unmute)"      : Key("cs-down"),
        "search"               : Key("c-l"),
        "page back [<n>]"      : Key("a-left:%(n)s"),
        "page forward [<n>]"   : Key("a-right:%(n)s"),
        "preferences"          : Key("c-p"),

        "add to playlist [<n>]": Key("s-f10/10, up:2, right/10, down:%(n)s, enter"),
    }

    extras = [
    	IntegerRef("n", 1, 10),
    ]
    defaults = {
    	"n": 1,

    }

control.non_ccr_app_rule(SpotifyRule())