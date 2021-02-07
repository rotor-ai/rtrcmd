from vehicle.vehicle_sensor import VehicleSensor
from common.config_handler import ConfigHandler
from datetime import datetime
from pathlib import Path
import threading
import logging
from vehicle.image_stream_client import ImageStreamClient
import io


# Surround this in a try/except so it can be run on a non-pi machine
try:
    import picamera
except ImportError:
    pass


class ImageStreamerThread(threading.Thread):
    """
    Main thread for capturing images from the camera and streaming them to the server
    """

    def __init__(self, *args, **kwargs):
        super(ImageStreamerThread, self).__init__(*args, **kwargs)
        self._running = False
        self._streaming = False

        self._config_handler = ConfigHandler.get_instance()
        self._data_dir = self._config_handler.get_config_value_or('data_dir', '/data')

        # Default resolution gives us a 4:3 aspect ratio. Width must be a multiple of 32, height must be a multiple
        # of 16
        self._res_width = self._config_handler.get_config_value_or('res_width', 192)
        self._res_height = self._config_handler.get_config_value_or('res_height', 144)
        # self.ip = self.config_handler.get_config_value_or('')
        self._pi_camera = picamera.PiCamera()
        self._pi_camera.resolution = (self._res_width, self._res_height)

        self._lock = threading.Lock()
        self._last_image_filename = None

        self._video_stream_client = None

    def stop(self):
        self._streaming = False
        self._running = False

    def start_streaming(self, ip, port):
        logging.info("Beginning image stream")
        self._video_stream_client = ImageStreamClient()

        # Set streaming to true if we successfully connect
        self._video_stream_client.connect(ip, port)
        self._streaming = self._video_stream_client.is_connected()

    def stop_streaming(self):
        logging.info("Stopping image stream")
        self._streaming = False

    def is_streaming(self):
        return self._streaming

    def run(self):

        self._running = True
        while self._running:

            # Pull data from the camera and write to a numpy array
            image_buffer = io.BytesIO()

            # Capture the image to the buffer. Using the video port allows us to capture images at a higher frame rate
            self._pi_camera.capture(image_buffer, use_video_port=True, format='jpeg')

            # If we're streaming, send the data to the streaming class
            if self._streaming and self._video_stream_client.is_connected():
                self._video_stream_client.send_image(image_buffer, image_buffer.tell())


class ImageStreamer(object):

    def __init__(self):
        self.thread = ImageStreamerThread()

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()

    def start_streaming(self, ip, port):
        self.thread.start_streaming(ip, port)

    def stop_streaming(self):
        self.thread.stop_streaming()

    def is_streaming(self):
        return self.thread.is_streaming()
