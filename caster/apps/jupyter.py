from dragonfly import (Grammar, Pause, Choice, Function, Mimic, Playback, Repeat, Dictation)
from caster.lib.dfplus.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.dfplus.context import AppContext
from caster.lib.dfplus.integers import IntegerRef, ShortIntegerRef

from caster.lib.merge.mergerule import MergeRule
from caster.lib import control

class JupyterRule(MergeRule):
	pronunciation = "jupyter notebook"
	mcontext = AppContext(title="jupyter notebook")

	mapping = {
		"(insert | new) cell"       : Key("a-enter"),
		"run cell"                  : Key("c-enter"),
		"(next cell | necker) [<n>]": Key("s-enter:%(n)s"),
		"split cell"                : Key("cs-minus"),

		"indent [<n>]"              : Key("c-rbracket:%(n)s"),
		"outdent [<n>]"             : Key("c-lbracket:%(n)s"),

		"show help"                 : Key("s-tab"),
	}

	extras = [
		IntegerRef("n", 1, 10),

	]

	defaults = {
		"n": 1,
	}

control.non_ccr_app_rule(JupyterRule())
