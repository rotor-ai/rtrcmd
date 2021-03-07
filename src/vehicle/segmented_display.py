import threading
import time
import adafruit_ht16k33.segments

class SegmentedDisplay():

    def __init__(self, i_square_c_instance):
        self.hardwareInstance = adafruit_ht16k33.segments.Seg7x4(i_square_c_instance)
        self.modeBehaviors = []
        self.currentDisplayMode = 0
        self.thread = SegmentedDisplayThread()

    def run_duration(self):
        return self.thread.run_duration

    def loop_delay(self):
        return self.thread.loop_delay

    def add_display_mode(self, mode_behavior):
        self.modeBehaviors.append(mode_behavior)
        self.set_display_mode(len(self.modeBehaviors)-1)

    def set_display_mode(self, mode_index):
        self.currentDisplayMode = mode_index
        self.thread.behave = self.modeBehaviors[self.currentDisplayMode]

    def start(self):
        self.thread.start()

    def run(self):
        self.thread.run()

    def stop(self):
        self.stop()

    def set_text(self, text):
        self.hardwareInstance.fill(0)
        self.hardwareInstance.print(text)


class SegmentedDisplayThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.loop_delay = 0.5
        self.run_duration = 0
        self.behave = lambda : print("NO BEHAVIOR DEFINED FOR THREAD!")

    def run(self) -> None:
        super().run()
        while 1:
            time.sleep(self.loop_delay)
            self.run_duration += self.loop_delay
            self.behave()

