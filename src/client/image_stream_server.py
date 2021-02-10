import socket
import threading
import logging
import struct
import io
from PIL import Image
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QObject


class ImageStreamWorker(QObject):
    """
    Simple worker class to listen to a socket and notify the main thread when the images are received
    """

    # Signal is emitted when the image is received
    image_received = pyqtSignal()

    def __init__(self, port, *args, **kwargs):
        super(QObject, self).__init__(*args, **kwargs)

        self._running = False
        self._lock = threading.Lock()
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(.1)

        self._last_image = None

    def get_last_image(self):

        with self._lock:
            return self._last_image

    @pyqtSlot()
    def do_work(self):

        logging.debug("Doing work")

        self._running = True

        try:
            logging.info(f"Starting image stream server on port {self._port}")
            self._socket.bind(('', self._port))
            self._socket.listen(1)

            while self._running:

                # Wait for incoming connections
                try:
                    connection, client_addr = self._socket.accept()
                    logging.info(f"Bound to vehicle at {client_addr}")
                    conn_file = connection.makefile('rb')
                    self.listen_for_images(connection)

                except socket.timeout:
                    continue

        except Exception as e:
            logging.error(f"Closing server socket due to exception: {e}")

    # Continually listens for images coming over the connection
    def listen_for_images(self, connection):

        while self._running:

            size_format = '<L'  # Corresponds to a little endian 32 bit unsigned int
            image_len_bytes = connection.recv(struct.calcsize(size_format))

            if not image_len_bytes:
                break

            # Calculate the size of the next image
            image_len = struct.unpack(size_format, image_len_bytes)[0]
            logging.debug(f"Received image of length: {image_len}")

            # Gut check to make sure the size is reasonable
            if image_len > 2 ** 16:
                break

            # Read that number of bytes from the buffer. Need to do this repeatedly because each packet is not
            # guaranteed to include all of the data
            data = bytearray()
            while len(data) < image_len:
                packet = connection.recv(image_len - len(data))
                if not packet:
                    break
                data.extend(packet)

            image_received = False
            with self._lock:
                try:
                    self._last_image = Image.open(io.BytesIO(data))
                    self._last_image = self._last_image.convert("RGB")
                    image_received = True
                except Exception as e:
                    logging.error(f"While receiving image: {e}")

            # Notify listeners if an image was received
            if image_received:
                self.image_received.emit()


class ImageStreamServer(QObject):
    """
    Server class that will asynchronously listen for images coming from the vehicle and emit signals when images are
    received.
    """

    # Emitted when a new image is received
    image_received = pyqtSignal()

    def __init__(self, port, *args, **kwargs):
        super(QObject, self).__init__(*args, **kwargs)
        self._worker = ImageStreamWorker(port)
        self._thread = QThread(self)
        self._worker.image_received.connect(self.image_received_slot)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.do_work)

    @pyqtSlot()
    def image_received_slot(self):
        # Just pass on the signal
        self.image_received.emit()

    def get_last_image(self):
        return self._worker.get_last_image()

    def start(self):
        self._thread.start()

    def stop(self):
        logging.info("Stopping image server")
        self._worker._running = False
        self._thread.quit()
        self._thread.wait()
