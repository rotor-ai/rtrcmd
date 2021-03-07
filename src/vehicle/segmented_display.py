import threading
import time
import adafruit_ht16k33.segments
import netifaces


class SegmentedDisplay(threading.Thread):

    def __init__(self, i_square_c_instance):
        super().__init__()
        self.segmentDisplayInstance = adafruit_ht16k33.segments.Seg7x4(i_square_c_instance)
        self.loop_delay = 1
        self.runDuration = 0
        self.modeBehaviors = []
        self.currentDisplayMode = 0

    def set_text(self, text):
        self.segmentDisplayInstance.fill(0)
        self.segmentDisplayInstance.print(text)

    def add_display_mode(self, mode_behavior):
        self.modeBehaviors.append(mode_behavior)

    def run(self) -> None:
        super().run()
        while 1:
            time.sleep(self.loop_delay)
            self.runDuration += self.loop_delay

            current_behavior = self.modeBehaviors[self.currentDisplayMode]
            current_behavior(self)

