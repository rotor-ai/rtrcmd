from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from .request_handler import RequestHandler
from common.config_handler import ConfigHandler
from common.mode import Mode, ModeType
from .image_stream_server import ImageStreamServer
import logging
from .training_mgr import TrainingMgr
from .auto_agent import AutoAgent


class VehicleCtl(QObject):
    """
    Primary vehicle interface class for the client. This class Controls:
        - Communication to and from the vehicle
        - Autonomous agents
        - Video streaming
        - Mode control
    """

    # Signal is emitted when the image is received
    image_received = pyqtSignal()
    command_ready = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QObject, self).__init__(*args, **kwargs)

        self._config_handler = ConfigHandler.get_instance()

        self._request_handler = RequestHandler()
        vehicle_ip = self._config_handler.get_config_value_or('vehicle_ip', "127.0.0.1")
        vehicle_port = self._config_handler.get_config_value_or('vehicle_port', 5000)
        proxy_address = self._config_handler.get_config_value_or('proxy_address', "")
        proxy_port = self._config_handler.get_config_value_or('proxy_port', 0)
        use_proxy = self._config_handler.get_config_value_or('use_proxy', False)
        self._request_handler.set_endpoint(vehicle_ip, vehicle_port)
        self._request_handler.set_proxy(proxy_address, proxy_port)
        if use_proxy:
            self._request_handler.enable_proxy()

        self._mode = Mode()

        # Setup the image server to receive images from the vehicle
        self._stream_port = self._config_handler.get_config_value_or('stream_port', 4000)
        self._image_stream_server = ImageStreamServer(self._stream_port)
        self._image_stream_server.image_received.connect(self.image_received_slot)

        self._training_mgr = TrainingMgr()
        self._auto_agent = AutoAgent()

    def start(self):
        # Start the image server and automatically request the vehicle to start streaming image data
        self._image_stream_server.start()
        self._request_handler.send_image_stream_start(self._stream_port)

    def stop(self):
        # Tell the vehicle to stop sending images, and stop the server
        if self._image_stream_server.streaming():
            self._request_handler.send_image_stream_stop()

        self._image_stream_server.stop()
        self._training_mgr.finalize_log()
        self._auto_agent.stop()

    def restart_stream(self):

        self._request_handler.send_image_stream_stop()
        self._request_handler.send_image_stream_start(self._stream_port)

    @pyqtSlot()
    def image_received_slot(self):

        if self._mode.mode_type() == ModeType.TRAIN:
            # Get the latest telemetry data from the vehicle
            telemetry = self._request_handler.get_telemetry()

            # Save off the current image and the current controls
            image = self._image_stream_server.get_last_image()
            self._training_mgr.add_image_telemetry(image, telemetry)

        elif self._mode.mode_type() == ModeType.AUTO:
            # Send the image to the auto agent
            image = self._image_stream_server.get_last_image()
            self._auto_agent.add_image(image)

        self.image_received.emit()

    def set_vehicle_endpoint(self, ip, port):
        self._request_handler.set_endpoint(ip, port)

    def vehicle_ip(self):
        return self._request_handler.dest_ip()

    def vehicle_port(self):
        return self._request_handler.dest_port()

    def vehicle_proxy_address(self):
        return self._request_handler.proxy_address()

    def vehicle_proxy_port(self):
        return self._request_handler.proxy_port()

    def send_command(self, cmd):
        self._request_handler.send_command(cmd)

    def mode(self):
        return self._mode

    def set_mode(self, mode):
        logging.info(f"Setting to mode {mode.mode_name()}")

        if self._mode.mode_type() == ModeType.TRAIN and mode.mode_type() != ModeType.TRAIN:
            # We're moving out of training mode
            self._training_mgr.finalize_log()

        if self._mode.mode_type() != ModeType.TRAIN and mode.mode_type() == ModeType.TRAIN:
            # We're moving into training mode
            self._training_mgr.init_new_log()

        if self._mode.mode_type() == ModeType.AUTO and mode.mode_type() != ModeType.AUTO:
            # We're moving out of auto mode
            self._auto_agent.stop()

        if self._mode.mode_type() != ModeType.AUTO and mode.mode_type() == ModeType.AUTO:
            # Moving into auto
            self._auto_agent.start()

        self._mode = mode

    def get_last_image(self):
        return self._image_stream_server.get_last_image()

    def set_proxy(self, address, port):
        self._config_handler.set_config_value('proxy_address', address)
        self._config_handler.set_config_value('proxy_port', port)
        self._request_handler.set_proxy(address, port)

        # Need to now restart the image server and image stream
        self._image_stream_server.stop()
        self._image_stream_server.start()
        self.restart_stream()

    def is_using_proxy(self):
        return self._request_handler.is_using_proxy()

    def enable_proxy(self):
        self._config_handler.set_config_value('use_proxy', True)
        self._request_handler.enable_proxy()

    def disable_proxy(self):
        self._config_handler.set_config_value('use_proxy', False)
        self._request_handler.disable_proxy()

    def set_endpoint(self, ip, port):
        self._config_handler.set_config_value('vehicle_ip', ip)
        self._config_handler.set_config_value('vehicle_port', port)
        self._request_handler.set_endpoint(ip, port)

        # Need to now restart the image server and image stream
        self._image_stream_server.stop()
        self._image_stream_server.start()
        self.restart_stream()

    def get_trim(self):
        return self._request_handler.get_trim()

    def send_trim(self, trim):
        self._request_handler.send_trim(trim)
