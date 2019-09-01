from caster.imports import *

BINDINGS = utilities.load_toml_relative("config/gitbash.toml")
CORE     = utilities.load_toml_relative("config/core.toml")

def clip_repo():
    clip = Clipboard.get_system_text()
    if clip.startswith("https://github.com"):
        if clip.endswith("/"):
            clip = clip[:-1]
        Text(clip).execute()
        if not clip.endswith(".git"):
            Text(".git").execute()

class GitBashNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="gitbash.toml"),

        "open link":
            Key("c-insert") + Function(lambda: utilities.browser_open(Clipboard.get_system_text())),

        "git fetch pull <prn>": Text("git fetch upstream pull/%(prn)s/head:pr-%(prn)s && git checkout pr-%(prn)s"),

        "git <command> <snake_text>":
            Text("git %(command)s %(snake_text)s"),
    }
    extras = [
        Dictation("snake_text").replace(" ", "_"),
        ShortIntegerRef("prn", 1, 10000),
        Choice("command", {
            "check out" : "checkout",
            "new branch": "checkout -b",
        }),
    ]

class GitBashRule(MergeRule):
    non           = GitBashNon
    pronunciation = BINDINGS["pronunciation"]
    mwith         = "Core"
    mcontext      = AppContext(executable=BINDINGS["executable_contexts"])

    mapping       = {
        "option <alph>": Text(" -%(alph)s "),

        "<command>": Alternating("command"),

        "git <git_command>":
            Text("git ") + Alternating("git_command"),
        "git clone":
            Text("git clone ") + Function(clip_repo) + Text(" "),
        "git remote add":
            Text("git remote add  ") + Function(clip_repo) + Key("home, right:15"),
    }
    extras = [
        Modifier(
            Repetition(
                Choice("", CORE["letters_alt"]),
                1, 4, "alph"),
            lambda r: "".join(r)),
        Choice("command",     BINDINGS["commands"]),
        Choice("git_command", BINDINGS["git_commands"]),
    ]

control.app_rule(GitBashRule())