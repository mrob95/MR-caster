import os
import threading
import subprocess
import time
import webbrowser
# import dragonfly
from dragonfly import Choice, Function, Dictation, Window, Grammar

from caster.lib import context, utilities
from caster.lib.actions import Text, Key
from caster.lib.merge.selfmodrule import SelfModifyingRule

DEFAULT_CONFIG = {
        "website": {},
        "folder": {},
        "program": {},
        "file": {},
    }

CONFIG = utilities.load_toml_relative("config/bringme.toml")
if not CONFIG:
    CONFIG = DEFAULT_CONFIG

def refresh():
    bring_rule.refresh()

#module functions
def bring_it(desired_item):
    '''
    Currently simply invoke os.startfile. New thread keeps Dragon from crashing.
    '''
    item, item_type = desired_item
    if item_type == "website":
        utilities.browser_open(item)
    elif item_type == 'folder':
        subprocess.Popen(['C:/Windows/explorer.exe', item])
    elif item_type == 'program':
        subprocess.Popen(item)
    else:
        threading.Thread(target=os.startfile, args=(item,)).start()

def bring_add(launch, key):
    '''
    Add current program or highlighted text to bring me
    '''
    key = str(key)
    if launch == "program":
        path = Window.get_foreground().executable
        if not path:
            # dragonfly.get_engine().speak("program not detected")
            print("Program path for bring me not found ")
    # elif launch == 'folder':
    #     Key("a-d").execute()
    #     Key("escape").execute()
    else:
        Key("a-d/5").execute()
        _, path = utilities.read_selected(True)
        Key("escape").execute()
    if not path:
        print('Cannot add %s as %s to bringme: cannot get path', launch, key)
        return
    CONFIG[launch][key] = path
    utilities.save_toml_relative(CONFIG, "config/bringme.toml")
    refresh()

def bring_remove(key):
    '''
    Remove item from bring me
    '''
    key = str(key)
    for section in CONFIG.keys():
        if key in CONFIG[section]:
            del CONFIG[section][key]
            utilities.save_toml_relative(CONFIG, "config/bringme.toml")
            refresh()
            return

def bring_restore():
    '''
    Restore bring me list to defaults
    '''
    global CONFIG
    CONFIG = DEFAULT_CONFIG
    refresh()

def _rebuild_items():
    #logger.debug('Bring me rebuilding extras')
    return {key: (os.path.expandvars(value), header) for header, section in CONFIG.iteritems()
        for key, value in section.iteritems()}

class BringRule(SelfModifyingRule):

    pronunciation = "bring me"

    def refresh(self, *args):
        #logger.debug('Bring me refresh')
        self.extras[0] = Choice('desired_item', _rebuild_items())
        self.reset(self.mapping)

    mapping = {
       "bring me <desired_item>":
            Function(bring_it),
       "<launch> to bring me [as] <key>":
            Function(bring_add),
       "remove <key> from bring me":
            Function(bring_remove),
       "restore bring me defaults":
            Function(bring_restore),
    }

    extras = [
        Choice("desired_item", _rebuild_items()),
        Choice("launch", {
            "[current] program": "program",
            "website": "website",
            "folder": "folder",
            "file": "file",
        }),
        Dictation("key"),
    ]


bring_rule = BringRule()
grammar = Grammar("bring me")
grammar.add_rule(bring_rule)
grammar.load()
