from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef
from caster.lib.actions import Key, Text, Mouse
from caster.lib.context import AppContext, TitleContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/markdown.toml")

class MarkdownNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="markdown.toml"),
    }

    extras = [
        Choice("template", BINDINGS["templates"]),
    ]


class Markdown(MergeRule):
    non = MarkdownNon
    mwith = "Core"
    mcontext = TitleContext(*BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]
    mapping = {
        "heading [<num>] [<dict>]":
                Function(lambda num, dict:
                    Text(("#" * num) + " " + str(dict).capitalize()).execute()),
        "subheading [<dict>]":
            Function(lambda num, dict:
                Text(("#" * 2) + " " + str(dict).capitalize()).execute()),

        BINDINGS["insert_prefix"] + " <element>":
            Key("%(element)s"),

        BINDINGS["insert_prefix"] + " <command>":
            Function(execution.alternating_command),

        BINDINGS["output_prefix"] + " <output>":
            Text("%(output)s"),

        BINDINGS["option_prefix"] + " <option>":
            Text("%(option)s"),

        "table row <n>":
            Function(lambda n: Text("|"*(n-1)).execute()) + Key("home"),
        "table (break | split) <n>":
            Function(lambda n: Text("---|"*(n-1) + "---").execute()) + Key("enter"),
    }

    extras = [
        Dictation("dict"),
        IntegerRef("num", 1, 7),
        IntegerRef("n", 1, 12),
        Choice("element", BINDINGS["elements"]),
        Choice("output", BINDINGS["outputs"]),
        Choice("option", BINDINGS["options"]),
        Choice("command", BINDINGS["alternating"]),
    ]

    defaults = {
        "dict": "",
        "num": 1,
    }

control.nexus().merger.add_app_rule(Markdown())