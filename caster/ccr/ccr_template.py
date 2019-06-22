from caster.imports import *

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
