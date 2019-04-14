from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext, TitleContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/language_name.toml")

class classNameNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="language_name.toml"),
    }
    extras = [
        Choice("template", BINDINGS["templates"]),
    ]

class className(MergeRule):
    non = classNameNon
    mwith = "Core"
    mcontext = TitleContext(*BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        BINDINGS["function_prefix"] + " <fun>":
            Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
    }

    extras = [
        Choice("fun",    BINDINGS["functions"]),
        Choice("command",BINDINGS["commands"]),
    ]

    defaults = {}


control.nexus().merger.add_app_rule(className())
