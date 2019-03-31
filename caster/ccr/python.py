from dragonfly import Dictation, MappingRule, Choice, Function
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/python.toml")

class PythonNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),

        "test test": Text(" seater successful"),
    }
    extras = [
        Choice("template", BINDINGS["templates"]),
    ]



class Python(MergeRule):
    non = PythonNon
    mwith = "Core"

    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        BINDINGS["function_prefix"] + " <fun>":
            Store() + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),

        BINDINGS["method_prefix"] + " <meth>":
            Text("def __%(meth)s__():") + Key("left:2") + Text("self, "),
    }

    extras = [
        Choice("fun",    BINDINGS["functions"]),
        Choice("meth",   BINDINGS["methods"]),
        Choice("command",BINDINGS["commands"]),
    ]

    defaults = {}


# control.nexus().merger.add_global_rule(Python())
context = AppContext(title=".py")
control.nexus().merger.add_app_rule(Python(), context=context)
