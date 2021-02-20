from common.command import Command
from threading import Condition, Lock
import time
import logging
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread


class AutoAgentWorker(QObject):
    """
    Simple worker class to listen to a socket and notify the main thread when the images are received
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

    @pyqtSlot()
    def do_work(self):

        self._running = True

        while self._running:

            with self._lock:
                while self._running and self._image is None:
                    self._cond_var.wait()
            logging.info("Running image through ")
            time.sleep(1)


class AutoAgent(QObject):
    """
    Server class that will asynchronously listen for images coming from the vehicle and emit signals when images are
    received.
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

    def start(self):
        self._thread.start()

    def stop(self):
        if self._worker.running():
            logging.info("Stopping auto agent")
            self._worker._running = False
            self._thread.quit()
            self._thread.wait()
