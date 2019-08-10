from caster.imports import *

BRING = utilities.load_toml_relative("config/bringme.toml")

def new_window():
    Key("a-d/100").execute()
    _, path = utilities.read_selected(True)
    # Key("escape").execute()
    Popen(["explorer", path])

class WERule(MergeRule):
    pronunciation = "explorer"
    mcontext = AppContext(executable="explorer")

    mapping = {
        "address bar"                        : Key("a-d"),
        "new window"                         : Function(new_window),
        "new folder"                         : Key("cs-n"),
        "new file"                           : Key("a-f, w, t"),
        "[(show | file | folder)] properties": Key("a-enter"),
        "go up [<n>]"                        : Key("a-up:%(n)s"),
        "go back [<n>]"                      : Key("a-left:%(n)s"),
        "go forward [<n>]"                   : Key("a-right:%(n)s"),

        "go <folder>":
            Key("a-d/10") + Text("%(folder)s") + Key("enter"),

        # "terminal here"                      : Key("f6:5, s-f10, g, down, enter"),
        "terminal here":
            Key("a-d/20") + Store() + Key("escape/20") + Function(lambda: utilities.terminal(Retrieve.text())),
        "new window"                         :
            Key("a-d:50") + Store() + Key("escape:50") + Function(lambda: Popen(["explorer", Retrieve.text() + "/"])),
        "sublime here"                       :
            Key("a-d:50") + Store() + Key("escape:50") + Function(lambda: Popen(["subl", Retrieve.text() + "/"])),
    }
    extras = [
        Choice("folder", BRING["folder"]),
    ]

control.non_ccr_app_rule(WERule())

#------------------------------------------------

class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"
    mwith = "Core"
    mcontext = AppContext(title=["save", "open", "select", "choose directory"])

    mapping = {
        "go up [<n>]"        : Key("a-up:%(n)s"),
        "go back [<n>]"      : Key("a-left:%(n)s"),
        "go forward [<n>]"   : Key("a-right:%(n)s"),
        "(files | file list)": Key("a-d, f6:3"),
        "navigation [pane]"  : Key("a-d, f6:2"),
        "file name [<text>]" : Key("a-d, f6:5") + Text("%(text)s"),

        "go <folder>":
            Key("a-d/10") + Text("%(folder)s") + Key("enter"),

        "dot <ext>"          : Text(".%(ext)s"),
    }
    extras = [
        Choice("folder", BRING["folder"]),
        Choice("ext", {
            "batch"         : "bat",
            "(hyper | HTML)": "html",
            "git ignore"    : "gitignore",
            "mark [down]"   : "md",
            "PDF"           : "pdf",
            "(pie | python)": "py",
            "R"             : "R",
            "R mark [down]" : "Rmd",
            "shell"         : "sh",
            "tech"          : "tex",
            "text"          : "txt",
            "tommel"        : "toml",
            "yammel"        : "yml",
        }),
    ]

control.app_rule(FileDialogueRule())