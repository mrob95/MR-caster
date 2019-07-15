'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/latex.toml")
CORE     = utilities.load_toml_relative("config/core.toml")

class LaTeXNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="latex.toml"),

        "(open | edit) bibliography":
            Function(utilities.load_text_file, path=BINDINGS["bibliography_path"]),

        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "[<sub>] section <text>":
            Function(tex_funcs.section),
    }
    extras = [
        Choice("sub", {
            "sub": "sub",
            "sub sub": "subsub",
            }, ""),
        Choice("template", BINDINGS["templates"]),
    ]

class LaTeX(MergeRule):
    non = LaTeXNon
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "insert comment":  Text("% "),

        BINDINGS["class_prefix"] + " [<doc_class>]":
            Function(lambda doc_class: tex_funcs.back_curl("documentclass", doc_class)),

        BINDINGS["environment_prefix"] + " <environment>":
            Function(tex_funcs.begin_end),
        "end <environment>":
            Function(lambda environment: tex_funcs.back_curl("end", environment)),
        #
        BINDINGS["package_prefix"] + " [<packopts>]":
            Function(tex_funcs.packages),
        #
        BINDINGS["symbol_prefix"] + " <symbol>":
            Function(tex_funcs.symbol),
        BINDINGS["symbol_prefix"] + " <misc_symbol>":
            execution.Alternating("misc_symbol"),
        BINDINGS["accent_prefix"] + " <accent>":
            Store(same_is_okay=False) + Text("\\%(accent)s{}") + Key("left") + Retrieve(action_if_text="right"),

        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(tex_funcs.greek_letters),
        #
        BINDINGS["command_prefix"] + " <command>":
            Store(same_is_okay=False) + Text("\\%(command)s{}") + Key("left") + Retrieve(action_if_text="right"),
        BINDINGS["command_prefix"] + " <commandnoarg>":
            Text("\\%(commandnoarg)s "),

        BINDINGS["command_prefix"] + " my (bib resource | bibliography)":
            Function(lambda: tex_funcs.back_curl("addbibresource", BINDINGS["bibliography_path"])),

        BINDINGS["command_prefix"] + " quote":
            Function(tex_funcs.quote),
    }

    extras = [
        Boolean("big", CORE["capitals_prefix"]),
        Choice("packopts",    BINDINGS["packages"], default=""),
        Choice("doc_class",   BINDINGS["document_classes"], default=""),
        Choice("greek_letter",BINDINGS["greek_letters"]),
        Choice("symbol",      BINDINGS["symbols"]),
        Choice("misc_symbol", BINDINGS["misc_symbols"]),
        Choice("accent",      BINDINGS["accents"]),
        Choice("commandnoarg",BINDINGS["commandnoarg"]),
        Choice("command",     BINDINGS["command"]),
        Choice("environment", BINDINGS["environments"]),
        ]

control.global_rule(LaTeX())
