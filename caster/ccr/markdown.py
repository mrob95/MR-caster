from caster.imports import *

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
    mcontext = AppContext(title=BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]
    mapping = {
        "heading [<num>] [<text>]":
                Function(lambda num, text:
                    Text(("#" * num) + " " + text.capitalize()).execute()),
        "subheading [<text>]":
            Function(lambda num, text:
                Text(("#" * 2) + " " + text.capitalize()).execute()),

        BINDINGS["insert_prefix"] + " <element>":
            Key("%(element)s"),

        BINDINGS["insert_prefix"] + " <command>":
            execution.Alternating("command"),

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
        Dictation("text"),
        IntegerRef("num", 1, 7),
        Choice("element", BINDINGS["elements"]),
        Choice("output", BINDINGS["outputs"]),
        Choice("option", BINDINGS["options"]),
        Choice("command", BINDINGS["alternating"]),
    ]
    defaults = {
        "text": "",
        "num": 1,
    }

control.app_rule(Markdown())