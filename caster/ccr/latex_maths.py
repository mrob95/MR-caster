'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/latex.toml")
CORE = utilities.load_toml_relative("config/core.toml")

class LaTeXmath(MergeRule):
    pronunciation = BINDINGS["pronunciation"]  +  " maths"

    mapping = {
        # "<n1> hundred": Text("%(n1)s00"),
        "<numbers1>": Text("%(numbers1)s"),
        "<numbers2>": Text("%(numbers2)s"),
        "<symbol>":  Function(tex_funcs.symbol),
        "<misc_symbol>": Alternating("misc_symbol"),
    }

    extras = [
        IntegerRef("numbers1", 0, 100),
        IntegerRef("n2", 0, 100),
        IntegerRef("numbers2", 100, 1000),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("symbol", BINDINGS["symbols"]),
        Choice("misc_symbol", BINDINGS["misc_symbols"]),
        ]

control.global_rule(LaTeXmath())