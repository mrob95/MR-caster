from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/python.toml")

class PythonNon(MergeRule):
    mapping = {

        BINDINGS["template_prefix"] + " <template>":
            Function(execution.template),

        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="python.toml"),

        #------------------------------------------------

        "create setters":
            Function(execution.python_setters),

        BINDINGS["magic_prefix"] + " <umeth>":
            Text("def __%(umeth)s__(self):"),
        BINDINGS["magic_prefix"] + "[<right>] <bmeth>":
            Text("def __%(right)s%(bmeth)s__(self, other):"),
        BINDINGS["magic_prefix"] + " <mmeth>":
            Function(lambda mmeth: Text("def __%s__(%s):" % (mmeth[0], mmeth[1])).execute()),

        BINDINGS["decorator_prefix"] + " <decorator>":
            Text("@") + Alternating("decorator"),

        "try except [<exception>] [error] [<as>]":
            Text("try: ") + Key("enter:2, backspace") + Text("except%(exception)s%(as)s:") + Key("up"),
        "raise [<exception>] [error]":
            Text("raise%(exception)s"),
        "error <exception> [error]":
            Text("%(exception)s"),

        "comment [<comment>]": Text("# %(comment)s"),

        "insert line break": Text("#" + ("-"*48)),
        "insert to do": Text("# TODO: "),

        #------------------------------------------------

        "cheat sheet <module>":
            Function(lambda module: Popen(["SumatraPDF", "C:/Users/Mike/Documents/cheatsheets/python/%s.pdf" % module])),

        "help <fun>":
            Function(lambda fun: utilities.browser_search(fun, url="https://docs.python.org/3/search.html?q=%s")),
        "help <docs>":
            Function(lambda docs: utilities.browser_open(docs)),
        "help that":
            Function(utilities.browser_search, url="https://www.google.com/search?q=python+%s"),
    }
    extras = [
        Dictation("comment", "").capitalize(),
        Choice("module",   BINDINGS["cheatsheets"]),
        Choice("decorator",BINDINGS["decorators"]),
        Choice("template", BINDINGS["templates"]),
        Choice("umeth",    BINDINGS["unary_methods"]),
        Choice("bmeth",    BINDINGS["binary_methods"]),
        Choice("mmeth",    BINDINGS["misc_methods"]),
        Choice("exception",BINDINGS["exceptions"], ""),
        Choice("fun",      BINDINGS["functions"]),
        Choice("docs",     BINDINGS["docs"]),
        Choice("as",       {"as": " as "}, ""),
        Choice("right",    {"right": "r", "eye": "i"}, ""),
    ]

#------------------------------------------------

PYLIBS = utilities.load_toml_relative("config/python_libs.toml")

# Dynamically adds library commands
libs={}
for lib, data in PYLIBS.iteritems():
    pronunciation = data.pop("pronunciation")
    name = data.pop("name") if "name" in data else lib
    libs[pronunciation] = name + " as " + data.pop("import_as") if "import_as" in data else name
    # e.g. "numb pie <numpy_lib>": Alternating("numpy_lib")
    PythonNon.mapping["%s <%s_lib>" % (pronunciation, lib)] = Alternating("%s_lib" % lib)
    PythonNon.extras.append(Choice("%s_lib" % lib, data))
PythonNon.mapping["import <lib>"] = Text("import %(lib)s")
PythonNon.mapping["from <lib> import"] = Text("from %(lib)s import ")
PythonNon.extras.append(Choice("lib", libs))

#------------------------------------------------

class Python(MergeRule):
    non = PythonNon
    mwith = ["Core"]
    mcontext = AppContext(title=BINDINGS["title_contexts"])
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        "<command>":
            Alternating("command"),

        BINDINGS["function_prefix"] + " <fun>":
            ContextAction(Store(same_is_okay=False) + Text("%(fun)s()") + Key("left") + Retrieve(action_if_text="right"),
            [(AppContext(title="jupyter"), Text("%(fun)s()") + Key("left"))]),

        BINDINGS["method_prefix"] + " <fun>":
            Text(".%(fun)s()") + Key("left"),

        "from typing import <types>": Text("from typing import %(types)s"),
        "type <types>"        : Text("%(types)s"),
        "type is <types>"     : Text(": %(types)s"),
        "produces [<types>]"  : Key("end, left") + Text(" -> %(types)s"),

        "method": ContextAction(
            Text("def (self):") + Key("left:7"),
            [(AppContext(title="Sublime Text"), Text("defs") + Key("tab"))]),
        "list comp": ContextAction(
            Text("[ for  in i]") + Key("left:11"),
            [(AppContext(title="Sublime Text"), Text("lc") + Key("tab"))]),

        #------------------------------------------------

        "method [<under>] <snaketext>":
            Text("def %(under)s%(snaketext)s(self):") + Key("left:2"),
        "function <snaketext>":
            Text("def %(snaketext)s():") + Key("left:2"),
        "selfie [<under>] [<snaketext>]":
            Text("self.%(under)s%(snaketext)s"),
        "pointer [<under>] [<snaketext>]":
            Text(".%(under)s%(snaketext)s"),
        "classy [<classtext>]":
            Text("class %(classtext)s:") + Key("left"),

        "<formatting> <text>":
            Function(lambda formatting, text:
                textformat.master_format_text(formatting[0], formatting[1], text)),
    }
    extras = [
        Dictation("snaketext", "").lower().replace(" ", "_"),
        Dictation("classtext", "").title().replace(" ", ""),
        Choice("under", "_", ""),
        Choice("formatting", {
            "(snaky | sneaky)": [5, 3],
            "(singer | title)": [2, 1],
        }),
        Choice("fun",      BINDINGS["functions"]),
        Choice("command",  BINDINGS["commands"]),
        Choice("types",    BINDINGS["types"], ""),
    ]

control.app_rule(Python())

#------------------------------------------------

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
        "<cmisc>": Alternating("cmisc"),

        "go to core [pie]": Key("c-p") + Text("core\n"),
    }
    extras = [
        IntegerRef("intn", 1, 1001),
        Choice("cfun",  CASTER["functions"]),
        Choice("cmisc", CASTER["misc"]),
    ]

control.app_rule(CasterPythonRule())

#------------------------------------------------

class JupyterLabRule(MergeRule):
    mwith = ["Core", "Python"]
    mcontext = AppContext(title="JupyterLab")

    mapping = {
        "next pane [<n>]"          : Key("cs-rbracket:%(n)s"),
        "previous pane [<n>]"      : Key("cs-lbracket:%(n)s"),

        "replace": Key("cs-r"),

        "toggle cyber"              : Key("c-b"),
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

control.app_rule(JupyterLabRule())