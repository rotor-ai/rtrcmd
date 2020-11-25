from vehicle.vehicle_sensor import VehicleSensor
from common.config_handler import ConfigHandler
from datetime import datetime
from pathlib import Path
import threading
import logging
from time import sleep
import picamera


class CameraThread(threading.Thread):
    """
    Main thread for capturing images from the camera and writing to disk
    """

    def __init__(self, *args, **kwargs):
        super(CameraThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._recording_event = threading.Event()

        self.config_handler = ConfigHandler.get_instance()
        self.data_dir = self.config_handler.get_config_value_or('data_dir', '/data')
        res_width = self.config_handler.get_config_value_or('res_width', 254)
        res_height = self.config_handler.get_config_value_or('res_height', 254)
        self.pi_camera = picamera.PiCamera()
        self.pi_camera.resolution = (res_width, res_height)

        self.lock = threading.Lock()
        self.last_image_filepath = None
        self.loop_delay = 0  # The camera takes long enough to capture an image

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def set_recording(self, recording):
        if recording:
            logging.info("Beginning camera recording")
            self._recording_event.set()
        else:
            logging.info("Stopping camera recording")
            self._recording_event.clear()

    def get_last_image_filepath(self):
        with self.lock:
            return str(self.last_image_filepath)

    def recording(self):
        return self._recording_event.is_set()

    def run(self):
        while not self.stopped():

            if self.recording():
                filename = datetime.now().strftime("%d%m%Y_%H%M%S_%f")[:-3] + ".jpg"
                filepath = Path(self.data_dir) / Path(filename)
                self.pi_camera.capture(str(filepath))

                with self.lock:
                    self.last_image_filepath = filepath

            sleep(self.loop_delay)


class Camera(VehicleSensor):

    def __init__(self):
        self.camera_thread = CameraThread()

    def get_data(self) -> dict:
        filepath = self.camera_thread.get_last_image_filepath()
        return {'filepath': filepath}

    def start(self):
        self.camera_thread.start()

    def stop(self):
        self.camera_thread.stop()
        self.camera_thread.join()

    def set_recording(self, recording):
        self.camera_thread.set_recording(recording)
