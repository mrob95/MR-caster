'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import MappingRule, Pause, Function, ActionBase, IntegerRef, Dictation, Choice, RuleWrap
from caster.lib import utilities
import re



class MergeRule(MappingRule):
    @staticmethod
    def _get_next_id():
        if not hasattr(MergeRule._get_next_id, "id"):
            MergeRule._get_next_id.id = 0
        MergeRule._get_next_id.id += 1
        return MergeRule._get_next_id.id

    @staticmethod
    def get_merge_name():  # returns unique str(int) for procedural rule names
        return str(MergeRule._get_next_id())

    mapping = {"hello world default macro": Pause("10")}
    '''MergeRules which define `pronunciation` will use
    the pronunciation string rather than their class name
    for their respective enable/disable commands'''
    pronunciation = None
    # Allows for self referencing rules (which include arbitrary sequences of other commands from the rule) to be included
    nested = None
    '''MergeRules which define `non` will instantiate
    their paired non-CCR MergeRule and activate it
    alongside themselves'''
    non = None
    '''MergeRules which define `mcontext` with a
    Dragonfly AppContext become non-global; this
    is the same as adding a context to a Grammar'''
    mcontext = None
    '''app MergeRules MUST define `mwith` in order to
    define what else they can merge with -- this is an
    optimization to prevent pointlessly large global
    CCR copies; mwith is a list of get_pronunciation()s'''
    mwith = None

    default_extras = {
        "n"   : IntegerRef("n", 1, 20),
        "text": Dictation("text"),
    }
    default_defaults = {
        "n": 1,
        "text": "",
    }

    def __init__(self,
                 name=None,
                 mapping=None,
                 extras=None,
                 defaults=None,
                 exported=None,
                 ID=None,
                 composite=None,
                 compatible=None,
                 mcontext=None,
                 mwith=None):

        self.ID = ID if ID is not None else MergeRule._get_next_id()
        self.compatible = {} if compatible is None else compatible
        '''composite is the IDs of the rules which this MergeRule is composed of: '''
        self.composite = composite if composite is not None else set([self.ID])
        self._mcontext = self.__class__.mcontext
        if self._mcontext is None: self._mcontext = mcontext
        self._mwith = self.__class__.mwith
        if self._mwith is None: self._mwith = mwith

        self.add_defaults()
        MappingRule.__init__(self, name, mapping, extras, defaults, exported)

    def __eq__(self, other):
        if not isinstance(other, MergeRule):
            return False
        return self.ID == other.ID

    def __call__(self):
        return self

    def add_defaults(self):
        if self.mapping:
            for name in self.default_extras.keys():
                match = "<%s>" % name
                for spec in self.mapping.keys():
                    if match in spec:
                        self.extras.append(self.default_extras[name])
                        if name in self.default_defaults:
                            self.defaults[name] = self.default_defaults[name]
                        break

    ''' "copy" getters used for safe merging;
    "actual" versions used for filter functions'''

    def mapping_copy(self):
        return self._mapping.copy()

    def mapping_actual(self):
        return self._mapping

    def extras_copy(self):
        return self._extras.copy()

    def extras_actual(self):
        return self._extras

    def defaults_copy(self):
        return self._defaults.copy()

    def defaults_actual(self):
        return self._defaults

    def merge(self, other):
        mapping = self.mapping_copy()
        mapping.update(other.mapping_copy())
        extras_dict = self.extras_copy()
        extras_dict.update(other.extras_copy())
        # not just combining lists avoids duplicates
        extras = extras_dict.values()
        defaults = self.defaults_copy()
        defaults.update(other.defaults_copy())
        context = self._mcontext if self._mcontext is not None else other.get_context(
        )  # one of these should always be None; contexts don't mix here
        return MergeRule(
            "Merged" + MergeRule.get_merge_name() + self.get_pronunciation()[0] +
            other.get_pronunciation()[0],
            mapping,
            extras,
            defaults,
            self._exported and other._exported,  # no ID
            composite=self.composite.union(other.composite),
            mcontext=context)

    def get_pronunciation(self):
        return self.pronunciation if self.pronunciation is not None else self.name

    def copy(self):
        return MergeRule(self.name, self._mapping.copy(), self._extras.values(),
                         self._defaults.copy(), self._exported, self.ID, self.composite,
                         self.compatible, self._mcontext, self._mwith)

    def compatibility_check(self, other):
        if other.ID in self.compatible:
            return self.compatible[other.ID]  # lazily
        compatible = True
        for key in self._mapping.keys():
            if key in other.mapping_actual().keys():
                compatible = False
                break
        self.compatible[other.ID] = compatible
        other.compatible[self.ID] = compatible
        return compatible

    def incompatible_IDs(self):
        return [ID for ID in self.compatible if not self.compatible[ID]]

    def get_context(self):
        return self._mcontext

    def set_context(self, context):
        self._mcontext = context

    def get_merge_with(self):
        return self._mwith

    def _display_available_commands(self):
        for spec in self.mapping_actual().keys():
            print(spec)  # do something fancier when the ui is better

    def generate_docs(self):
        result = "# %s\n## Commands\n" % self.pronunciation.capitalize()
        result += "| Command | Action | Options |\n"
        result += "| --- | --- | --- |\n"
        for k, v in self.mapping.items():
            if hasattr(v, "base"):
                v = v.base
            command = "`%s`" % k
            action = str(v).replace("ActionSeries", "").replace(", dynamic", "")
            action = re.sub(r"^\(+", "", action)
            action = re.sub(r"\)+", ")", action)
            action = re.sub(r"%\(", "***", action)
            action = re.sub(r"\)s", "***", action)
            action = re.sub(r"/\d+", "", action)
            options = ", ".join(re.findall(r"\<(.+?)\>", k))
            result  += "| `%s` | `%s` | `%s` |\n" % (command, action, options)
        if not self.extras:
            return result
        result += "\n## Extras\n"
        for e in self.extras:
            if isinstance(e, RuleWrap):
                values = "### %s : Numbers %s-%s\n" % (e.name, e.rule._element._min, e.rule._element._max)
            elif isinstance(e, Dictation):
                values = "### %s : Free dictation\n" % e.name
            elif isinstance(e, Choice):
                values = "### %s\n" % e.name
                values += "| Spoken form | Result |\n"
                values += "| --- | --- |\n"
                for k, v in e._choices.items():
                    values += "| `%s` | `%s` |\n" % (k, v)
            else:
                values = ""
            result += values
        # result += "| Name | Values | Default |\n"
        # result += "| --- | --- | --- |\n"
        # for e in self.extras:
        #     name = e.name
        #     if isinstance(e, RuleWrap):
        #         values = "Numbers %s-%s" % (e.rule._element._min, e.rule._element._max)
        #     elif isinstance(e, Dictation):
        #         values = "Free dictation"
        #     elif isinstance(e, Choice):
        #         values = "<br/>".join(["`%s`:`%s`" % (k,v) for k,v in e._choices.items()]) + "`"
        #     else:
        #         values = ""
        #     default = self.defaults[name] if name in self.defaults else "No default"
        #     result  += "| %s | %s | %s |\n" % (name, values, default)
        return result

    def _process_recognition(self, value, extras):
        if isinstance(value, ActionBase):
            value.execute(extras)
        elif self._log_proc:
            self._log_proc.warning("%s: mapping value is not an action,"
                                   " cannot execute." % self)
