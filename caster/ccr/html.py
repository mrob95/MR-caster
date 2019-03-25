from dragonfly import Function, Choice

from caster.lib import control, utilities
from caster.lib.actions import Key, Text
from caster.lib.dfplus.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_file(utilities.get_full_path("caster/ccr/html/html.toml"))

# Alternate between executing as text and executing as keys
def insert(element):
    if type(element) in [str, int]:
        Text(element).execute()
    elif type(element) in [list, tuple]:
        for i in range(len(element)):
            if i%2==0:
                Text(element[i]).execute()
            else:
                Key(element[i]).execute()


class HTML(MergeRule):
    mapping = {
        "insert <element>": Function(insert),

    }
    extras = [
        Choice("element", BINDINGS["elements"]),
        ]
    defaults = {}


control.nexus().merger.add_global_rule(HTML())
