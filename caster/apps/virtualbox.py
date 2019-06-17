from dragonfly import (Grammar, Pause, Choice, Function, IntegerRef, Mimic, Playback, Repeat, ShortIntegerRef)
from caster.lib.dfplus.actions import Key, Text
from caster.lib.dfplus.context import AppContext

from caster.lib.merge.mergerule import MergeRule
from caster.lib import control

class VirtualBoxRule(MergeRule):
	pronunciation = "virtualbox"
	mcontext = AppContext(title="virtualbox")

	mapping = {
		"kill window [<n>]"     : Key("ws-q:%(n)s"),
		"terminal"      : Key("w-enter"),
		"dee menu"      : Key("w-d"),
		"browser"      : Key("w-f2"),
		"worker <n>"     : Key("w-%(n)s"),
		"transfer worker <n>"     : Key("ws-%(n)s"),

	}

	extras = [
		IntegerRef("n", 1, 10),
		Choice("nth", {
			"first"         : "1",
			"second"        : "2",
			"third"         : "3",
			"fourth"        : "4",
			"fifth"         : "5",
			"sixth"         : "6",
			"seventh"       : "7",
			"eighth"        : "8",
			"(last | final)": "9",
			}),
	]

	defaults = {
		"n": 1,
	}

control.non_ccr_app_rule(VirtualBoxRule())
