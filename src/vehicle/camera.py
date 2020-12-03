from vehicle.vehicle_sensor import VehicleSensor
from common.config_handler import ConfigHandler
from datetime import datetime
from pathlib import Path
import threading
import logging
from vehicle.video_stream_client import VideoStreamClient
import io


# Surround this in a try/except so it can be run on a non-pi machine
try:
    import picamera
except ImportError:
    pass


class CameraThread(threading.Thread):
    """
    Main thread for capturing images from the camera and writing to disk
    """

    def __init__(self, *args, **kwargs):
        super(CameraThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._streaming_event = threading.Event()
        self._save_next_image_event = threading.Event()
        self._image_saved_event = threading.Event()

        self.config_handler = ConfigHandler.get_instance()
        self.data_dir = self.config_handler.get_config_value_or('data_dir', '/data')

        # Default resolution gives us a 4:3 aspect ratio. Width must be a multiple of 32, height must be a multiple
        # of 16
        self.res_width = self.config_handler.get_config_value_or('res_width', 192)
        self.res_height = self.config_handler.get_config_value_or('res_height', 144)
        self.pi_camera = picamera.PiCamera()
        self.pi_camera.resolution = (self.res_width, self.res_height)

        self.lock = threading.Lock()
        self.last_image_filepath = None

        video_stream_ip = self.config_handler.get_config_value_or('video_stream_ip', '127.0.0.1')
        video_stream_port = self.config_handler.get_config_value_or('video_stream_port', 4000)
        self.video_stream_client = VideoStreamClient(video_stream_ip, video_stream_port)

    def stop(self):
        self._stop_event.set()

        if self.streaming():
            self.set_streaming(False)

    def stopped(self):
        return self._stop_event.is_set()

    def set_streaming(self, streaming):
        if streaming:
            logging.info("Beginning camera stream")
            self.video_stream_client.connect()
            self._streaming_event.set()
        else:
            logging.info("Stopping camera stream")
            self.video_stream_client.close()
            self._streaming_event.clear()

    def get_next_image_filepath(self) -> str:

        # Notify the camera loop that we want to save the next image
        self._save_next_image_event.set()

        # Wait for the next image to be saved
        self._image_saved_event.wait()

        # Before we leave, clean up the events
        self._save_next_image_event.clear()
        self._image_saved_event.clear()

        return self.last_image_filepath

    def streaming(self):
        return self._streaming_event.is_set()

    def run(self):

        while not self.stopped():

            # Pull data from the camera and write to a numpy array
            image_buffer = io.BytesIO()

            # Capture the image to the buffer. Using the video port allows us to capture images at a higher frame rate
            self.pi_camera.capture(image_buffer, use_video_port=True, format='jpeg')

            # If we're training, check if we should save off this image to a file
            if self._save_next_image_event.is_set():
                filename = datetime.now().strftime("%d%m%Y_%H%M%S_%f")[:-3] + ".jpeg"
                filepath = Path(self.data_dir) / Path(filename)

                with open(filepath, 'wb') as file:

                    # Ensure we're at the beginning of the buffer
                    image_buffer.seek(0)
                    file.write(image_buffer.read())

                # Notify other threads that we just saved an image
                self.last_image_filepath = str(filepath)
                self._image_saved_event.set()

            # If we're streaming, send the data to the streaming class
            if self.streaming():
                pass


class Camera(VehicleSensor):

    def __init__(self):
        self.camera_thread = CameraThread()

    def get_data(self) -> dict:
        filepath = self.camera_thread.get_next_image_filepath()
        return {'filepath': filepath}

    def start(self):
        self.camera_thread.start()

    def stop(self):
        self.camera_thread.stop()
        self.camera_thread.join()

    def set_streaming(self, streaming):
        self.camera_thread.set_streaming(streaming)
