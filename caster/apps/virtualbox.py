from caster.imports import *

class VirtualBoxRule(MergeRule):
	pronunciation = "virtualbox"
	mcontext = AppContext(title="virtualbox")

	mapping = {
		"kill window [<n>]"  : Key("ws-q:%(n)s"),
		"terminal"           : Key("w-enter"),
		"dee menu"           : Key("w-d"),
		"browser"            : Key("w-f2"),
		"worker <n>"         : Key("w-%(n)s"),
		"transfer worker <n>": Key("ws-%(n)s"),
	}

control.non_ccr_app_rule(VirtualBoxRule())
