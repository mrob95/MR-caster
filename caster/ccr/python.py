from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/python.toml")

class PythonNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),

    }
    extras = [
        Choice("template", BINDINGS["templates"]),
    ]



class Python(MergeRule):
    non = PythonNon
    mwith = "Core"
    mcontext = AppContext(title=".py")
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        BINDINGS["function_prefix"] + " <fun>":
            Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),

        BINDINGS["method_prefix"] + " init":
            Text("def __init__():") + Key("left:2") + Text("self, "),
        BINDINGS["method_prefix"] + " <umeth>":
            Text("def __%(meth)s__(self):"),
        BINDINGS["method_prefix"] + " <bmeth>":
            Text("def __%(meth)s__(self, other):"),

        "import <lib>": Text("import %(lib)s") + Key("enter"),

    }

    extras = [
        Choice("fun",    BINDINGS["functions"]),
        Choice("umeth",  BINDINGS["unary_methods"]),
        Choice("bmeth",  BINDINGS["binary_methods"]),
        Choice("command",BINDINGS["commands"]),
        Choice("lib",    BINDINGS["libraries"]),
    ]

    defaults = {}

control.nexus().merger.add_app_rule(Python())

#---------------------------------------------------------------------------

class BasePythonRule(MergeRule):
    mwith = ["Core", "Python"]
    mcontext = AppContext(title=".py") & ~AppContext(title="Sublime Text")
    mapping = {
        "function": Text("def ():") + Key("left:2"),
        "method": Text("def (self):") + Key("left:7"),
        "list comprehension": Text("[ for  in i]") + Key("left:11"),
    }

control.nexus().merger.add_app_rule(BasePythonRule())

#---------------------------------------------------------------------------

class SublimePythonRule(MergeRule):
    mwith = ["Core", "Python"]
    mcontext = AppContext(title=".py") & AppContext(title="Sublime Text")
    mapping = {
        "function": Text("def") + Key("tab"),
        "method": Text("defs") + Key("tab"),
        "list comprehension": Text("lc") + Key("tab"),
    }

control.nexus().merger.add_app_rule(SublimePythonRule())

#---------------------------------------------------------------------------

CASTER = utilities.load_toml_relative("config/python_caster.toml")

class CasterPythonRuleNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <ctemplate>":
            Function(lambda ctemplate: execution.template(ctemplate)),
    }
    extras = [
        Choice("ctemplate", CASTER["templates"]),
    ]

class CasterPythonRule(MergeRule):
    non = CasterPythonRuleNon
    mwith = ["Core", "Python"]
    mcontext = AppContext(title=".py") & (AppContext(title="caster") | AppContext(title="mathfly"))
    mapping = {
        "integer ref <intn>": Text("IntegerRef("", 1, %(intn)s),") + Key("left:16"),
        BINDINGS["function_prefix"] + " <cfun>":
            Store(same_is_okay=False) + Text("%(cfun)s()") + Key("left") + Retrieve(action_if_text="right"),
        "<cmisc>":
            Function(lambda cmisc: execution.alternating_command(cmisc)),
    }
    extras = [
        IntegerRef("intn", 1, 1001),
        Choice("cfun", CASTER["functions"]),
        Choice("cmisc", CASTER["misc"]),
    ]

control.nexus().merger.add_app_rule(CasterPythonRule())

#---------------------------------------------------------------------------
