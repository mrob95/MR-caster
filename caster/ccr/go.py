'''
Created on , 2018

@author: Mike Roberts
'''
from dragonfly import Choice, Function
from caster.lib.actions import Key, Text, Mouse
from caster.lib.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

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
            Function(execution.alternating_command),

        BINDINGS["type_prefix"] + " <type>":
            Text("%(type)s"),
    }

    extras = [
        Choice("type", BINDINGS["types"]),
        Choice("command", BINDINGS["commands"]),
    ]

    defaults = {
    }



control.nexus().merger.add_app_rule(Go())
