from caster.lib import control, utilities, textformat
from caster.lib.actions import Key, Text, Mouse
from caster.lib.clipboard import Clipboard
import time
SETTINGS = utilities.load_toml_relative("config/settings.toml")

# https://github.com/reckoner/pyVirtualDesktopAccessor
from ctypes import cdll
from win32gui import GetForegroundWindow
def load_vda():
    return cdll.LoadLibrary(utilities.get_full_path("lib/bin/VirtualDesktopAccessor.dll"))
# vda = cdll.LoadLibrary(utilities.get_full_path("lib/bin/VirtualDesktopAccessor.dll"))

def move_current_window_to_desktop(n=0,follow=False):
    vda = load_vda()
    wndh = GetForegroundWindow()
    vda.MoveWindowToDesktopNumber(wndh, n-1)
    if follow:
        vda.GoToDesktopNumber(n-1)

def move_current_window_to_new_desktop(follow=False):
    vda = load_vda()
    wndh = GetForegroundWindow()
    current = vda.GetCurrentDesktopNumber()
    total = vda.GetDesktopCount()
    Key("wc-d").execute()
    vda.MoveWindowToDesktopNumber(wndh, total)
    if not follow:
        vda.GoToDesktopNumber(current)

def go_to_desktop_number(n):
    vda = load_vda()
    return vda.GoToDesktopNumber(n-1)

def close_all_workspaces():
    vda = load_vda()
    total = vda.GetDesktopCount()
    go_to_desktop_number(total)
    Key("wc-f4/10:" + str(total-1)).execute()


def initialize_clipboard(nexus):
    if len(nexus.clip) == 0:
        nexus.clip = utilities.load_toml_relative(SETTINGS["clipboard_path"])

def temp_store(nexus):
    _, text = utilities.read_selected(False)
    if text:
        nexus.temp = text

def type_temp(nexus):
    if nexus.temp:
        Text(nexus.temp).execute()

def stoosh(nnavi500, nexus, key="c"):
    if nnavi500 == 1:
        Key("c-" + key).execute()
    else:
        cb = Clipboard(from_system=True)
        Key("c-" + key).execute()
        # time for keypress to execute
        time.sleep(SETTINGS["keypress_wait"])
        nexus.clip[str(nnavi500)] = Clipboard.get_system_text()
        utilities.save_toml_relative(
            nexus.clip, SETTINGS["clipboard_path"])
        cb.copy_to_system()


def drop(nnavi500, nexus, capitalization, spacing):
    # Maintain standard spark functionality for non-strings
    if capitalization == 0 and spacing == 0 and nnavi500 == 1:
        Key("c-v").execute()
        return
    # Get clipboard text
    if nnavi500 > 1:
        if str(nnavi500) in nexus.clip:
            text = nexus.clip[str(nnavi500)]
        else:
            text = None
    else:
        text = Clipboard.get_system_text()
    # Format if necessary, and paste
    if text is not None:
        cb = Clipboard(from_system=True)
        if capitalization != 0 or spacing != 0:
            text = textformat.formatted_text(capitalization, spacing, text)
        Clipboard.set_system_text(text)
        time.sleep(SETTINGS["keypress_wait"])
        Key("c-v").execute()
        time.sleep(SETTINGS["keypress_wait"])
        # Restore the clipboard contents.
        cb.copy_to_system()

def duple(nnavi50):
    cb = Clipboard(from_system=True)
    Key("escape, home, s-end, c-c, end").execute()
    time.sleep(SETTINGS["keypress_wait"])
    for _ in range(nnavi50):
        Key("enter, home, c-v").execute()
        time.sleep(SETTINGS["keypress_wait"])
    cb.copy_to_system()


def text_nav(modifier, direction, nnavi50, extreme):
    k = ""
    if extreme:
        if direction in ["left", "up"]:
            k = "home"
        else:
            k = "end"
        if direction in ["up", "down"]:
            k = "c-" + k
    else:
        k = str(direction) + ":" + str(nnavi50)
    if modifier:
        if "c-" in k:
            k = str(modifier).replace("c", "") + k
        else:
            k = str(modifier) + "-" + k.replace("c-", "")
    Key(k).execute()



def enclose_selected(enclosure):
    '''
    Encloses selected text in the appropriate enclosures
    By using the system Clipboard as a buffer ( doesn't delete previous contents)
    '''
    (err, selected_text) = utilities.read_selected(True)
    if err == 0:
        opener = enclosure.split('~')[0]
        closer = enclosure.split('~')[1]
        enclosed_text = opener + selected_text + closer
        # Attempt to paste enclosed text without altering clipboard
        if not utilities.paste_string(enclosed_text):
            print("failed to paste {}".format(enclosed_text))
