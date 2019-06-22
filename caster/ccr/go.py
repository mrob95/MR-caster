'''
Created on , 2018

@author: Mike Roberts
'''
from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/go.toml")

class GoNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Text("%(template)s"),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="go.toml"),
    }

    extras = [
        Choice("template", BINDINGS["templates"]),
    ]

class Go(MergeRule):
    non = GoNon
    mwith = "Core"
    mcontext = AppContext(title=".go")
    mapping = {
        "<command>":
            execution.Alternating("command"),

        BINDINGS["type_prefix"] + " <type>":
            Text("%(type)s"),
    }

    extras = [
        Choice("type", BINDINGS["types"]),
        Choice("command", BINDINGS["commands"]),
    ]

    defaults = {
    }



control.app_rule(Go())
