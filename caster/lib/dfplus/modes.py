from dragonfly import Mimic, Playback, AppContext, Window, get_engine
import natlink

class ModeManager():
    def __init__(self):
        self.mode = "normal"
        self.frequency = 5
        self.command_titles = ["sublime", "jupyter", "rstudio", "mingw64"]
        self.command_contexts = AppContext(title=self.command_titles)
        self.timer = get_engine().create_timer(self.check_context, self.frequency)

    def switch_mode(self, mode="command"):
        Playback([([mode, "mode", "on"], 0.0)]).execute()
        self.mode = mode

    def check_context(self):
        if natlink.getMicState() == "on":
            window = Window.get_foreground()
            should_be_normal = not self.command_contexts.matches(window.executable, window.title, window.handle)
            if should_be_normal and self.mode == "command":
                self.switch_mode("normal")
            elif not should_be_normal and self.mode == "normal":
                self.switch_mode("command")
            else:
                pass

mm = ModeManager()