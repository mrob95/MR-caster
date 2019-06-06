from dragonfly import Dictation, MappingRule, Choice, IntegerRef, Clipboard, Function
from caster.lib.dfplus.actions import Key, Text, Mouse, Store, Retrieve, MultiChoice
from caster.lib.dfplus.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/gitbash.toml")
CORE     = utilities.load_toml_relative("config/core.toml")

class GitBashNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="gitbash.toml"),
    }

class GitBashRule(MergeRule):
    non = GitBashNon
    pronunciation = BINDINGS["pronunciation"]
    mwith = "Core"
    mcontext = AppContext(executable=BINDINGS["executable_contexts"])

    mapping = {
        "<command>":
            Function(lambda command: execution.alternating_command(command)),

        "go <directory>":
            Text("cd %(directory)s") + Key("enter"),

        "folder <directory>":
            Text("%(directory)s"),

        "(pull request | open link)":
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