from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import t

BINDINGS = utilities.load_toml_relative("config/toml.toml")

class TOMLNon(t):
    mapping = {
        # BINDINGS["template_prefix"] + " <template>":
            # Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="toml.toml"),
    }
    extras = [
        # Choice("template", BINDINGS["templates"]),
    ]

class TOML(t):
    non = TOMLNon
    mwith = "Core"
    mcontext = AppContext(title=".toml")
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        # "<command>":
            # Function(execution.alternating_command),

        "command that":
            Key("end, s-home") + Store() + Key("quote, right:2, space, equal, space, quote") + Retrieve(),

    }

    extras = [
        # Choice("command",BINDINGS["commands"]),
    ]

    defaults = {}


control.nexus().merger.add_app_rule(TOML())
