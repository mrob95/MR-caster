from dragonfly import (Grammar, Pause, Choice, Function, IntegerRef, Mimic, Playback, Repeat, ShortIntegerRef)
from caster.lib.dfplus.actions import Key, Text, Mouse
from caster.lib.dfplus.context import AppContext

from caster.lib.merge.mergerule import MergeRule
from caster.lib import control

class KindleRule(MergeRule):
	pronunciation = "kindle"
	mcontext = AppContext(title="kindle for PC")

	mapping = {
		"library": Key("ca-l"),
		"(show | hide) notebook": Key("c-b"),
		"(search | find)": Key("c-f"),
		"(synchronise | refresh)": Key("f5"),


		"zoom in [<n>]" : Key("c-equals:%(n)s"),
		"zoom out [<n>]": Key("c-minus:%(n)s"),
	}

	extras = [
		IntegerRef("n", 1, 10),
	]

	defaults = {
		"n": 1,
	}

control.non_ccr_app_rule(KindleRule())
