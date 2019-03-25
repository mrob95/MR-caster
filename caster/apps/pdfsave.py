import subprocess
# import dragonfly
from dragonfly import Choice, Function, Dictation, Window, Grammar

from caster.lib import utilities
from caster.lib.merge.selfmodrule import SelfModifyingRule

#module functions
def bring_it(path, page=None):
    if page:
        path += "#page=" + str(page)
    browser = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    subprocess.Popen([browser, path])

def bring_add(key):
    '''
    Add current program or highlighted text to bring me
    '''
    CONFIG = utilities.load_toml_relative("config/pdfs.toml")
    key = str(key)
    Key("a-d/5").execute()
    _, path = utilities.read_selected(True)
    Key("escape").execute()
    if not path:
        print('Cannot add %s as %s to bringme: cannot get path', launch, key)
        return
    CONFIG[key] = {"path": path}
    utilities.save_toml_relative(CONFIG, "config/pdfs.toml")
    bring_rule.refresh()

class BookmarkRule(SelfModifyingRule):
    pronunciation = "bookmark"
    def refresh(self, *args):
        #logger.debug('Bring me refresh')
        # self.extras[0] = Choice('desired_item', _rebuild_items())
        # self.reset(self.mapping)
        CONFIG = utilities.load_toml_relative("config/pdfs.toml")
        mapping = {}
        mapping["bookmark PDF as <key>"] = Function(bring_add)
        mapping["reload bookmarks"] = Function(self.refresh)
        mapping["edit bookmarks"] = Function(utilities.load_config, config_name="pdfs.toml")
        for pdf, data in CONFIG.iteritems():
            mapping["open bookmark " + pdf] = Function(
                bring_it, path=data["path"])
            for ref, page in data.iteritems():
                if ref != "path":
                    mapping["open bookmark " + pdf + " " + ref] = Function(
                        bring_it, path=data["path"], page=page)
        self.reset(mapping)

    mapping = {

    }

    extras = [
        Dictation("key"),
    ]


bookmark_rule = BookmarkRule()
grammar = Grammar("bookmark")
grammar.add_rule(bookmark_rule)
grammar.load()
