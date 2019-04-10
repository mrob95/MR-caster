from dragonfly import (Grammar, Playback, Key, Dictation, Function)

from caster.lib.merge.mergerule import t
from caster.lib import utilities


class DragonRule(t):
    pronunciation = "dragon"

    mapping = {
        '(lock Dragon | deactivate)':
            Playback([(["go", "to", "sleep"], 0.0)]),
        '(number|numbers) mode':
            Playback([(["numbers", "mode", "on"], 0.0)]),
        'spell mode':
            Playback([(["spell", "mode", "on"], 0.0)]),
        'dictation mode':
            Playback([(["dictation", "mode", "on"], 0.0)]),
        'normal mode':
            Playback([(["normal", "mode", "on"], 0.0)]),
        'command mode':
            Playback([(["command", "mode", "on"], 0.0)]),
    }
    extras = [
    ]
    defaults = {}


#---------------------------------------------------------------------------

grammar = Grammar("Dragon Naturallyspeaking")

rule = DragonRule(name="dragon")
grammar.add_rule(rule)
grammar.load()
