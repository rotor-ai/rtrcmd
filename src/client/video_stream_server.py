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

        self.stop_thread = False
        self.lock = threading.Lock()
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(.1)

        self.last_image = None

    def get_last_image(self):

        with self.lock:
            return self.last_image

    @pyqtSlot()
    def do_work(self):

        try:
            logging.info(f"Starting video stream server on port {self.port}")
            self.socket.bind(('', self.port))
            self.socket.listen(1)

            while not self.stop_thread:

                # Wait for incoming connections
                try:
                    connection, client_addr = self.socket.accept()
                    conn_file = connection.makefile('rb')
                    self.listen_for_images(connection)

                except socket.timeout:
                    continue

                logging.info(f"Bound to client {client_addr}")

        except Exception as e:
            logging.error(f"Closing server socket due to exception: {e}")

    # Continually listens for images coming over the connection
    def listen_for_images(self, connection):

        while not self.stop_thread:
            size_format = '<L'  # Corresponds to a little endian 32 bit unsigned int
            image_len_bytes = connection.recv(struct.calcsize(size_format))

            if not image_len_bytes:
                break

            # Calculate the size of the next image
            image_len = struct.unpack(size_format, image_len_bytes)[0]

            # Gut check to make sure the size is reasonable
            if image_len > 2 ** 16:
                break

            # Read that number of bytes from the buffer
            buffer = connection.recv(image_len)

            with self.lock:
                self.last_image = Image.open(io.BytesIO(buffer))
                self.last_image = self.last_image.convert("RGB")

            # Notify listeners that an image was received
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
        self.worker = ImageStreamWorker(port)
        self.thread = QThread(self)
        self.worker.image_received.connect(self.image_received_slot)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.do_work)

    @pyqtSlot()
    def image_received_slot(self):
        # Just pass on the signal
        self.image_received.emit()

    def get_last_image(self):
        return self.worker.get_last_image()

    def start(self):
        self.thread.start()

    def stop(self):
        logging.info("Stopping image server")
        self.worker.stop_thread = True
        self.thread.quit()
        self.thread.wait()
