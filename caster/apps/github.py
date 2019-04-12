from dragonfly import (Grammar, Repeat, Choice, IntegerRef)
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext

from caster.lib.merge.mergerule import MergeRule

class GitHubRule(MergeRule):
    pronunciation = "github"

    mapping = {
            "new repository": Key("c-n"),
            "add local repository": Key("c-o"),
            "clone repository": Key("c-o"),
            "options": Key("c-comma"),

            "changes": Key("c-1"),
            "history": Key("c-2"),
            "(repositories | repository list)": Key("c-t"),
            "branches [list]": Key("c-b"),

            "zoom in [<n>]": Key("c-equals")*Repeat(extra="n"),
            "zoom out [<n>]": Key("c-minus")*Repeat(extra="n"),
            "reset zoom": Key("c-0"),

            "push [repository]": Key("c-p"),
            "pull [repository]": Key("cs-p"),
            "remove repository": Key("c-delete"),
            "view on github": Key("cs-g"),
            "(terminal | command prompt)": Key("c-backtick"),
            "explorer": Key("cs-f"),
            "edit": Key("cs-a"),

            "new branch": Key("cs-n"),
            "rename branch": Key("cs-r"),
            "delete branch": Key("cs-d"),

            "update from master": Key("cs-u"),
            "compare to branch": Key("cs-b"),
            "merge into current [branch]": Key("cs-m"),

            "compare on github": Key("cs-c"),
            "[create] pull request": Key("c-r"),
        }
    extras = [
        IntegerRef("n", 1, 10),

    ]
    defaults = {"n": 1}


#---------------------------------------------------------------------------

context = AppContext(executable="GitHubDesktop")
grammar = Grammar("GitHubDesktop", context=context)

rule = GitHubRule(name="GitHubDesktop")
grammar.add_rule(rule)
grammar.load()
