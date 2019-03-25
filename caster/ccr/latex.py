'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Mouse, Repeat, Clipboard, Dictation

from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule
from caster.lib.latex import tex_funcs

BINDINGS = utilities.load_toml_relative("config/latex.toml")
CORE = utilities.load_toml_relative("config/core.toml")

class LaTeXNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="latex.toml"),

        "add <ref_type> to bibliography":
            Function(tex_funcs.selection_to_bib, bib_path=BINDINGS["bibliography_path"]),

        "(open | edit) bibliography":
            Function(utilities.load_text_file, path=BINDINGS["bibliography_path"]),

        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "show word count":
            Function(tex_funcs.word_count_from_string),

        "[<sub>] section <dict>":
            Function(tex_funcs.section),

    }

    extras = [
        Dictation("dict"),
        Choice("sub", {
            "sub": "sub",
            "sub sub": "subsub",
            }),
        Choice("ref_type", {
                "book": "book",
                "link": "link",
                "paper": "paper",
                }),
        Choice("template", BINDINGS["templates"]),
    ]
    defaults = {
        "sub": "",
    }

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
            Function(lambda misc_symbol: execution.alternating_command(misc_symbol)),
        BINDINGS["accent_prefix"] + " <accent>":
            # Function(lambda accent: execution.paren_function("\\" + accent, "{", "}")),
            Store() + Text("\\%(accent)s{}") + Key("left") + Retrieve(action_if_text="right"),

        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(tex_funcs.greek_letters),
        #
        BINDINGS["command_prefix"] + " <command>":
            Store() + Text("\\%(command)s{}") + Key("left") + Retrieve(action_if_text="right"),
        BINDINGS["command_prefix"] + " <commandnoarg>":
            Text("\\%(commandnoarg)s "),

        BINDINGS["command_prefix"] + " my (bib resource | bibliography)":
            Function(lambda: tex_funcs.back_curl("addbibresource", BINDINGS["bibliography_path"])),

        BINDINGS["command_prefix"] + " quote":
            Function(tex_funcs.quote),

    }

    extras = [
        Choice("big", {CORE["capitals_prefix"]: True}),
        Choice("packopts", BINDINGS["packages"]),
        Choice("doc_class", BINDINGS["document_classes"]),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("symbol", BINDINGS["symbols"]),
        Choice("misc_symbol", BINDINGS["misc_symbols"]),
        Choice("accent", BINDINGS["accents"]),
        Choice("commandnoarg", BINDINGS["commandnoarg"]),
        Choice("command", BINDINGS["command"]),
        Choice("environment", BINDINGS["environments"]),
        ]
    defaults = {
        "big": False,
        "packopts": "",
        "doc_class": "",
    }


control.nexus().merger.add_global_rule(LaTeX())
