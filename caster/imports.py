from dragonfly import *
from dragonfly.actions.action_mouse import get_cursor_position
# from dragonfly.grammar.elements_basic import Modifier

from caster.lib.dfplus.actions import Key, Text, SlowKey, SlowText, Mouse
from caster.lib.dfplus.actions import Store, Retrieve
from caster.lib.dfplus.elements import Dictation, Choice, Boolean
from caster.lib.dfplus.elements import Dictation, Choice, Boolean, Modifier
from caster.lib.dfplus.context import AppContext, ChromeURLContext
from caster.lib.dfplus.integers import ShortIntegerRef, ShortIntegerRefNo8, IntegerRef, IntegerRefMF, TestInteger
from caster.lib.execution import Alternating, SlowAlternating

from caster.lib.merge.selfmodrule import SelfModifyingRule
from caster.lib.merge.mergerule import MergeRule
from caster.lib.merge.nestedrule import NestedRule
from caster.lib import control, utilities, navigation, textformat, execution
from caster.lib.latex import tex_funcs

import re, os, datetime, sys
from subprocess import Popen