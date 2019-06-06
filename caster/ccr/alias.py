from dragonfly import Dictation, Choice, Text, Function, Grammar

from caster.lib.dfplus.integers import IntegerRef, ShortIntegerRef
from caster.lib import utilities, control
from caster.lib.merge.selfmodrule import SelfModifyingRule

_NEXUS = control.nexus()

class Alias(SelfModifyingRule):
    mapping = {"default command": ""}
    key = "aliases"
    pronunciation = "alias"

    def delete_all(self):
        aliases = utilities.load_toml_relative("config/aliases.toml")
        aliases[Alias.key] = {}
        utilities.save_toml_relative(aliases, "config/aliases.toml")
        self.refresh()

    def delete(self, spec):
        aliases = utilities.load_toml_relative("config/aliases.toml")
        del aliases[Alias.key][spec]
        utilities.save_toml_relative(aliases, "config/aliases.toml")
        self.refresh()

    def alias(self, spec):
        spec = str(spec)
        e, text = utilities.read_selected(True)
        if spec and text:
            self.refresh(spec, str(text))

    def refresh(self, *args):
        '''args: spec, text'''
        aliases = utilities.load_toml_relative("config/aliases.toml")
        if not Alias.key in aliases:
            aliases[Alias.key] = {}
        if len(args) > 0:
            aliases[Alias.key][args[0]] = args[1]
            utilities.save_toml_relative(aliases, "config/aliases.toml")
        mapping = {}
        for spec in aliases[Alias.key]:
            mapping[spec] = Function(utilities.paste_string,
                    content=str(aliases[Alias.key][spec]))
            mapping["delete alias " + spec] = Function(self.delete, spec=spec)
        mapping["alias <s>"] = Function(lambda s: self.alias(s))
        mapping["delete aliases"] = Function(self.delete_all)
        self.reset(mapping)

# control.selfmod_rule(Alias())
grammar = Grammar("alias")
rule = Alias()
grammar.add_rule(rule)
grammar.load()


class Var(SelfModifyingRule):
    mapping = {"default command": ""}
    key = "variables"
    pronunciation = "variable"

    def delete_all(self):
        aliases = utilities.load_toml_relative("config/aliases.toml")
        aliases[Var.key] = {}
        utilities.save_toml_relative(aliases, "config/aliases.toml")
        self.refresh()

    def delete(self, spec):
        aliases = utilities.load_toml_relative("config/aliases.toml")
        del aliases[Var.key][spec]
        utilities.save_toml_relative(aliases, "config/aliases.toml")
        self.refresh()

    def alias(self, spec):
        spec = str(spec)
        e, text = utilities.read_selected(True)
        if spec and text:
            self.refresh(spec, str(text))

    def refresh(self, *args):
        '''args: spec, text'''
        aliases = utilities.load_toml_relative("config/aliases.toml")
        if not Var.key in aliases:
            aliases[Var.key] = {}
        if len(args) > 0:
            aliases[Var.key][args[0]] = args[1]
            utilities.save_toml_relative(aliases, "config/aliases.toml")
        mapping = {}
        for spec in aliases[Var.key]:
            mapping["var " + spec] = Text(str(aliases[Var.key][spec]))
            mapping["delete variable " + spec] = Function(self.delete, spec=spec)
        mapping["variable <s> [brunt]"] = Function(lambda s: self.alias(s))
        mapping["delete variables"] = Function(self.delete_all)
        self.reset(mapping)

control.selfmod_rule(Var())
