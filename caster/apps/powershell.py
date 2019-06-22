from caster.imports import *

class PowerShellRule(MergeRule):
    pronunciation = "PowerShell"
    mcontext = AppContext(title="PowerShell")

    mapping = {
        "PDF LaTeX"   : Text("pdflatex "),
        "bib TeX"     : Text("bibtex "),
        "python 3"    : Text("python3 .py") + Key("left:3"),
        "python 2"    : Text("python27 .py") + Key("left:3"),
        "python 2 pip": Text("python27 -m pip install ") + Key("left:3"),
        "R script"    : Text("Rscript .r") + Key("left:2"),
        "R markdown"  : Text("Rscript -e \"rmarkdown::render('.Rmd', clean=TRUE)\""),
        "dot pie"     : Text(".py"),
        "dot tex"     : Text(".tex"),
        "dot PDF"     : Text(".pdf"),
    }

    extras = [
    ]
    defaults = {
    }

control.non_ccr_app_rule(PowerShellRule())