from caster.imports import *
from caster.ccr.python import Python, PythonNon
import copy

Key = SlowKey
Text = SlowText
Alternating = SlowAlternating

BINDINGS = utilities.load_toml_relative("config/python.toml")

def setters():
    Store().execute()
    text = re.search(r"self,(.*?)\)", Retrieve.text())
    args = text.group(1).split(",")
    args2 = [x.split("=")[0].strip() for x in args]
    Key("end, enter").execute()
    for arg in args2:
        Text("self.%s = %s\n" % (arg, arg)).execute()

class JupyterNon(PythonNon):
    mapping = {
        "cheat sheet <module>":
            Function(lambda module: Popen(["SumatraPDF", "C:/Users/Mike/Documents/cheatsheets/python/%s.pdf" % module])),

        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),

        "create setters":
            Function(setters),

        BINDINGS["magic_prefix"] + " <umeth>":
            Text("def __%(umeth)s__(self):"),
        BINDINGS["magic_prefix"] + "[<right>] <bmeth>":
            Text("def __%(right)s%(bmeth)s__(self, other):"),
        BINDINGS["magic_prefix"] + " <mmeth>":
            Function(lambda mmeth: Text("def __%s__(%s):" % (mmeth[0], mmeth[1])).execute()),

        "try except [<exception>] [<as>]":
            Text("try: ") + Key("enter:2, backspace") + Text("except%(exception)s%(as)s:") + Key("up"),

        "insert line break": Text("#" + ("-"*77)),

        "help <fun>":
            Function(lambda fun: utilities.browser_search(fun, url="https://docs.python.org/3/search.html?q=%s")),
        "help that":
            Function(utilities.browser_search, url="https://www.google.com/search?q=python+%s"),

        #------------------------------------------------

        "find": Key("escape, f"),
    }

#------------------------------------------------

PYLIBS = utilities.load_toml_relative("config/python_libs.toml")

# Dynamically adds library commands
libs={}
for lib, data in PYLIBS.iteritems():
    pronunciation = data.pop("pronunciation")
    name = data.pop("name") if "name" in data else lib
    libs[pronunciation] = name + " as " + data.pop("import_as") if "import_as" in data else name
    # e.g. "numb pie <numpy_lib>": execution.Alternating("numpy_lib")
    JupyterNon.mapping["%s <%s_lib>" % (pronunciation, lib)] = Alternating("%s_lib" % lib)
    JupyterNon.extras.append(Choice("%s_lib" % lib, data))
JupyterNon.mapping["import <lib>"] = Text("import %(lib)s") + Key("enter")
JupyterNon.extras.append(Choice("lib", libs))

#------------------------------------------------

class Jupyter(Python):
    non = JupyterNon
    mwith = "Core"
    mcontext = AppContext(title="jupyter notebook")
    pronunciation = "jupyter python"
    mapping = {
        "<command>":
                Alternating("command"),

        "method <snaketext>": Text("def %(snaketext)s(self):") + Key("left:2"),
        "function <snaketext>": Text("def %(snaketext)s():") + Key("left:2"),
        "selfie [<snaketext>]": Text("self.%(snaketext)s"),
        "classy [<classtext>]": Text("class %(classtext)s:") + Key("left"),

        #-------------------------------------------------

        BINDINGS["function_prefix"] + " <fun>":
            Text("%(fun)s()") + Key("left"),

        "method":
            Text("def (self):") + Key("left:7"),
        "list comprehension":
            Text("[ for  in ]") + Key("left:10"),

        "(insert | new) cell"       : Key("a-enter"),
        "run cell"                  : Key("c-enter"),
        "(next cell | necker) [<n>]": Key("s-enter:%(n)s"),
        "split cell"                : Key("cs-minus"),
        "[insert] cell above"       : Key("escape, a"),
        "[insert] cell below"       : Key("escape, b"),
        "merge below"               : Key("escape, M"),
        "merge above"               : Key("escape, s-up, M"),
        "toggle line numbers"       : Key("escape, L"),
        "delete cell [<n>]"         : Key("escape, d, d")*Repeat("n"),
        "select all"                : Key("c-a"),

        "indent [<n>]"              : Key("c-rbracket:%(n)s"),
        "outdent [<n>]"             : Key("c-lbracket:%(n)s"),

        "comment line"              : Key("c-slash"),
        "command pallette"          : Key("cs-p"),
    }
    extras = list(Python.extras)
    defaults = Python.defaults.copy()

control.app_rule(Jupyter())
