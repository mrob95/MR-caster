from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/python.toml")

class PythonNon(MergeRule):
    mapping = {
        "cheat sheet <module>":
            Function(lambda module: Popen(["SumatraPDF", "C:/Users/Mike/Documents/cheatsheets/python/%s.pdf" % module])),

        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),

        "create setters":
            Function(execution.python_setters),

        BINDINGS["magic_prefix"] + " <umeth>":
            Text("def __%(umeth)s__(self):"),
        BINDINGS["magic_prefix"] + "[<right>] <bmeth>":
            Text("def __%(right)s%(bmeth)s__(self, other):"),
        BINDINGS["magic_prefix"] + " <mmeth>":
            Function(lambda mmeth: Text("def __%s__(%s):" % (mmeth[0], mmeth[1])).execute()),

        "try except [<exception>] [<as>]":
            Text("try: ") + Key("enter:2, backspace") + Text("except%(exception)s%(as)s:") + Key("up"),

        "insert line break": Text("#" + ("-"*48)),

        "help <fun>":
            Function(lambda fun: utilities.browser_search(fun, url="https://docs.python.org/3/search.html?q=%s")),
        "help that":
            Function(utilities.browser_search, url="https://www.google.com/search?q=python+%s"),
    }
    extras = [
        Choice("module",   BINDINGS["cheatsheets"]),
        Choice("template", BINDINGS["templates"]),
        Choice("umeth",    BINDINGS["unary_methods"]),
        Choice("bmeth",    BINDINGS["binary_methods"]),
        Choice("mmeth",    BINDINGS["misc_methods"]),
        Choice("exception",BINDINGS["exceptions"]),
        Choice("fun",      BINDINGS["functions"]),
        Choice("as",       {"as": " as "}),
        Choice("right",    {"right": "r", "eye": "i"}),
    ]
    defaults = {
        "as"       : "",
        "exception": "",
        "right"    : "",
    }

#---------------------------------------------------------------------------

PYLIBS = utilities.load_toml_relative("config/python_libs.toml")

# Dynamically adds library commands
libs={}
for lib, data in PYLIBS.iteritems():
    pronunciation = data.pop("pronunciation")
    name = data.pop("name") if "name" in data else lib
    libs[pronunciation] = name + " as " + data.pop("import_as") if "import_as" in data else name
    # e.g. "numb pie <numpy_lib>": execution.Alternating("numpy_lib")
    PythonNon.mapping["%s <%s_lib>" % (pronunciation, lib)] = Alternating("%s_lib" % lib)
    PythonNon.extras.append(Choice("%s_lib" % lib, data))
PythonNon.mapping["import <lib>"] = Text("import %(lib)s") + Key("enter")
PythonNon.extras.append(Choice("lib", libs))

#---------------------------------------------------------------------------

class Python(MergeRule):
    non = PythonNon
    mwith = "Core"
    mcontext = AppContext(title=BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Alternating("command"),

        BINDINGS["function_prefix"] + " <fun>":
            Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
        BINDINGS["method_prefix"] + " <fun>":
            Text(".%(fun)s()") + Key("left"),

        "method": ContextAction(
            Text("def (self):") + Key("left:7"),
            [(AppContext(title="Sublime Text"), Text("defs") + Key("tab"))]),
        "list comp": ContextAction(
            Text("[ for  in i]") + Key("left:11"),
            [(AppContext(title="Sublime Text"), Text("lc") + Key("tab"))]),

        "method <snaketext>": Text("def %(snaketext)s(self):") + Key("left:2"),
        "function <snaketext>": Text("def %(snaketext)s():") + Key("left:2"),
        "selfie [<snaketext>]": Text("self.%(snaketext)s"),
        "classy [<classtext>]": Text("class %(classtext)s:") + Key("left"),
    }
    extras = [
        Dictation("snaketext").lower().replace(" ", "_"),
        Dictation("classtext").title().replace(" ", ""),
        Choice("fun",      BINDINGS["functions"]),
        Choice("command",  BINDINGS["commands"]),
    ]
    defaults = {
        "exception": "",
        "snaketext": "",
        "classtext": "",
    }

control.app_rule(Python())

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
    mcontext = AppContext(title=".py") & AppContext(title=["caster", "mathfly"])

    mapping = {
        "integer ref <intn>": Text("IntegerRef("", 1, %(intn)s),") + Key("c-left:3"),
        BINDINGS["function_prefix"] + " <cfun>":
            Store(same_is_okay=False) + Text("%(cfun)s()") + Key("left") + Retrieve(action_if_text="right"),
        "<cmisc>": execution.Alternating("cmisc"),
    }
    extras = [
        IntegerRef("intn", 1, 1001),
        Choice("cfun",  CASTER["functions"]),
        Choice("cmisc", CASTER["misc"]),
    ]

control.app_rule(CasterPythonRule())

#---------------------------------------------------------------------------