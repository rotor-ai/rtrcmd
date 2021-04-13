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
        # FYI, this does not instantaneously stop the thread.
        # The thread will stop after it iterates through the next behavior cycle inside the run() method
        self._thread.behave = lambda: False


class ThreadableBehaviorThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self._should_continue = True
        self.behave = self.default_behavior

    def default_behavior(self):
        logging.error("NO BEHAVIOR DEFINED FOR THREAD!")
        return False

    def run(self) -> None:
        super().run()

        while self._should_continue:
            self._should_continue = self.behave()

        logging.info("ENDING THREAD")
