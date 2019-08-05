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
        "heading [<num>] [<capitalised_text>]":
            Text("#")*Repeat("num") + Text(" %(capitalised_text)s"),
        "subheading [<capitalised_text>]":
            Text("## %(capitalised_text)s"),

        BINDINGS["insert_prefix"] + " <element>":
            Key("%(element)s"),

        BINDINGS["insert_prefix"] + " <command>":
            execution.Alternating("command"),

        BINDINGS["output_prefix"] + " <output>":
            Text("%(output)s"),

        BINDINGS["option_prefix"] + " <option>":
            Text("%(option)s"),

        "remark <remarks>":
            execution.Alternating("remarks"),

        "table row <n>":
            Function(lambda n: Text("|"*(n-1)).execute()) + Key("home"),
        "table (break | split) <n>":
            Function(lambda n: Text("---|"*(n-1) + "---").execute()) + Key("enter"),

        "insert link": Function(execution.markdown_link),

        "insert [<language>] code block":
            Text("```%(language)s```") + Key("left:3, enter:2, up"),
    }
    extras = [
        Dictation("capitalised_text", "").capitalize(),
        IntegerRef("num", 1, 7, 1),
        Choice("element", BINDINGS["elements"]),
        Choice("output",  BINDINGS["outputs"]),
        Choice("option",  BINDINGS["options"]),
        Choice("remarks",  BINDINGS["remarks"]),
        Choice("language",BINDINGS["languages"], ""),
        Choice("command", BINDINGS["alternating"]),
    ]

control.app_rule(Markdown())