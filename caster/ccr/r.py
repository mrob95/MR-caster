from dragonfly import Dictation, MappingRule, Choice, Function
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext, TitleContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule
from subprocess import Popen

BINDINGS = utilities.load_toml_relative("config/r.toml")

def rfunc(rf):
    if type(rf) in [str, unicode]:
        action = Store(same_is_okay=False) + Text("%s()" % rf) + Key("left") + Retrieve(action_if_text="right")
    else:
        action = Store(same_is_okay=False) + Text("%s()" % rf[0]) + Key("left") + Retrieve(action_if_text="comma, space") + Text(rf[1]) + Key("left:%s" % rf[2])
    action.execute()

class RlangNon(MergeRule):
    mapping = {
        "<module> cheatsheet":
            Function(lambda module: Popen(["SumatraPDF", "C:/Users/Mike/Documents/cheatsheets/R/%s.pdf" % module])),

        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        BINDINGS["markdown_prefix"] + " <markdown_command>":
            Function(lambda markdown_command:
                execution.alternating_command(markdown_command)),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="r.toml"),
    }
    extras = [
        Choice("template",        BINDINGS["templates"]),
        Choice("markdown_command",BINDINGS["markdown"]),
        Choice("module",          BINDINGS["cheatsheets"]),
    ]

class Rlang(MergeRule):
    non           = RlangNon
    pronunciation = BINDINGS["pronunciation"]
    mwith         = "Core"
    mcontext      = TitleContext(*BINDINGS["title_contexts"])

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        #
        BINDINGS["function_prefix"] + " <function>":
            Function(lambda function: rfunc(function)),
        #
        BINDINGS["graph_prefix"] + " <ggfun>":
            Text("%(ggfun)s()") + Key("left"),

        BINDINGS["model_prefix"] + " <modelargs>":
            Text("%(modelargs)s"),

        # BINDINGS["argument_prefix"] + " <argument>":
            # Text("%(argument)s"),

        BINDINGS["library_prefix"] + " <library>":
            Text("library(%(library)s)") + Key("end"),

    }

    extras = [
        Dictation("text"),
        Choice("command",  BINDINGS["commands"]),
        Choice("function", BINDINGS["r_functions"]),
        Choice("ggfun",    BINDINGS["r_graph"]),
        Choice("argument", BINDINGS["r_args"]),
        Choice("modelargs",BINDINGS["r_model"]),
        Choice("library",  BINDINGS["libraries"]),
    ]
    defaults = {}


control.nexus().merger.add_app_rule(Rlang())