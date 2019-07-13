from caster.imports import *

class RuleNameRule(MergeRule):
	pronunciation = "apppronunciation"
	mcontext = AppContext(title="apppronunciation")

	mapping = {
		"open file"     : Key("c-o"),
		"new file"      : Key("c-n"),
		"print file"    : Key("c-p"),

		"close tab"     : Key("c-w"),
		"next tab"      : Key("c-tab"),
		"previous tab"  : Key("cs-tab"),
		"<nth> tab"     : Key("a-%(nth)s"),

		"go to page"    : Key("c-g"),
		"find"          : Key("c-f"),
		"find next"     : Key("f3"),
		"find previous" : Key("s-f3"),
		"page <n>"      : Key("c-g") + Text("%(n)s") + Key("enter"),

		"zoom in [<n>]" : Key("c-equals:%(n)s"),
		"zoom out [<n>]": Key("c-minus:%(n)s"),
	}

	extras = [
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

control.non_ccr_app_rule(RuleNameRule())
