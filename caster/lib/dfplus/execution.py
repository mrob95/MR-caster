from dragonfly import Playback, Clipboard, ActionBase

from caster.lib.dfplus.actions import Key, Text, SlowKey, SlowText, Mouse, Store, Retrieve
from caster.lib import utilities

# Alternate between executing as text and executing as keys
# "<example>": Alternating("example")
class Alternating(ActionBase):
    def __init__(self, command=""):
        ActionBase.__init__(self)
        self.command = command

    def _execute(self, data=None):
        command = data[self.command]
        if type(command) in [str, int, unicode]:
            Text(str(command)).execute()
        elif type(command) in [list, tuple] and len(command) == 1:
            (Text(command[0]) + Key("left")).execute()
        else:
            for i in range(len(command)):
                if i%2==0:
                    Text(command[i]).execute()
                else:
                    Key(command[i]).execute()

class SlowAlternating(ActionBase):
    def __init__(self, command=""):
        ActionBase.__init__(self)
        self.command = command

    def _execute(self, data=None):
        command = data[self.command]
        if type(command) in [str, int, unicode]:
            SlowText(str(command)).execute()
        elif type(command) in [list, tuple]:
            for i in range(len(command)):
                if i%2==0:
                    SlowText(command[i]).execute()
                else:
                    SlowKey(command[i]).execute()

def template(template):
    utilities.paste_string(template)

def python_setters():
    Store().execute()
    text = re.search(r"self,(.*?)\)", Retrieve.text())
    args = text.group(1).split(",")
    args2 = [x.split("=")[0].strip() for x in args]
    Key("end, enter").execute()
    for arg in args2:
        Text("self.%s = %s\n" % (arg, arg)).execute()

def markdown_link():
    text = Clipboard.get_system_text()
    print(text)
    if len(text)>4 and text.startswith("http"):
        Text("[]()").execute()
        Key("left, c-v, left:" + str(len(text) + 2)).execute()
    else:
        (Text("[]()") + Key("left")).execute()

def paste_as_admin():
    text = Clipboard.get_system_text()
    keys = []
    mapping = {
        "a": "a",
        "b": "b",
        "c": "c",
        "d": "d",
        "e": "e",
        "f": "f",
        "g": "g",
        "h": "h",
        "i": "i",
        "j": "j",
        "k": "k",
        "l": "l",
        "m": "m",
        "n": "n",
        "o": "o",
        "p": "p",
        "q": "q",
        "r": "r",
        "s": "s",
        "t": "t",
        "u": "u",
        "v": "v",
        "w": "w",
        "x": "x",
        "y": "y",
        "z": "z",
        "A": "A",
        "B": ["capital", "bravo"],
        "C": ["capital", "charlie"],
        "D": ["capital", "delta"],
        "E": ["capital", "echo"],
        "F": ["capital", "foxtrot"],
        "G": ["capital", "golf"],
        "H": ["capital", "hotel"],
        "I": ["capital", "india"],
        "J": ["capital", "juliet"],
        "K": ["capital", "kilo"],
        "L": ["capital", "lima"],
        "M": ["capital", "mike"],
        "N": ["capital", "november"],
        "O": ["capital", "oscar"],
        "P": ["capital", "papa"],
        "Q": ["capital", "quebec"],
        "R": ["capital", "romeo"],
        "S": ["capital", "sierra"],
        "T": ["capital", "tango"],
        "U": ["capital", "uniform"],
        "V": ["capital", "victor"],
        "W": ["capital", "whiskey"],
        "X": ["capital", "x-ray"],
        "Y": ["capital", "yankee"],
        "Z": ["capital", "zulu"],
        " ": "space",
        "&": "ampersand",
        "'": "apostrophe",
        "*": "asterisk",
        "@": ["at", "sign"],
        "\\": "backslash",
        "|": "bar",
        "^": "caret",
        ":": "colon",
        ",": "comma",
        "$": ["dollar", "sign"],
        "=": "equals",
        "!": ["exclamation", "mark"],
        "#": "hash",
        "-": "minus",
        "%": "percent",
        "+": "plus",
        "?": ["question", "mark"],
        ";": "semicolon",
        "/": "slash",
        "~": "tilde",
        "_": "underscore",
        ">": ["greater", "than"],
        "<": ["less", "than"],
        "(": ["left", "paren"],
        ")": ["right", "paren"],
        "[": ["left", "bracket"],
        "]": ["right", "bracket"],
        "{": ["left", "brace"],
        "}": ["right", "brace"],
    }
    playback_list = []
    interval = 0.5
    for char in text:
        if char in mapping and type(mapping[char]) is str:
            playback_list.append((["press", mapping[char]], interval))
        if char in mapping and type(mapping[char]) is list:
            playback_list.append((["press", mapping[char][0], mapping[char][1]], interval))
    Playback(playback_list).execute()