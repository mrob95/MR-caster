from dragonfly import (Grammar, Pause, Choice, Function, IntegerRef)
from caster.lib.dfplus.actions import Key, Text
from caster.lib.dfplus.context import AppContext

from caster.lib.merge.mergerule import MergeRule


class PowerShellRule(MergeRule):
    pronunciation = "PowerShell"

    mapping = {
    	"PDF LaTeX": Text("pdflatex "),
    	"bib TeX": Text("bibtex "),
    	"python 3": Text("python3 .py") + Key("left:3"),
    	"python 2": Text("python27 .py") + Key("left:3"),
        "python 2 pip": Text("python27 -m pip install ") + Key("left:3"),
    	"R script": Text("Rscript .r") + Key("left:2"),
    	"R markdown": Text("Rscript -e \"rmarkdown::render('.Rmd', clean=TRUE)\""),
    	"dot pie": Text(".py"),
    	"dot tex": Text(".tex"),
    	"dot PDF": Text(".pdf"),


    }

    extras = [
    ]
    defaults = {
    }


context = AppContext(title="PowerShell")
grammar = Grammar("PowerShell", context=context)
rule = PowerShellRule()
grammar.add_rule(PowerShellRule(name="PowerShell"))
grammar.load()
