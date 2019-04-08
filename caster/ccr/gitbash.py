from dragonfly import Dictation, MappingRule, Choice, Function, IntegerRef, Clipboard
from caster.lib.actions import Key, Text, Mouse, Store, Retrieve
from caster.lib.context import AppContext

from caster.lib import control, utilities, execution
from caster.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/gitbash.toml")

class GitBashNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="gitbash.toml"),
    }

class GitBashRule(MergeRule):
    non = GitBashNon
    pronunciation = BINDINGS["pronunciation"]
    mwith = "Core"
    mcontext = AppContext(executable="\\sh.exe") | AppContext(executable="\\bash.exe") | AppContext(executable="\\cmd.exe") | AppContext(executable="\\mintty.exe")

    mapping = {
        "<general_command>":
            Function(lambda general_command: execution.alternating_command(general_command)),
        "<git_command>":
            Function(lambda git_command: execution.alternating_command(git_command)),
        "<latex_command>":
            Function(lambda latex_command: execution.alternating_command(latex_command)),
        "<python_command>":
            Function(lambda python_command: execution.alternating_command(python_command)),
        "<r_command>":
            Function(lambda r_command: execution.alternating_command(r_command)),
        "<jekyll_command>":
            Function(lambda jekyll_command: execution.alternating_command(jekyll_command)),
        "<image_command>":
            Function(lambda image_command: execution.alternating_command(image_command)),

        "(pull request | open link)":
            Key("c-insert") + Function(lambda: utilities.browser_open(Clipboard.get_system_text())),
    }

    extras = [
        Choice("git_command",    BINDINGS["git_commands"]),
        Choice("python_command", BINDINGS["python_commands"]),
        Choice("r_command",      BINDINGS["r_commands"]),
        Choice("image_command",  BINDINGS["image_commands"]),
        Choice("latex_command",  BINDINGS["latex_commands"]),
        Choice("jekyll_command", BINDINGS["jekyll_commands"]),
        Choice("general_command",BINDINGS["general_commands"]),
    ]

control.nexus().merger.add_app_rule(GitBashRule())