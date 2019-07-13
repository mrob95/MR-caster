from caster.imports import *

class DragonRule(MergeRule):
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

control.non_ccr_app_rule(DragonRule())