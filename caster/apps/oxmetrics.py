from dragonfly import (Grammar, Pause, Choice, Function, IntegerRef)
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext

from caster.lib.merge.mergerule import MergeRule


class OxMetricsRule(MergeRule):
    pronunciation = "OxMetrics"

    mapping = {
    	"open file": Key("c-o"),
    	"graphics": Key("a-g"),
    	"calculator": Key("a-c"),
    	"model": Key("a-y"),
    }

    extras = [
    ]
    defaults = {
    }


context = AppContext(executable="OxMetrics", title="OxMetrics")
grammar = Grammar("OxMetrics", context=context)
rule = OxMetricsRule()
grammar.add_rule(OxMetricsRule(name="OxMetrics"))
grammar.load()
