from dragonfly import Window, Key
from caster.lib import utilities

import struct
from ctypes import cdll

# https://github.com/mrob95/pyVirtualDesktopAccessor
if struct.calcsize("P")*8 == 32:
    vda = cdll.LoadLibrary(utilities.get_full_path("lib/bin/VirtualDesktopAccessor32.dll"))
else:
    vda = cdll.LoadLibrary(utilities.get_full_path("lib/bin/VirtualDesktopAccessor64.dll"))

def move_current_to_n(n=0,follow=False):
    wndh = Window.get_foreground().handle
    vda.MoveWindowToDesktopNumber(wndh, n-1)
    if follow:
        vda.GoToDesktopNumber(n-1)

def move_current_to_new(follow=False):
    wndh = Window.get_foreground().handle
    current = vda.GetCurrentDesktopNumber()
    total = vda.GetDesktopCount()
    Key("wc-d").execute()
    vda.MoveWindowToDesktopNumber(wndh, total)
    if not follow:
        vda.GoToDesktopNumber(current)

def go_to_n(n):
    current = vda.GetCurrentDesktopNumber() + 1
    if n>=1 and n != current:
        if current>n:
            Key("wc-left/10:" + str(current-n)).execute()
        else:
            Key("wc-right/10:" + str(n-current)).execute()
    # vda.GoToDesktopNumber(n-1)

def close_all():
    total = vda.GetDesktopCount()
    go_to_n(total)
    Key("wc-f4/10:" + str(total-1)).execute()

def move_desktop_to(n):
    for window in Window.get_all_windows():
        if vda.IsWindowOnCurrentVirtualDesktop(window.handle):
            vda.MoveWindowToDesktopNumber(window.handle, n-1)

