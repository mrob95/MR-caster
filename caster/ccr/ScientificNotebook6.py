'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/ScientificNotebook6.toml")
CORE = utilities.load_toml_relative("config/core.toml")

#------------------------------------------------

def TeX(symbol):
    return Key("c-space") + Text(symbol) + Key("enter")

def greek(big, greek_letter):
    if big:
        greek_letter = greek_letter.upper()
    Key("c-g, " + greek_letter).execute()

def matrix(rows, cols):
    Key("f10/5, i/5, down:8, enter/50").execute()
    Key(str(rows) + "/50, tab, " + str(cols) + "/50, enter").execute()

class SN6_nested(NestedRule):
    mapping = {
        "[<before>] integral from <sequence1> to <sequence2>":
            [TeX("int") + Key("c-l"),
            Key("right, c-h"), Key("right")],

        "[<before>] definite from <sequence1> to <sequence2>":
            [Key("c-6, right, c-l"),
            Key("right, c-h"), Key("right, c-left, left")],

        "[<before>] differential <sequence1> by <sequence2>":
            [Key("c-f, d"), Key("down, d"), Key("right")],

        "[<before>] sum from <sequence1> to <sequence2>":
            [Key("f10, i, down:11, enter/25, a, enter, f10, i, down:11, enter/25, b, enter") + TeX("sum") + Key("down"),
            Key("up:2"), Key("right")],

        "[<before>] limit from <sequence1> to <sequence2>":
            [Key("f10, i, down:11, enter/25, b, enter") + TeX("lim") + Key("down"),
            TeX("rightarrow"),
            Key("right")],

        "[<before>] argument that <minmax> <sequence1>":
            [Key("f10, i, down:11, enter/25, b, enter") + Text("arg%(minmax)s") + Key("down"),
            Key("right"), None],

        "[<before>] <minmax> by <sequence1>":
            [Key("f10, i, down:11, enter/25, b, enter") + Text("%(minmax)s") + Key("down"),
            Key("right"), None],

        "[<before>] <script1> <singleton1> [<after>]":
            [Key("%(script1)s"), Key("right"), None],

        "[<before>] <script1> <singleton1> <script2> <singleton2> [<after>]":
            [Key("%(script1)s"), Key("right, %(script2)s"), Key("right")],

    }
    extras = [
        Choice("minmax", {
            "(minimum | minimises)": "min",
            "(maximum | maximises)": "max",
            }),
        Choice("script1", {
            "sub": "c-l",
            "super": "c-h",
            }),
        Choice("script2", {
            "sub": "c-l",
            "super": "c-h",
            }),
    ]

class SN6Non(MergeRule):
    mapping = {
        "text <text>":
            Key("c-t") + Function(lambda text: Text(str(text).capitalize()).execute()),
        "<control>":
            Key("%(control)s"),

        BINDINGS["unit_prefix"] + " <units>": Alternating("units"),
    }
    extras = [
        Choice("control", BINDINGS["control"]),
        Choice("units",   BINDINGS["units"]),
    ]


class SN6(MergeRule):
    non = SN6Non
    nested = SN6_nested
    mwith = CORE["pronunciation"]
    mcontext = AppContext(executable="snb")
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        BINDINGS["symbol_prefix"] + " <symbol>":
            TeX("%(symbol)s"),
        #
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(greek),
        BINDINGS["accent_prefix"] + " <accent>":
            Key("%(accent)s"),

        "<misc_sn_keys>":
            Key("%(misc_sn_keys)s"),
        "<misc_sn_text>":
            Text("%(misc_sn_text)s"),

        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers>": Text("%(numbers)s"),

        "<numbers> <denominator>":
            Key("c-slash") + Text("%(numbers)s") + Key("down") + Text("%(denominator)s") + Key("right"),
    }
    extras = [
        IntegerRef("rows",    1, BINDINGS["max_matrix_size"]),
        IntegerRef("cols",    1, BINDINGS["max_matrix_size"]),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Boolean("big", CORE["capitals_prefix"]),
        Choice("greek_letter",   BINDINGS["greek_letters"]),
        Choice("symbol",         BINDINGS["tex_symbols"]),
        Choice("accent",         BINDINGS["accents"]),
        Choice("misc_sn_keys",   BINDINGS["misc_sn_keys"]),
        Choice("misc_sn_text",   BINDINGS["misc_sn_text"]),
        Choice("denominator",    BINDINGS["denominators"]),
    ]

control.app_rule(SN6())
