import logging
import threading
from abc import ABC


class ThreadableBehavior(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._thread = ThreadableBehaviorThread()

    def start(self):
        self._thread.start()

    def stop(self):
        self._thread.quit()
        self._thread.wait()

class ThreadableBehaviorThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.behave = lambda: logging.error("NO BEHAVIOR DEFINED FOR THREAD!")

    def run(self) -> None:
        super().run()

        while 1:
            self.behave()
