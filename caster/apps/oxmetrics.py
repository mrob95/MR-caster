from caster.imports import *

class OxMetricsRule(MergeRule):
    pronunciation = "OxMetrics"
    mcontext = AppContext(executable="OxMetrics", title="OxMetrics")

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

control.non_ccr_app_rule(OxMetricsRule())