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
    mcontext = AppContext(title=".py")
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        BINDINGS["function_prefix"] + " <fun>":
            Store() + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),

        BINDINGS["method_prefix"] + " init":
            Text("def __init__():") + Key("left:2") + Text("self, "),
        BINDINGS["method_prefix"] + " <umeth>":
            Text("def __%(meth)s__(self):"),
        BINDINGS["method_prefix"] + " <bmeth>":
            Text("def __%(meth)s__(self, other):"),
    }

    extras = [
        Choice("fun",    BINDINGS["functions"]),
        Choice("umeth",  BINDINGS["unary_methods"]),
        Choice("bmeth",  BINDINGS["binary_methods"]),
        Choice("command",BINDINGS["commands"]),
    ]

    defaults = {}

control.nexus().merger.add_app_rule(Python())
