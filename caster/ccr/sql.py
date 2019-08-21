from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/sql.toml")

class SQLNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="sql.toml"),

        "limit <n1000>": Text("LIMIT %(n1000)s"),
    }
    extras = [
        ShortIntegerRef("n1000", 1, 10000),
        Choice("template", BINDINGS["templates"]),
    ]

class SQL(MergeRule):
    non = SQLNon
    mwith = "Core"
    mcontext = AppContext(title=BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            execution.Alternating("command"),

        BINDINGS["logical_prefix"] + "<logical>":
            Text("%(logical)s"),


        # BINDINGS["function_prefix"] + " <fun>":
        #     Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
        BINDINGS["function_prefix"] + " <fun>":
            Text("%(fun)s() ") + Key("left:2"),

        "<formatting> <text>":
            Function(lambda formatting, text:
                textformat.master_format_text(formatting[0], formatting[1], text)),
    }

    extras = [
        Choice("fun",    BINDINGS["functions"]),
        Choice("command",BINDINGS["commands"]),
        Choice("logical",BINDINGS["logicals"]),
        Choice("formatting", {
            "(snaky | sneaky)": [5, 3],
            "(singer | title)": [2, 1],
            "yeller"          : [1, 0],
        }),

    ]

control.app_rule(SQL())
