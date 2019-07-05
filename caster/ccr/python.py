from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/python.toml")

def setters():
    Store().execute()
    text = re.search(r"self,(.*?)\)", Retrieve.text())
    args = text.group(1).split(",")
    args2 = [x.split("=")[0].strip() for x in args]
    Key("c-enter").execute()
    for arg in args2:
        Text("self.%s = %s\n" % (arg, arg)).execute()

camel = lambda t: t[0] + (t.title().replace(" ", "")[1:] if len(t)>1 else "")

class PythonNon(MergeRule):
    mapping = {
        "cheat sheet <module>":
            Function(lambda module: Popen(["SumatraPDF", "C:/Users/Mike/Documents/cheatsheets/python/%s.pdf" % module])),
            # RunCommand(["SumatraPDF", "C:/Users/Mike/Documents/cheatsheets/python/%(module)s.pdf"]),

        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),

        "create setters":
            Function(setters),

        BINDINGS["magic_prefix"] + " init":
            Text("def __init__():") + Key("left:2") + Text("self, "),
        BINDINGS["magic_prefix"] + " <umeth>":
            Text("def __%(umeth)s__(self):"),
        BINDINGS["magic_prefix"] + " <bmeth>":
            Text("def __%(bmeth)s__(self, other):"),
        BINDINGS["magic_prefix"] + " <mmeth>":
            Function(lambda mmeth: Text("def __%s__(%s):" % (mmeth[0], mmeth[1])).execute()),

        "try except [<exception>] [<as>]":
            Text("try: ") + Key("enter:2, backspace") + Text("except%(exception)s%(as)s:") + Key("up"),

        "insert line break": Text("#" + ("-"*77)),

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
        Choice("as", {"as": " as "}),
    ]
    defaults = {
        "as"       : "",
        "exception": "",
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
    PythonNon.mapping["%s <%s_lib>" % (pronunciation, lib)] = execution.Alternating("%s_lib" % lib)
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
            execution.Alternating("command"),

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
        Dictation("snaketext").replace(" ", "_"),
        Dictation("classtext").title().replace(" ", ""),
        # Dictation("classtext", lambda text: text.title().replace(" ", "")),
        # Dictation("classtext", camel),
        Choice("fun",      BINDINGS["functions"]),
        Choice("command",  BINDINGS["commands"]),
    ]
    defaults = {
        "exception": "",
        "selftext": "",
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

class JupyterPython(MergeRule):
    non = PythonNon
    mwith = "Core"
    mcontext = AppContext(title="jupyter notebook")
    pronunciation = "jupyter python"

    mapping = {
        "<command>":
            execution.Alternating("command"),

        BINDINGS["function_prefix"] + " <fun>":
            Text("%(fun)s()") + Key("left"),

        "method":
            Text("def (self)") + Key("colon/3, left:7"),
        "list comprehension":
            Text("[ for  in i]") + Key("left:11"),

        "(insert | new) cell"       : Key("a-enter"),
        "run cell"                  : Key("c-enter"),
        "(next cell | necker) [<n>]": Key("s-enter:%(n)s"),
        "split cell"                : Key("cs-minus"),

        "indent [<n>]"              : Key("c-rbracket:%(n)s"),
        "outdent [<n>]"             : Key("c-lbracket:%(n)s"),

        "comment line"              : Key("c-slash"),
    }
    extras = [
        IntegerRef("n", 1, 10),
        Choice("fun",      BINDINGS["functions"]),
        Choice("command",  BINDINGS["commands"]),
    ]
    defaults = {
        "exception": "",
        "n": 1,
    }

control.app_rule(JupyterPython())
