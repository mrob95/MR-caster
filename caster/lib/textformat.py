from caster.lib import utilities
from caster.lib.actions import Text

SETTINGS = utilities.load_toml_relative("config/settings.toml")


def formatted_text(capitalization, spacing, t):
    if capitalization == 0:
        capitalization = 5
    if spacing == 0 and capitalization == 3:
        spacing = 1

    if capitalization == 6:
        t = "".join(t.split(" "))
        t = t.lower()
        punc = "@1/4#9?5%,."
        result = []
        for i in range(len(t)):
            if i%2==0:
                result.append(punc[(i/2)%len(punc)])
            if i%3==0:
                result.append(t[i].upper())
            else:
                result.append(t[i])
        t = "".join(result)
    elif capitalization != 0:
        if capitalization == 1:
            t = t.upper()
        elif capitalization == 2:
            t = t.title()
        elif capitalization == 3:
            if len(t) > 1:
                t = t.title()
                t = t[0].lower() + t[1:]
            else:
                t = t[0].lower()
        elif capitalization == 4:
            t = t.capitalize()
        elif capitalization == 5:
            t = t.lower()
    if spacing != 0:
        if spacing == 1:
            t = "".join(t.split(" "))
        elif spacing == 2:
            t = "-".join(t.split(" "))
        elif spacing == 3:
            t = "_".join(t.split(" "))
        elif spacing == 4:
            t = ".".join(t.split(" "))
        elif spacing == 5:
            t = "/".join(t.split(" "))
        elif spacing == 6:
            t = "\\".join(t.split(" "))
    return t

def master_format_text(capitalization, spacing, text):
    Text(formatted_text(capitalization, spacing, unicode(text))).execute()