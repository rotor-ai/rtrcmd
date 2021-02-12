from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from client.request_handler import RequestHandler
from common.config_handler import ConfigHandler
from common.mode import Mode
from client.image_stream_server import ImageStreamServer


class VehicleCtl(QObject):
    """
    Primary vehicle interface class for the client. Controls:
        - Communication to and from the vehicle
        - Autonomous agents
        - Video streaming
        - Mode control
    """

    # Signal is emitted when the image is received
    image_received = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QObject, self).__init__(*args, **kwargs)

        self._config_handler = ConfigHandler.get_instance()

        self._request_handler = RequestHandler()
        vehicle_ip = self._config_handler.get_config_value_or('vehicle_ip', "127.0.0.1")
        vehicle_port = self._config_handler.get_config_value_or('vehicle_port', 5000)
        self._request_handler.set_endpoint(vehicle_ip, vehicle_port)

        self._mode = Mode()

        # Setup the image server to receive images from the vehicle
        self._stream_port = self._config_handler.get_config_value_or('stream_port', 4000)
        self._image_stream_server = ImageStreamServer(self._stream_port)
        self._image_stream_server.image_received.connect(self.image_received_slot)

    def start(self):
        # Start the image server and automatically request the vehicle to start streaming image data
        self._image_stream_server.start()
        self._request_handler.send_image_stream_start(self._stream_port)

    def stop(self):
        # Tell the vehicle to stop sending images, and stop the server
        if self._image_stream_server.streaming():
            self._request_handler.send_image_stream_stop()

        self._image_stream_server.stop()

    @pyqtSlot()
    def image_received_slot(self):
        self.image_received.emit()

    def set_vehicle_endpoint(self, ip, port):
        self._request_handler.set_endpoint(ip, port)

    def vehicle_ip(self):
        return self._request_handler.dest_ip()

    def vehicle_port(self):
        return self._request_handler.dest_port()

    def send_command(self, cmd):
        self._request_handler.send_command(cmd)

    def mode(self):
        return self._mode

    def set_mode(self, mode):
        self._mode = mode

    def get_last_image(self):
        return self._image_stream_server.get_last_image()

    def set_endpoint(self, ip, port):
        self._config_handler.set_config_value('vehicle_ip', ip)
        self._config_handler.set_config_value('vehicle_port', port)
        self._request_handler.set_endpoint(ip, port)

    def get_trim(self):
        return self._request_handler.get_trim()

    def send_trim(self, trim):
        self._request_handler.send_trim(trim)
