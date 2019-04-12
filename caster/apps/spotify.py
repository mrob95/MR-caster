from dragonfly import (Grammar, Pause, Choice, Function, IntegerRef, Repeat)
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext

from caster.lib.merge.mergerule import MergeRule


class SpotifyRule(MergeRule):
    pronunciation = "Spotify"

    mapping = {
		"new playlist": Key("c-n"),
		"select all": Key("c-a"),
		"deselect items": Key("cs-a"),
		"(play | pause)": Key("space"),
		"next [track]": Key("c-right"),
		"previous [track]": Key("c-left"),
		"volume up": Key("c-up"),
		"volume down": Key("c-down"),
		"(mute | unmute)": Key("cs-down"),
		"search": Key("c-l"),
		"page back [<n>]": Key("a-left")*Repeat(extra="n"),
		"page forward [<n>]": Key("a-right")*Repeat(extra="n"),
		"preferences": Key("c-p"),

		"add to playlist [<n>]": Key("s-f10/10, up:2, right/10, down:%(n)s, enter"),
    }

    extras = [
    	IntegerRef("n", 1, 10),
    ]
    defaults = {
    	"n": 1,

    }


context = AppContext("Spotify")
grammar = Grammar("Spotify", context=context)
rule = SpotifyRule()
grammar.add_rule(SpotifyRule(name="Spotify"))
grammar.load()
