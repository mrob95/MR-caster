from dragonfly import Dictation, MappingRule, Choice, IntegerRef, Function
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext, TitleContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule
import re

BINDINGS = utilities.load_toml_relative("config/python.toml")

def test(arg):
    Text(arg).execute()

def setters():
    Store().execute()
    text = re.search(r"self,(.*?)\)", Retrieve.text())
    args = text.group(1).split(",")
    args2 = [x.split("=")[0].strip() for x in args]
    Key("c-enter").execute()
    for arg in args2:
        Text("self.%s = %s\n" % (arg, arg)).execute()

class PythonNon(MergeRule):
    mapping = {
        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),

        "create setters":
            Function(setters),

        BINDINGS["method_prefix"] + " init":
            Text("def __init__():") + Key("left:2") + Text("self, "),
        BINDINGS["method_prefix"] + " <umeth>":
            Text("def __%(umeth)s__(self):"),
        BINDINGS["method_prefix"] + " <bmeth>":
            Text("def __%(bmeth)s__(self, other):"),
        BINDINGS["method_prefix"] + " <mmeth>":
            Function(lambda mmeth: Text("def __%s__(%s):" % (mmeth[0], mmeth[1])).execute()),

        "import <lib>":
            Text("import %(lib)s") + Key("enter"),

        "try except [<exception>]":
            Text("try: ") + Key("enter:2, backspace") + Text("except%(exception)s:") + Key("up"),
        "try except <exception> as":
            Text("try:") + Key("enter:2, backspace") + Text("except%(exception)s as :") + Key("left"),

        "insert line break": Text("#---------------------------------------------------------------------------"),

        "help <fun>":
            Function(lambda fun: utilities.browser_search(fun, url="https://docs.python.org/3/search.html?q=%s")),
        "help that":
            Function(utilities.browser_search, url="https://www.google.com/search?q=python+%s"),

    }
    extras = [
        Choice("test", {
                "success": "success",
                "failure": "failure",
            }),
        Choice("template", BINDINGS["templates"]),
        Choice("umeth",    BINDINGS["unary_methods"]),
        Choice("bmeth",    BINDINGS["binary_methods"]),
        Choice("mmeth",    BINDINGS["misc_methods"]),
        Choice("exception",BINDINGS["exceptions"]),
        Choice("fun",      BINDINGS["functions"]),
    ]
    defaults = {
        "exception": "",
    }

PYLIBS = utilities.load_toml_relative("config/python_libs.toml")

# Dynamically adds library commands
libs={}
for lib, data in PYLIBS.iteritems():
    pronunciation = data.pop("pronunciation")
    if "name" in data:
        name = data.pop("name")
    else:
        name = lib
    if "import_as" in data:
        libs[pronunciation] = "%s as %s" % (name, data.pop("import_as"))
    else:
        libs[pronunciation] = name
    command = "%s <%s_lib>" % (pronunciation, lib)
    action = Function(eval("lambda %s_lib: execution.alternating_command(%s_lib)" % (lib, lib)))
    PythonNon.mapping[command] = action
    choice = Choice("%s_lib" % lib, data)
    PythonNon.extras.append(choice)
PythonNon.extras.append(Choice("lib", libs))

#---------------------------------------------------------------------------


class Python(MergeRule):
    non = PythonNon
    mwith = "Core"
    mcontext = TitleContext(*BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Function(execution.alternating_command),

        BINDINGS["function_prefix"] + " <fun>":
            Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),

    }

    extras = [
        Choice("fun",      BINDINGS["functions"]),
        Choice("command",  BINDINGS["commands"]),
    ]

    defaults = {
        "exception": "",
    }

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
        "integer ref <intn>": Text("IntegerRef("", 1, %(intn)s),") + Key("c-left:3"),
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
