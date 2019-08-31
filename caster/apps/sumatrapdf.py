from caster.imports import *

class SumatraPDFRule(MergeRule):
	pronunciation = "SumatraPDF"
	mcontext = AppContext("SumatraPDF")

	mapping = {
		# https://www.sumatrapdfreader.org/manual.html
		"open file"          : Key("c-o"),
		"print file"         : Key("c-p"),

		"close tab"          : Key("c-w"),
		"next tab"           : Key("c-tab"),
		"previous tab"       : Key("cs-tab"),
		"<nth> tab"          : Key("a-%(nth)s"),

		"go to page"         : Key("c-g"),
		"find"               : Key("c-f"),
		"find next"          : Key("f3"),
		"find previous"      : Key("s-f3"),
		"page <ln1>"           : Key("c-g") + Text("%(ln1)s") + Key("enter"),
		"table of contents"  : Key("f12"),

		"fit page"           : Key("c-0"),
		"actual size"        : Key("c-1"),
		"fit width"          : Key("c-2"),
		"fit content"        : Key("c-3"),
		"[view] single page" : Key("c-6"),
		"facing view"        : Key("c-7"),
		"book view"          : Key("c-8"),
		"rotate [right]"     : Key("c-plus"),
		"rotate left"        : Key("c-minus"),
		"presentation [mode]": Key("f11"),
		"full screen"        : Key("s-f11"),
	}

	extras = [
		ShortIntegerRef("ln1", 1, 1000),
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
			})
	]

control.non_ccr_app_rule(SumatraPDFRule())