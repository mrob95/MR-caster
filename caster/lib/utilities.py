# -*- coding: utf-8 -*-
import io, os, sys, time, re, datetime
import toml
from subprocess import Popen
from dragonfly import Choice, Clipboard, Key
from urllib2 import quote
from multiprocessing import Process, Queue
from win10toast import ToastNotifier
import threading

BASE_PATH = os.path.abspath(__file__).replace("\\", "/").rsplit("/lib/")[0]

if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)


def diary():
    now = datetime.datetime.now()
    datestr = "%s-%s-%s" % (now.year, now.month, now.day)
    path = "C:/Users/Mike/Documents/notes/%s.md" % datestr
    if os.path.isfile(path):
        Popen(["notepad", path])
    else:
        with open(path, "w+") as f:
            f.write(title = "# %s - Notes - Mike Roberts\n" % datestr)
        Popen(["notepad", path])


def toast_notify(title="title", message="message"):
    Popen([
            "python27",
            BASE_PATH + "/lib/toaster.py",
            title,
            message
        ],
        shell=True)

def save_toml_file(data, path):
    try:
        formatted_data = unicode(toml.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        raise

def load_toml_file(path):
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = toml.loads(f.read())
    except IOError as e:
        if e.errno == 2:  # The file doesn't exist.
            save_toml_file(result, path)
        else:
            print(e)
    except Exception as e:
        print(e)
    return result

def get_full_path(path):
    return BASE_PATH + "/" + path

def load_toml_relative(path):
    path = get_full_path(path)
    return load_toml_file(path)

def save_toml_relative(data, path):
    path = get_full_path(path)
    return save_toml_file(data, path)

def read_selected(same_is_okay=False):
    '''Returns a tuple:
    (0, "text from system") - indicates success
    (1, None) - indicates no change
    (2, None) - indicates clipboard error
    '''
    time.sleep(SETTINGS["keypress_wait"])
    cb = Clipboard(from_system=True)
    temporary = None
    prior_content = None
    try:
        prior_content = Clipboard.get_system_text()
        Clipboard.set_system_text("")
        Key("c-c").execute()
        time.sleep(SETTINGS["keypress_wait"])
        temporary = Clipboard.get_system_text()
        cb.copy_to_system()
    except Exception:
        return 2, None
    if prior_content == temporary and not same_is_okay:
        return 1, None
    return 0, temporary

def paste_string(content):
    cb = Clipboard(from_system=True)
    time.sleep(SETTINGS["keypress_wait"])
    try:
        Clipboard.set_system_text(str(content))
        time.sleep(SETTINGS["keypress_wait"])
        Key("c-v").execute()
        time.sleep(SETTINGS["keypress_wait"])
        cb.copy_to_system()
    except Exception:
        return False
    return True

SETTINGS = load_toml_relative("config/settings.toml")

def reboot():
    Popen([BASE_PATH + "/lib/bin/reboot.bat", SETTINGS["dragon_path"]])

def load_config(config_name):
    parameters = []
    parameters.append(SETTINGS["editor_path"])
    parameters.append(get_full_path("config/" + config_name))
    Popen(parameters)

def load_text_file(path):
    parameters = []
    parameters.append(SETTINGS["editor_path"])
    parameters.append(path)
    Popen(parameters)

def kill_notepad():
    Popen(get_full_path("lib/bin/notepad_kill.bat"))

def browser_open(url):
    browser = SETTINGS["browser_path"]
    Popen([browser, url])

def browser_search(text=None, url="https://www.google.com/search?q=%s"):
    if not text:
        _, selection = read_selected(True)
        selection = ''.join(i for i in selection if ord(i)<128)
    else:
        selection = str(text)
    url = url % selection.replace(" ", "+").replace("\n", "")
    browser_open(url)


def terminal(dir):
    Popen(["C:/Program Files/Git/git-bash.exe",
        "--cd=" + dir.replace("\\", "/")])

def mathfly_switch():
    Popen("C:/Users/Mike/Documents/NatLink/mathfly/SwitchHere.bat")
