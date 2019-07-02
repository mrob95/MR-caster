from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/gitbash.toml")
CORE     = utilities.load_toml_relative("config/core.toml")

def checkout(text):
    Text("git checkout " + text.replace(" ", "_")).execute()
    output = "test" + text
    Text(output).execute()
    Text("git checkout " + text).execute()

class GitBashNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="gitbash.toml"),

        "git fetch pull <prn>": Text("git fetch upstream pull/%(prn)s/head:pr-%(prn)s && git checkout pr-%(prn)s"),

        "git check out <text>":
            # Function(lambda text: Text("git checkout " + text.replace(" ", "_").execute())),
            Text("git checkout %(text)s"),
            # Function(checkout),
    }
    extras = [
        Dictation("text").replace(" ", "_"),
        ShortIntegerRef("prn", 1, 10000),
    ]

class GitBashRule(MergeRule):
    non = GitBashNon
    pronunciation = BINDINGS["pronunciation"]
    mwith = "Core"
    mcontext = AppContext(executable=BINDINGS["executable_contexts"])

    mapping = {
        "<command>": execution.Alternating("command"),

        "go <directory>":
            Text("cd \"%(directory)s\"") + Key("enter"),

        "folder <directory>":
            Text("%(directory)s"),

        "open link":
            Key("c-insert") + Function(lambda: utilities.browser_open(Clipboard.get_system_text())),
    }

    extras = [
        Choice("directory",      CORE["directories"]),
        MultiChoice("command",  [BINDINGS["git_commands"],
                                 BINDINGS["python_commands"],
                                 BINDINGS["r_commands"],
                                 BINDINGS["image_commands"],
                                 BINDINGS["latex_commands"],
                                 BINDINGS["jekyll_commands"],
                                 BINDINGS["general_commands"]]),
    ]

control.app_rule(GitBashRule())