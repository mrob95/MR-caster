from ctrl.nexus import Nexus

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
    nexus().merger.add_non_ccr_app_rule(rule, context=context)

def selfmod_rule(rule):
    nexus().merger.add_selfmod_rule(rule)