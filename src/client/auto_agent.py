from common.command import Command
from threading import Condition, Lock
import time
import logging
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread


class AutoAgentWorker(QObject):
    """
    Worker class to actually run the image processing
    """

    # Signal is emitted when the image is received
    command_ready = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QObject, self).__init__(*args, **kwargs)

        self._running = False
        self._latest_command = Command()
        self._lock = Lock()
        self._cond_var = Condition()
        self._image = None

    def running(self):
        return self._running

    def latest_command(self):

        with self._lock:
            return self._last_image

    def add_image(self, image):

        with self._cond_var:
            self._image = image
            self._cond_var.notifyAll()

    @pyqtSlot()
    def do_work(self):

        self._running = True

        while self._running:

            # Use the condition variable to determine if a new image is ready to be processed
            with self._cond_var:
                while self._running and self._image is None:

                    # No image is ready for processing, wait for notification that one is ready
                    self._cond_var.wait()

            if not self._running:
                break

            # Placeholder for running the image through the neural net
            logging.info("Processing image (PLACEHOLDER)...")
            time.sleep(1)


class AutoAgent(QObject):
    """
    Auto agent class will asynchronously process images and emit a signal when a new command is ready
    """

    # Emitted when a new image is received
    command_ready = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QObject, self).__init__(*args, **kwargs)
        self._worker = AutoAgentWorker()
        self._thread = QThread(self)
        self._worker.command_ready.connect(self.command_ready_slot)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.do_work)

    @pyqtSlot()
    def command_ready_slot(self):
        # Just pass on the signal
        self.command_ready.emit()

    def latest_command(self):
        return self._worker.latest_command()

    def add_image(self, image):

        self._worker.add_image(image)

    def start(self):
        self._thread.start()

    def stop(self):
        if self._worker.running():
            logging.info("Stopping auto agent")
            self._worker._running = False
            self._worker.add_image(None)
            self._thread.quit()
            self._thread.wait()
