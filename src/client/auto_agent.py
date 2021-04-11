import typing

import PySide6
from PySide6.QtCore import QObject, Signal, Slot, QThread
from common.command import Command
from common.config_handler import ConfigHandler
import logging
from threading import Condition, Lock
from PIL.Image import Image
from torchvision.transforms import functional
from ai.simple_net import SimpleNet
from ai.label import Label
from torch import load as torch_load
from torch import max as torch_max
from pathlib import Path


class AutoAgentWorker(QObject):
    """
    Worker class to actually run the image processing
    """

    # Signal is emitted when the image is received
    command_ready = Signal()

    def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = ...) -> None:
        super().__init__()

        self._config_handler = ConfigHandler.get_instance()
        model_filepath = self._config_handler.get_config_value_or('model_filepath', None)
        if model_filepath is None:
            model_filepath = Path(self._config_handler.rotor_dir()) / 'model.nn'
            logging.info(f"No model filepath specified, checking {model_filepath}")
        else:
            logging.info(f"Using model filepath specified in config: {model_filepath}")

        self._model = SimpleNet()
        try:
            self._model.load_state_dict(torch_load(model_filepath))
            self._model.eval()
        except FileNotFoundError:
            logging.error("Model filepath does not exist, disabling auto mode")
            self._model = None

        self._running = False
        self._image_ready = False
        self._latest_command = Command()
        self._lock = Lock()
        self._cond_var = Condition()
        self._image = None

    def running(self):
        return self._running

    def latest_command(self):

        with self._lock:
            return self._last_image

    def add_image(self, image: Image):

        with self._cond_var:
            self._image = image
            self._image_ready = True
            self._cond_var.notifyAll()

    @Slot()
    def do_work(self):

        self._running = True

        while self._running:

            # Use the condition variable to determine if a new image is ready to be processed
            with self._cond_var:
                while self._running and not self._image_ready:

                    # No image is ready for processing, wait for notification that one is ready
                    self._cond_var.wait()

            if not self._running:
                break

            # Copy the image into the local thread
            pil_image = None
            with self._lock:
                pil_image = self._image
                self._image_ready = False

            # Convert the image to an image tensor
            pil_image = pil_image.convert('RGB')
            pil_image = functional.resize(pil_image, (64, 64))
            image_tensor = functional.to_tensor(pil_image)

            if self._model is not None:
                output = self._model(image_tensor)
                _, result_value = torch_max(output, dim=1)

                result_name = Label.label_index_to_name(result_value)
                logging.info(f"Prediction: {result_name}")


class AutoAgent(QObject):
    """
    Auto agent class will asynchronously process images and emit a signal when a new command is ready
    """

    # Emitted when a new image is received
    command_ready = Signal()

    def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = ...) -> None:
        super().__init__()
        self._worker = AutoAgentWorker()
        self._thread = QThread(self)
        self._worker.command_ready.connect(self.command_ready_slot)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.do_work)

    @Slot()
    def command_ready_slot(self):
        # Just pass on the signal
        self.command_ready.emit()

    def latest_command(self):
        return self._worker.latest_command()

    def add_image(self, image: Image):

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
