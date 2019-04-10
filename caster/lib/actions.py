from dragonfly import Key, Mouse, Pause, ActionBase, ActionError
from dragonfly import Text as TextBase
from dragonfly import Function as FunctionBase
from inspect import getargspec
import re

class Text(TextBase):
    _pause_default = 0.002
    def __init__(self, spec=None, static=False, pause=_pause_default, autofmt=False, use_hardware=False):
        TextBase.__init__(self, spec=spec, static=static, pause=pause, autofmt=autofmt, use_hardware=use_hardware)

class Function(FunctionBase):
    def _execute(self, data=None):
        arguments = dict(self._defaults)
        if isinstance(data, dict):
            arguments.update(data)

        if self._filter_keywords:
            invalid_keywords = set(arguments.keys()) - self._valid_keywords
            for key in invalid_keywords:
                del arguments[key]

        for argname, spec in arguments.iteritems():
            if type(spec) is str and spec.find("%") != -1:
                try:
                    arguments[argname] = spec % data
                except KeyError:
                    self._log_exec.error("%s: Spec %r doesn't match data %r."
                                         % (self._str, spec,
                                            {k:v for k,v in data.items() if k not in ["_grammar", "_rule", "_node"]}))
                    return False

        try:
            self._function(**arguments)
        except Exception as e:
            self._log.exception("Exception from function %s:"
                                % self._function.__name__)
            raise ActionError("%s: %s" % (self, e))

from caster.lib import utilities, control, navigation
SETTINGS = utilities.load_toml_relative("config/settings.toml")
# Override imported dragonfly actions with aenea's if the 'use_aenea' setting
# is set to true.
if SETTINGS["use_aenea"]:
    try:
        from aenea import Key, Text, Mouse
    except ImportError:
        print("Unable to import aenea actions. Dragonfly actions will be used "
              "instead.")
'''
Stores the currently highlighted text in a temporary variable,
to be Retrieved after some other action. If no text was
highlighted, an empty string will be stored.
Sample usage:
"find that": Store() + Key("c-f") + Retrieve() + Key("enter")

In order to enable use with web URLs, Store() takes a string,
space, which will replace all space characters, and a bool,
remove_cr, which if true will remove any newlines in the
selection, to avoid them triggering the request early.
Sample usage:
"wikipedia that":
    Store(space="+", remove_cr=True) + Key("c-t") +
    Text("https://en.wikipedia.org/w/index.php?search=") +
    Retrieve() + Key("enter")

There are cases where you may want the same function to do
different things depending on whether or not text was highlighted.
The action_if_no_text and action_if_text arguments to Retrieve()
are calls to Key() and allow this.
For example, you may want to finish inside a set of brackets
if no text was highlighted, but outside if there was text.
Sample usage:
"insert bold text":
    Store() + Text("\\textbf{}") + Key("left") +
    Retrieve(action_if_text="right")
'''


class Store(ActionBase):
    def __init__(self, space=" ", remove_cr=False, same_is_okay=True):
        ActionBase.__init__(self)
        self.space = space
        self.remove_cr = remove_cr
        self.same_is_okay = same_is_okay

    def _execute(self, data=None):
        _, orig = utilities.read_selected(self.same_is_okay)
        text = orig.replace(" ", self.space) if orig else ""
        control.nexus().temp = text.replace("\n", "") if self.remove_cr else text
        return True


class Retrieve(ActionBase):
    def __init__(self, action_if_no_text="", action_if_text=""):
        ActionBase.__init__(self)
        self.action_if_no_text = action_if_no_text
        self.action_if_text = action_if_text

    @classmethod
    def text(cls):
        return control.nexus().temp

    def _execute(self, data=None):
        output = control.nexus().temp
        Text(output).execute()
        if output:
            Key(self.action_if_text).execute()
        else:
            Key(self.action_if_no_text).execute()
        return True
