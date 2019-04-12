'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, IntegerRef

from caster.lib import control, execution, utilities
from caster.lib.merge.mergerule import MergeRule
from caster.lib.latex import tex_funcs

BINDINGS = utilities.load_toml_relative("config/latex.toml")
CORE = utilities.load_toml_relative("config/core.toml")


class LaTeXmath(MergeRule):
    pronunciation = BINDINGS["pronunciation"]  +  " maths"

    mapping = {
        # "<n1> hundred": Text("%(n1)s00"),
        "<numbers1>": Text("%(numbers1)s"),
        "<numbers2>": Text("%(numbers2)s"),
        "<symbol>":  Function(tex_funcs.symbol),
        "<misc_symbol>":
            Function(lambda misc_symbol: execution.alternating_command(misc_symbol)),
    }

    extras = [
        IntegerRef("numbers1", 0, 100),
        IntegerRef("n2", 0, 100),
        IntegerRef("numbers2", 100, 1000),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("symbol", BINDINGS["symbols"]),
        Choice("misc_symbol", BINDINGS["misc_symbols"]),
        ]
    defaults = {
    }


control.nexus().merger.add_global_rule(LaTeXmath())
