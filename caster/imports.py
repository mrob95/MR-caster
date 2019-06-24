from dragonfly import Dictation, MappingRule, Choice, Function, ContextAction, Repetition, Compound
from dragonfly import Repeat, Playback, Mimic, Window, Clipboard
from dragonfly.actions.action_mouse import get_cursor_position

from caster.lib.dfplus.actions import Key, Text, Mouse, Store, Retrieve, MultiChoice
from caster.lib.dfplus.context import AppContext
from caster.lib.dfplus.integers import ShortIntegerRef, ShortIntegerRefNo8, IntegerRef, IntegerRefMF
from caster.lib.merge.selfmodrule import SelfModifyingRule
from caster.lib.merge.mergerule import MergeRule
from caster.lib.merge.nestedrule import NestedRule
from caster.lib import control, utilities, navigation, textformat, execution
from caster.lib.latex import tex_funcs


import re, os, datetime, sys
from subprocess import Popen