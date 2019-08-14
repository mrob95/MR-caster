from dragonfly import Choice as ChoiceBase
from dragonfly import Dictation as DictationBase
from dragonfly import ElementBase
from dragonfly import Compound as CompoundBase
from dragonfly import Alternative as AlternativeBase

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


class Modifier(AlternativeBase):
    def __init__(self, element, modifier=None, modify_default=False):
        self._element = element
        self._modifier = modifier
        self._modify_default = modify_default
        AlternativeBase.__init__(self, children=(element,), name=element.name, default=element.default)

    def value(self, node):
        initial_value = AlternativeBase.value(self, node)
        value_is_default = initial_value == self.default
        if self._modifier and (self._modify_default or not value_is_default):
            return self._modifier(initial_value)
        else:
            return initial_value

