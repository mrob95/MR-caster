from caster.imports import *

class BringRule(SelfModifyingRule):
    pronunciation = "bring me"

    def refresh(self):
        self.mapping = {
            "bring me <program>":
                Function(self.bring_program),
            "bring me <website>":
                Function(self.bring_website),
            "bring me <folder> [in <app>]":
                Function(self.bring_folder),
            "bring me <file>":
                Function(self.bring_file),
            "refresh bring me":
                Function(self.load_and_refresh),
            "<launch> to bring me as <key>":
                Function(self.bring_add),
            "to bring me as <key>":
                Function(self.bring_add_auto),
            "remove <key> from bring me":
                Function(self.bring_remove),
        }
        self.extras = [
            Choice(
                "launch", {
                    "[current] program": "program",
                    "website": "website",
                    "folder": "folder",
                }),
            Choice("app", {
                "terminal": "terminal",
                "explorer": "explorer",
            }),
            Dictation("key"),
        ]
        self.extras.extend(self._rebuild_items())
        self.defaults = {"app": None}
        self.reset(self.mapping)

    def __init__(self):
        # Contexts
        self.browser_context = AppContext(["chrome", "firefox"])
        self.explorer_context = AppContext(["explorer.exe", "save", "open", "select", "choose directory"])
        self.terminal_context = AppContext("mintty.exe")
        # Paths
        self.terminal_path = "C:\\Program Files\\Git\\git-bash.exe"
        self.explorer_path = "C:\\Windows\\explorer.exe"
        self.config_path = "config/bringme.toml"
        # Get things set up
        self.config = {}
        self.load_config()
        SelfModifyingRule.__init__(self)

    def bring_website(self, website):
        ContextAction(Function(utilities.browser_open),
            [(self.browser_context,
                Key("c-l/10") + Text("%(url)s") + Key("enter"))]
            ).execute({"url": website})


    def bring_folder(self, folder, app):
        if not app:
            ContextAction(Function(lambda: Popen([self.explorer_path, folder])), [
                (self.terminal_context, Text("cd \"%s\"\n" % folder)),
                (self.explorer_context, Key("c-l/5") + Text("%s\n" % folder))
            ]).execute()
        elif app == "terminal":
            Popen([self.terminal_path, "--cd=" + folder.replace("\\", "/")])
        else:
            Popen([self.explorer_path, folder])

    def bring_program(self, program):
        Popen(program)

    def bring_file(self, file):
        threading.Thread(target=os.startfile, args=(file, )).start()

    def bring_add(self, launch, key):
        # Add current program or highlighted text to bring me
        key = str(key)
        if launch == "program":
            path = Window.get_foreground().executable
            if not path:
                # dragonfly.get_engine().speak("program not detected")
                print("Program path for bring me not found ")
        else:
            Key("a-d/5").execute()
            _, path = utilities.read_selected()
            Key("escape").execute()
        if not path:
            # logger.warn('Cannot add %s as %s to bringme: cannot get path', launch, key)
            return
        self.config[launch][key] = path
        self.save_config()
        self.refresh()

    def bring_add_auto(self, key):
        def add(launch):
            return Function(lambda: self.bring_add(launch, key))

        ContextAction(add("program"), [
            (self.browser_context, add("website")),
            (self.explorer_context, add("folder")),
        ]).execute()

    def bring_remove(self, key):
        # Remove item from bring me
        key = str(key)
        for section in self.config.keys():
            if key in self.config[section]:
                del self.config[section][key]
                self.save_config()
                self.refresh()
                return

    def _rebuild_items(self):
        # E.g. [Choice("folder", {"my pictures": ...}), ...]
        return [
            Choice(header,
                   {key: os.path.expandvars(value)
                    for key, value in section.iteritems()})
            for header, section in self.config.iteritems()
        ]

    def load_and_refresh(self):
        self.load_config()
        self.refresh()

    def load_config(self):
        self.config = utilities.load_toml_relative(self.config_path)
        if not self.config:
            print("Could not load bringme defaults")

    def save_config(self):
        utilities.save_toml_relative(self.config, self.config_path)

control.non_ccr_app_rule(BringRule())
