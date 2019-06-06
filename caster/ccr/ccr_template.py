from dragonfly import Dictation, MappingRule, Choice, Function
from caster.lib.dfplus.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.dfplus.context import AppContext
from caster.lib.dfplus.integers import IntegerRef, ShortIntegerRef

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
    mcontext = AppContext(title=BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            execution.Alternating("command"),

        BINDINGS["function_prefix"] + " <fun>":
            Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
    }

    extras = [
        Choice("command",BINDINGS["commands"]),
        Choice("fun",    BINDINGS["functions"]),
    ]

    defaults = {}


control.app_rule(className())
