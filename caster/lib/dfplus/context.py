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
