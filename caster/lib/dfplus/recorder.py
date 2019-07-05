from dragonfly import Pause
import time

class Recorder():

    def __init__(self):
        self.recording = None
        self.recorded = []

    def is_recording(self):
        return True if self.recording is not None else False

    def start_recording(self):
        self.recorded = []
        self.recording = time.time()

    def stop_recording(self):
        print(self.recording)
        print(self.recorded)
        self.recording = None

    def add_action(self, action, extras=None):
        action_tup = (time.time(), action, extras)
        self.recorded.append(action_tup)

    def execute(self):
        for tup in self.recorded:
            if type(tup[1]) is list:
                for action in tup[1]:
                    action.execute()
            else:
                tup[1].execute(tup[2])
            Pause("3").execute()


recorder = Recorder()