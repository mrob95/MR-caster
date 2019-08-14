from caster.imports import *

BRING = utilities.load_toml_relative("config/bringme.toml")
CORE  = utilities.load_toml_relative("config/core.toml")

current_directory = lambda: Window.get_foreground().title

class WERule(MergeRule):
    pronunciation = "explorer"
    mcontext = AppContext(executable="explorer")

    mapping = {
        "address bar"                        : Key("a-d"),
        "new folder"                         : Key("cs-n"),
        "new file"                           : Key("a-f, w, t"),
        "[(show | file | folder)] properties": Key("a-enter"),
        "go up [<n>]"                        : Key("a-up:%(n)s"),
        "go back [<n>]"                      : Key("a-left:%(n)s"),
        "go forward [<n>]"                   : Key("a-right:%(n)s"),

        "go <folder>":
            Key("a-d/10") + Text("%(folder)s") + Key("enter"),

        "follow <letter_rep>":
            Text("%(letter_rep)s") + Key("enter"),

        # "terminal here"                      : Key("f6:5, s-f10, g, down, enter"),
        "terminal here":
            Function(lambda: utilities.terminal(current_directory().replace("\\", "/"))),
        "new window"                         :
             Function(lambda: Popen(["explorer", current_directory()])),
        "sublime here"                       :
             Function(lambda: Popen(["subl", "-n", current_directory()])),
    }
    extras = [
        Choice("folder", BRING["folder"]),
        Modifier(Repetition(Choice("", CORE["letters_alt"]), 1, 5, "letter_rep"), lambda r: "".join(r)),
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

        "follow <letter_rep>":
            Text("%(letter_rep)s") + Key("enter"),
    }
    extras = [
        Choice("folder", BRING["folder"]),
        Modifier(Repetition(Choice("", CORE["letters_alt"]), 1, 5, "letter_rep"), lambda r: "".join(r)),
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