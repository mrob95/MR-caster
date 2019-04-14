from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext, TitleContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/sql.toml")

class SQLNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="sql.toml"),
    }
    extras = [
        Choice("template", BINDINGS["templates"]),
    ]

class SQL(MergeRule):
    non = SQLNon
    mwith = "Core"
    mcontext = TitleContext(*BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        BINDINGS["logical_prefix"] + "<logical>":
            Text("%(logical)s"),


        BINDINGS["function_prefix"] + " <fun>":
            Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
    }

    extras = [
        Choice("fun",    BINDINGS["functions"]),
        Choice("command",BINDINGS["commands"]),
        Choice("logical",BINDINGS["logicals"]),
    ]

    defaults = {}


control.nexus().merger.add_app_rule(SQL())
