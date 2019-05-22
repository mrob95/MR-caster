from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext, TitleContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/shell.toml")

class ShellNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="shell.toml"),
    }
    extras = [
        Choice("template", BINDINGS["templates"]),
    ]

class Shell(MergeRule):
    non = ShellNon
    mwith = "Core"
    mcontext = AppContext(title=BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        # BINDINGS["function_prefix"] + " <fun>":
            # Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
    }

    extras = [
        Choice("command",BINDINGS["commands"]),
        # Choice("fun",    BINDINGS["functions"]),
    ]

    defaults = {}


control.app_rule(Shell())
