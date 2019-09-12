from dragonfly import Function
from caster.lib import control, utilities
from caster.lib.dfplus.actions import Key, Text, Store, Retrieve
from caster.lib.dfplus.clipboard import Clipboard
from caster.lib.latex import bibtexer, book_citation_generator, word_counter
import codecs
import sys, threading
_NEXUS = control.nexus()


# Execute \first{second}, if second is empty then end inside the brackets for user input
def back_curl(first, second):
    (Text("\\" + str(first)) + Key("lbrace, rbrace, left") + Text(
            str(second))).execute()
    if str(second) != "":
        Key("right").execute()


def greek_letters(big, greek_letter):
    Text("\\" + str(greek_letter.title() if big else greek_letter) + " ").execute()

def symbol(symbol):
    if type(symbol) in [str, unicode, int]:
        Text("\\" + symbol + " ").execute()
    else:
        Text("\\" + str(symbol[0])).execute()
        Text("{}"*int(symbol[1])).execute()
        Key("left:" + str(2*int(symbol[1])-1)).execute()

def quote():
    text = utilities.read_selected(False)
    if text:
        Text("``" + text + "\'\'").execute()
    else:
        Text("``\'\'").execute()
        Key("left:2").execute()

def section(sub, text):
    Text("\\" + sub + "section{}").execute()
    Key("left").execute()
    Text(text.capitalize()).execute()
    Key("c-enter").execute()

def packages(packopts):
    if type(packopts) in [str, unicode]:
        back_curl("usepackage", packopts)
    elif type(packopts) in [tuple, list]:
        back_curl("usepackage" + packopts[0], packopts[1])

def begin_end(environment):
    text = utilities.read_selected(False)
    if type(environment) in [str, unicode]:
        env, arg = environment, ""
    elif type(environment) in [tuple, list]:
        env, arg = environment[0], environment[1]
    back_curl("begin", env)
    Text(arg + "\n").execute()
    if text:
        utilities.paste_string(text)
    Key("enter").execute()
    back_curl("end", env)
    if not text:
        Key("up").execute()

def selection_to_bib(ref_type, bib_path):
    Store(remove_cr=True, space="+").execute()
    print(Retrieve.text())
    if ref_type == "book":
        ref = book_citation_generator.citation_from_name(Retrieve.text())
    elif ref_type == "paper":
        ref = bibtexer.bib_from_title(Retrieve.text())
    elif ref_type == "link":
        ref = bibtexer.bibtex_from_link(Retrieve.text())
    with codecs.open(bib_path, encoding="utf-8", mode="a") as f:
        f.write(ref)
    print("Reference added:\n" + ref)
    Clipboard.set_system_text(bibtexer.get_tag(ref))
    try:
        utilities.toast_notify("Reference added:", ref.replace(",\n", " -"))
    except:
        pass


def word_count_from_string():
    raw = utilities.read_selected(True)
    raw_line_list = raw.split("\n")
    sentence_list = word_counter.extract_sentences(raw_line_list)
    words_list = word_counter.extract_words(sentence_list)
    utilities.toast_notify("Word count:", str(len(words_list)))


def math_mode(enable=True):
    BINDINGS = utilities.load_toml_relative("config/latex.toml")
    prefix = BINDINGS["symbol_prefix"].replace("[", "").replace("]", "")
    if enable:
        BINDINGS["symbol_prefix"] = "[" + prefix + "]"
    else:
        BINDINGS["symbol_prefix"] = prefix
    utilities.save_toml_relative(BINDINGS, "config/latex.toml")
    _NEXUS.merger.wipe()
    try:
        del _NEXUS.merger._global_rules[BINDINGS["pronunciation"]]
        want_reload_module = sys.modules["caster.ccr.latex"]
        reload(want_reload_module)
        print(BINDINGS["pronunciation"] + " rebuilt")
    except Exception as e:
        print(e)
    _NEXUS.merger.update_config()
    _NEXUS.merger.merge(3)