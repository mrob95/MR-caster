from dragonfly import (Grammar, Pause, Choice, Function, IntegerRef, Mimic, Clipboard)
from caster.lib.actions import Key, Text
from caster.lib.context import AppContext

from caster.lib.merge.mergerule import MergeRule


class GitBashRule(MergeRule):
    pronunciation = "GitBash"

    mapping = {
        "paste": Function(lambda: Text(Clipboard.get_system_text().replace("\n", "")).execute()),
        "CD up":           Text("cd ..") + Key("enter"),
        "CD":              Text("cd "),
        "list":            Text("ls") + Key("enter"),
        "make directory":  Text("mkdir "),
        "to file":         Text(" > "),
        "PDF LaTeX":       Text("pdflatex "),
    	"bib TeX":         Text("bibtex "),
    	"python 3":        Text("python3 .py") + Key("left:3"),
    	"python 2":        Text("python27 .py") + Key("left:3"),
        "python 2 pip [install]":    Text("python27 -m pip install ") + Key("left:3"),
    	"R script":        Text("Rscript .r") + Key("left:2"),
    	"R markdown":      Text("Rscript -e \"rmarkdown::render('.Rmd', clean=TRUE)\"") + Key("left:19"),

        "pan doc":         Text("pandoc  -o ") + Key("left:4"),
        "pan doc beamer":  Text("pandoc  -t beamer -o ") + Key("left:14"),

    	"dot pie":         Text(".py"),
    	"dot tex":         Text(".tex"),
    	"dot PDF":         Text(".pdf"),

        "jekyll serve watch": Text("jekyll serve --watch"),
        "jekyll build": Text("jekyll build"),
        "jekyll": Text("jekyll"),

        "image [magic] trim": Text("convert  -fuzz 1% -trim +repage ") + Key("left:24"),

		"git base":        Text("git "),
        "git clone":       Text("git clone "),
        "git clone github":Text("git clone https://github.com/.git") + Key("left:4"),
        "git init":        Text("git init"),
        "git add":         Text("git add "),
        "git add all":         Text("git add -A"),
		"git checkout":    Text("git checkout "),
        "git checkout develop":    Text("git checkout develop") + Key("enter"),
        "git checkout master":    Text("git checkout master") + Key("enter"),
        "git checkout upstream develop":    Text("git checkout upstream/develop") + Key("enter"),
        "git (checkout branch | new branch)":    Text("git checkout -b "),
        "git (branch delete | delete branch)":    Text("git branch -d "),
        "git branch":      Text("git branch "),
        "git branch set upstream [to]":
            Text("git branch --set-upstream-to="),
        "git remote":      Text("git remote "),
        "git merge":       Text("git merge "),
        "git merge tool":  Text("git mergetool"),
        "git fetch":       Text("git fetch "),
        "git fetch upstream":       Text("git fetch upstream"),
        "git push":        Text("git push "),
        "git push set upstream [origin]":        Text("git push --set-upstream origin "),
        "git pull":        Text("git pull "),
        "git status":      Text("git status") + Key("enter"),
        "git commit":      Text("git commit -m \"\"") + Key("left"),
        "git commit all":      Text("git commit -a -m \"\"") + Key("left"),
        "git remote add origin": Text("git remote add origin "),
        "git hub": Text("https://github.com/"),

        "git bug fix commit <n>": Mimic("git", "commit") + Text("fixes #%(n)d ") + Key("backspace"),

        "git reference commit <n>": Mimic("git", "commit") + Text("refs #%(n)d ") + Key("backspace"),

        "undo [last] commit | git reset soft head":
        	Text("git reset --soft HEAD~1"),

        "(undo changes | git reset hard)":
        	Text("git reset --hard"),

        "stop tracking [file] | git remove":
        	Text("git rm --cached "),
        "preview remove untracked | git clean preview":
        	Text("git clean -nd"),

        "remove untracked | git clean untracked":
        	Text("git clean -fd"),
        "git visualize":           Text("gitk"),
        "git visualize file":      Text("gitk -- PATH"),
        "git visualize all":       Text("gitk --all"),
        "git stash":               Text("git stash"),
        "git stash list":          Text("git stash list"),
        "git stash branch":        Text("git stash branch NAME"),
        "git cherry pick":         Text("git cherry-pick "),
        "git (abort cherry pick | cherry pick abort)":
        	Text("git cherry-pick --abort"),
        "git (GUI | gooey)":       Text("git gui"),
        "git blame":               ("git blame PATH -L FIRSTLINE,LASTLINE"),
        "git gooey blame":         Text("git gui blame PATH"),
        "search recursive":        Text("grep -rinH \"PATTERN\" *"),
        "search recursive count":  Text("grep -rinH \"PATTERN\" * | wc -l"),
        "search recursive filetype":Text("find . -name \"*.java\" -exec grep -rinH \"PATTERN\" {} \\;"),


    }

    extras = [
    	IntegerRef("n", 1, 10),
    ]
    defaults = {
    	"n": 1,
    }



context = AppContext(executable="\\sh.exe")
context2 = AppContext(executable="\\bash.exe")
context3 = AppContext(executable="\\cmd.exe")
context4 = AppContext(executable="\\mintty.exe")

grammar = Grammar("MINGW32", context=(context | context2 | context3 | context4))
rule = GitBashRule()
grammar.add_rule(GitBashRule(name="GitBash"))
grammar.load()
