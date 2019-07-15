from caster.imports import *

class GitHubRule(MergeRule):
    pronunciation = "github"
    mcontext = AppContext(executable="GitHubDesktop")

    mapping = {
        "new repository": Key("c-n"),
        "add local repository": Key("c-o"),
        "clone repository": Key("c-o"),
        "options": Key("c-comma"),

        "changes": Key("c-1"),
        "history": Key("c-2"),
        "(repositories | repository list)": Key("c-t"),
        "branches [list]": Key("c-b"),

        "zoom in [<n>]": Key("c-equals")*Repeat("n"),
        "zoom out [<n>]": Key("c-minus")*Repeat("n"),
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

control.non_ccr_app_rule(GitHubRule())