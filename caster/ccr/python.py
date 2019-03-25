from dragonfly import Dictation, MappingRule, Choice, Function
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/python.toml")

class PythonNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),
    }
    extras = [
        Choice("template", BINDINGS["templates"]),
    ]

class Python(MergeRule):
    non = PythonNon
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        BINDINGS["function_prefix"] + " <fun>":
            Store() + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
    }

    extras = [
        Choice("fun", BINDINGS["functions"]),
        Choice("command", BINDINGS["commands"]),
    ]

    defaults = {}


control.nexus().merger.add_global_rule(Python())