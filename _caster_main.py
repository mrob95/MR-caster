import logging
logging.basicConfig()

from dragonfly import Function, Grammar, Choice, get_engine

from caster.lib import control, utilities
from caster.lib.merge.mergerule import MergeRule
from caster.lib.merge.mergepair import MergeInf
import os, sys

BASE_PATH = os.path.realpath(__file__).split("\\_caster_main.py")[0].replace("\\", "/")
sys.path.append(BASE_PATH)

# Does all the heavy lifting, importing of rules etc
_NEXUS = control.nexus()
_NEXUS.build(True)

class MainRule(MergeRule):

	mapping = {
        "<enable> <name>": Function(_NEXUS.rule_changer),

        "rebuild caster": Function(_NEXUS.build),
	}
	extras=[
		_NEXUS.generate_ccr_choices("name"),
        Choice("enable", {
            "enable": True,
            "disable": False
        }),
	]

if get_engine()._name == "natlink":
    from caster.lib.dfplus import modes
    MainRule.mapping["reboot dragon"] = Function(utilities.reboot)



grammar = Grammar('general')
main_rule = MainRule()
grammar.add_rule(main_rule)
grammar.load()

# def changeCallback(cbType, args):
#     print(cbType) # 'mic' or 'user'
#     print(args) # 'off',   'on', 'disabled' and 'sleeping'.
