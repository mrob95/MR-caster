from dragonfly import Dictation, MappingRule, Choice, Function
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/r.toml")

class RlangNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        BINDINGS["markdown_prefix"] + " <markdown_command>":
            Function(lambda markdown_command:
                execution.alternating_command(markdown_command)),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="r.toml"),
    }
    extras = [
        Choice("template", BINDINGS["templates"]),
        Choice("markdown_command", BINDINGS["markdown"]),
    ]

class Rlang(MergeRule):
    non = RlangNon
    pronunciation = BINDINGS["pronunciation"]
    mwith = "Core"
    mcontext = AppContext(title=".r") | AppContext(title=".R")| AppContext(title="RStudio") | AppContext(title="Rterm")

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        #
        BINDINGS["function_prefix"] + " <function>":
            Store() + Text("%(function)s()") + Key("left") + Retrieve(action_if_text="right"),
        #
        BINDINGS["graph_prefix"] + " <ggfun>":
            Text("%(ggfun)s()") + Key("left"),

        BINDINGS["model_prefix"] + " <modelargs>":
            Text("%(modelargs)s"),

        # BINDINGS["argument_prefix"] + " <argument>":
            # Text("%(argument)s"),

        BINDINGS["library_prefix"] + " <library>":
            Text("library(%(library)s)") + Key("end, enter"),

    }

    extras = [
        Dictation("text"),
        Choice("command", BINDINGS["commands"]),
        Choice("function", BINDINGS["r_functions"]),
        Choice("ggfun", BINDINGS["r_graph"]),
        Choice("argument", BINDINGS["r_args"]),
        Choice("modelargs", BINDINGS["r_model"]),
        Choice("library", BINDINGS["libraries"]),
    ]
    defaults = {}


control.nexus().merger.add_app_rule(Rlang())