from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef
from caster.lib.dfplus.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.dfplus.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/toml.toml")

class TOMLNon(MergeRule):
    mapping = {
        # BINDINGS["template_prefix"] + " <template>":
            # Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="toml.toml"),
    }
    extras = [
        # Choice("template", BINDINGS["templates"]),
    ]

class TOML(MergeRule):
    non = TOMLNon
    mwith = "Core"
    mcontext = AppContext(title=".toml")
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            execution.Alternating("command"),

        "command that":
            Key("end, s-home") + Store() + Key("quote, right:2, space, equal, space, quote") + Retrieve(),

    }

    extras = [
        Choice("command", BINDINGS["commands"]),
    ]

    defaults = {}


control.app_rule(TOML())
