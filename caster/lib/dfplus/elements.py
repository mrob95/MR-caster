from dragonfly import Choice as ChoiceBase
from dragonfly import Dictation as DictationBase

class Boolean(ChoiceBase):
    def __init__(self, name, spec=None):
        if not spec: spec = name
        ChoiceBase.__init__(self,
                        name,
                        {spec: True},
                        default=False)

def Choice(name, choices, default=None, extras=None):
    if isinstance(choices, str):
        choices = {name: choices}
    return ChoiceBase(name, choices, extras, default)

def Dictation(name=None, default=None):
    return DictationBase(name=name, default=default)
