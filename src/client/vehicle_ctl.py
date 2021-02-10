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
        stream_port = self._config_handler.get_config_value_or('stream_port', 4000)
        self._image_stream_server = ImageStreamServer(stream_port)
        self._image_stream_server.image_received.connect(self.image_received_slot)

    def start(self):
        self._image_stream_server.start()

    def stop(self):
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
