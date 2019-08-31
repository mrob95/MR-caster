from caster.imports import *

class KindleRule(MergeRule):
	pronunciation = "kindle"
	mcontext = AppContext(title="kindle for PC")

	mapping = {
		"library"                : Key("ca-l"),
		"(show | hide) notebook" : Key("c-b"),
		"(search | find)"        : Key("c-f"),
		"(synchronise | refresh)": Key("f5"),
	}

control.non_ccr_app_rule(KindleRule())
