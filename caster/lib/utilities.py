# -*- coding: utf-8 -*-
import io, os, sys, time, re, datetime
import toml, webbrowser
from PIL import ImageGrab
from subprocess import Popen
from dragonfly import Choice, Clipboard, Key, Window
from urllib2 import Request, urlopen, quote
# from urllib.parse import quote_pwe would reckon and do threelus
import threading
import uiautomation as automation


BASE_PATH = os.path.abspath(__file__).replace("\\", "/").rsplit("/lib/")[0]

if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

def diary():
    now = datetime.datetime.now()
    datestr = "%s-%s-%s" % (now.year, now.month, now.day)
    path = "C:/Users/Mike/Documents/notes/%s.md" % datestr
    if not os.path.isfile(path):
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
        with io.open(path, "wt+", encoding="utf-8") as f:
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

def read_text_relative(path):
    path = get_full_path(path)
    with open(path, "r") as f:
        return f.read()

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
        return None
    if prior_content == temporary and not same_is_okay:
        return None
    return temporary

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
    # browser = SETTINGS["browser_path"]
    # Popen([browser, url])
    webbrowser.open_new_tab(url)

def browser_search(text=None, url="https://www.google.com/search?q=%s"):
    if not text:
        text = read_selected(True)
    # text = ''.join(i for i in text if ord(i)<128)
    # url = url % text.replace(" ", "+").replace("\n", "")
    url = url % quote(text)
    browser_open(url)

def terminal(dir):
    Popen(["C:/Program Files/Git/git-bash.exe",
        "--cd=" + dir.replace("\\", "/")])
    # Popen(["C:/Program Files/WindowsApps/Microsoft.WindowsTerminal_0.4.2382.0_x64__8wekyb3d8bbwe/WindowsTerminal.exe",
        # "--cd=" + dir.replace("\\", "/")])

def mathfly_switch():
    Popen("C:/Users/Mike/Documents/NatLink/mathfly/SwitchHere.bat")

def word_count():
    selection = read_selected(True)
    words_list = selection.replace("\n", " ").split(" ")
    toast_notify("Word count", str(len(words_list)))

def windowinfo():
    wd = Window.get_foreground()
    print(wd.title)
    print(wd.executable)

def tinyurl():
    selection = read_selected(True)
    url = "http://tinyurl.com/api-create.php?url=" + selection
    request = Request(url)
    response = urlopen(request)
    tiny = response.read()
    Clipboard.set_system_text(tiny)

def chrome_get_url():
    control = automation.GetFocusedControl()
    control_list = []
    while control:
        control_list.insert(0, control)
        control = control.GetParentControl()
    if len(control_list) == 1:
        control = control_list[0]
    else:
        control = control_list[1]
    address_control = automation.FindControl(control, lambda c, d: isinstance(c, automation.EditControl) and "Address and search bar" in c.Name)
    return address_control.CurrentValue()

def image_name(dir="C:/Users/Mike/Pictures/saved"):
    now = datetime.datetime.now()
    file_name = str(now).rsplit(".", 1)[0].replace(":", "")
    return "%s/%s" % (dir, file_name)

def save_clipboard_image():
    im = ImageGrab.grabclipboard()
    try:
        im.save('%s.png' % image_name(),'PNG')
    except AttributeError:
        print("Clipboard does not contain an image")

def chrome_save_image():
    # Key("a-d/50").execute()
    # selection = read_selected(True)
    # Key("escape").execute()
    selection = chrome_get_url()
    img_type = selection.rsplit(".", 1)[1]
    if img_type in ["jpeg", "jpg", "png"]:
        Popen(["wget", "-O", "%s.%s" % (image_name(), img_type), selection])
