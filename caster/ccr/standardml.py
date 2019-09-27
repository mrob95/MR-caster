from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/standardml.toml")

class SMLNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="standardml.toml"),
    }
    extras = [
        Choice("template", BINDINGS["templates"]),
    ]

class SML(MergeRule):
    non = SMLNon
    mwith = "Core"
    mcontext = AppContext(title=BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Alternating("command"),

        BINDINGS["function_prefix"] + " <fun>":
            Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
    }

    extras = [
        Choice("command",BINDINGS["commands"]),
        Choice("fun",    BINDINGS["functions"]),
    ]

control.app_rule(SML())
