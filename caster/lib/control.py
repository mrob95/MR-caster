from ctrl.nexus import Nexus
from dragonfly import Grammar

_NEXUS = None

def nexus():
    global _NEXUS
    if _NEXUS is None:
        _NEXUS = Nexus()
    return _NEXUS

def app_rule(rule, context=None):
    nexus().merger.add_app_rule(rule, context=context)

def global_rule(rule):
    nexus().merger.add_global_rule(rule)

def non_ccr_app_rule(rule, context=None):
    if context is not None and rule.get_context() is None: rule.set_context(context)
    grammar = Grammar(str(rule), context=rule.get_context())
    grammar.add_rule(rule)
    if rule.non is not None:
        grammar.add_rule(rule.non())
    grammar.load()

def selfmod_rule(rule):
    nexus().merger.add_selfmod_rule(rule)