from dragonfly import (Function, Grammar, Choice)

import os, sys
import logging
logging.basicConfig()

# def changeCallback(cbType, args):
#     print(cbType) # 'mic' or 'user'
#     print(args) # 'off',   'on', 'disabled' and 'sleeping'.

def _wait_for_wsr_activation():
    count = 1
    while True:
        try:
            from caster.apps import chrome
            break
        except:
            print("(%d) Attempting to load Caster -- WSR not loaded and listening yet..."
                  % count)
            count += 1
            time.sleep(1)

WSR = __name__ == "__main__"

if WSR:
    _wait_for_wsr_activation()

from caster.lib import control, utilities
from caster.lib.merge.mergerule import MergeRule
from caster.lib.merge.mergepair import MergeInf
_NEXUS = control.nexus()

BASE_PATH = os.path.realpath(__file__).split("\\_caster_main.py")[0].replace("\\", "/")
sys.path.append(BASE_PATH)

CORE = utilities.load_toml_relative("config/core.toml")


# Seems ugly but works
def build(startup=False):
    SETTINGS = utilities.load_toml_relative("config/settings.toml")
    for word in SETTINGS["delete_words"]:
        try:
            natlink.deleteWord(word)
        except:
            pass
    for word in SETTINGS["add_words"]:
        try:
            natlink.addWord(word)
        except:
            pass
    _NEXUS.merger.wipe()
    _NEXUS.merger._global_rules = {}
    _NEXUS.merger._app_rules = {}
    _NEXUS.merger._self_modifying_rules = {}
    if startup:
        apploaded = []
        for module_name in SETTINGS["app_modules"]:
            try:
                lib = __import__("caster.apps." + module_name)
                apploaded.append(module_name)
            except Exception as e:
                print("Ignoring rule '{}'. Failed to load with: ".format(module_name))
                print(e)
        if apploaded:
            print("App modules loaded: " + ", ".join(apploaded))
    ccrloaded = []
    ccrrebuilt = []
    for module_name in SETTINGS["ccr_modules"]:
        if "caster.ccr." + module_name in sys.modules:
            try:
                want_reload_module = sys.modules["caster.ccr." + module_name]
                reload(want_reload_module)
                ccrrebuilt.append(module_name)
            except Exception as e:
                print(e)
        else:
            try:
                lib = __import__("caster.ccr." + module_name)
                ccrloaded.append(module_name)
            except Exception as e:
                print("Ignoring rule '{}'. Failed to load with: ".format(module_name))
                print(e)
    if ccrloaded:
        print("CCR modules loaded: " + ", ".join(ccrloaded))
    if ccrrebuilt:
        print("CCR modules rebuilt: " + ", ".join(ccrrebuilt))
    _NEXUS.merger.update_config()
    _NEXUS.merger.merge(MergeInf.BOOT)
    print("*- Starting caster -*")
    print("Say \"enable <module name>\" to begin, or \n\"configure <module name>\" to make changes.")
    print("Modules available:")
    _NEXUS.merger.display_rules()

build(True)

def generate_ccr_choices(ref, nexus):
    return Choice(ref, {rule: rule for rule in nexus.merger.global_rule_names()})

def rule_changer(enable, name):
    ccr = utilities.load_toml_relative("config/ccr.toml")["global"]
    del ccr["Core"]
    if (name == "LaTeX maths" and ccr["LaTeX"]) or (name == "LaTeX" and ccr["LaTeX maths"]):
        _NEXUS.merger.global_rule_changer(name=name, enable=enable, save=True)
    else:
        for module in ccr:
            if ccr[module] and module != name:
                _NEXUS.merger.global_rule_changer(name=module, enable=False, save=True)
        _NEXUS.merger.global_rule_changer(name=name, enable=enable, save=True)
    if name == CORE["pronunciation"]:
        _NEXUS.merger.selfmod_rule_changer(name2="variable", enable=enable, save=True)

class MainRule(MergeRule):

	mapping = {
        "<enable> <name>": Function(rule_changer),

        "reboot dragon": Function(utilities.reboot),

        "rebuild caster": Function(build),

	}
	extras=[
		generate_ccr_choices("name", _NEXUS),
        Choice("enable", {
            "enable": True,
            "disable": False
        }),
	]

grammar = Grammar('general')
main_rule = MainRule()
grammar.add_rule(main_rule)
grammar.load()


if WSR:
    import pythoncom, time
    print("Windows Speech Recognition is garbage; it is " \
        +"recommended that you not run Caster this way. ")
    while True:
        pythoncom.PumpWaitingMessages()  # @UndefinedVariable
        time.sleep(.1)