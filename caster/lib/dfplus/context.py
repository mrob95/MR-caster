from dragonfly import AppContext, Context

from six import string_types
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

class ChromeURLContext(Context):

    def __init__(self, match=None):
        Context.__init__(self)
        self.chrome_context = AppContext("chrome")
        if isinstance(match, string_types):
            self._matches = [match.lower()]
        elif isinstance(match, (list, tuple)):
            self._matches = [m.lower() for m in match]
        elif match is None:
            self._matches = None
        else:
            raise TypeError("match argument must be a string or None;"
                            " received %r" % match)

    def matches(self, executable, title, handle):
        if not self.chrome_context.matches(executable, title, handle):
            return False
        current_url = utilities.chrome_get_url()
        for match in self._matches:
            if match not in current_url:
                return False
        else:
            return True