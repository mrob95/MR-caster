from dragonfly import AppContext
from dragonfly.grammar.context import LogicOrContext

from caster.lib import utilities


SETTINGS = utilities.load_toml_relative("config/settings.toml")
# Override dragonfly.AppContext with aenea.ProxyAppContext if the 'use_aenea'
# setting is set to true.
if SETTINGS["use_aenea"]:
    try:
        from aenea import ProxyAppContext as AppContext
    except ImportError:
        print("Unable to import aenea.ProxyAppContext. dragonfly.AppContext "
              "will be used instead.")


# class TitleContext(LogicOrContext):
#     def __init__(self, executables=[], titles=[]):
#         self._children = [AppContext(executable=context)
#                             for context in executables] + \
#                         [AppContext(title=context)
#                             for context in titles]
#         self._str = ", ".join(str(child) for child in self._children)

class TitleContext(LogicOrContext):
    def __init__(self, *args):
        self._children = [AppContext(title=arg) for arg in args]
        self._str = ", ".join(str(child) for child in self._children)

class ExeContext(LogicOrContext):
    def __init__(self, *args):
        self._children = [AppContext(executable=arg) for arg in args]
        self._str = ", ".join(str(child) for child in self._children)
