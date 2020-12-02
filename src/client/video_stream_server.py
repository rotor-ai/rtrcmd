import socket
import threading
import logging
from time import sleep
import struct


class VideoStreamServerThread(threading.Thread):

    def __init__(self, port, *args, **kwargs):
        super(VideoStreamServerThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(.1)

    def stopped(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    def run(self):
        logging.info(f"Starting video stream server on port {self.port}")
        self.socket.bind(('', self.port))
        self.socket.listen(1)

        while not self.stopped():

            # Wait for incoming connections
            try:
                connection, client_addr = self.socket.accept()
                conn_file = connection.makefile('rb')
            except socket.timeout:
                continue

            logging.info(f"Bound to client {client_addr}")

            while not self.stopped():
                size_format = '<L'  # Corresponds to a 32 bit unsigned int
                image_len_bytes = connection.recv(struct.calcsize(size_format))

                if not image_len_bytes:
                    break

                # Calculate the size of the next image
                image_len = struct.unpack(size_format, image_len_bytes)[0]
                logging.debug(image_len)

                # Read that number of bytes from the buffer
                image_bytes = connection.recv(image_len)

                if not image_bytes:
                    break

                logging.debug("Received image")


class VideoStreamServer(object):

    def __init__(self, port):
        self.thread = VideoStreamServerThread(port)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()


if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel('DEBUG')

    server = VideoStreamServer(4000)
    server.start()

    try:
        while True:
            logging.debug("Sleeping...")
            sleep(1)

    except KeyboardInterrupt:
        server.stop()
