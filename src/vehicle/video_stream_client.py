import logging
from time import sleep
import io
import socket
import struct


class VideoStreamClient(object):

    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def send_image(self, image_buffer, image_size):
        # Send the size of the image
        size_format = '<L'  # Corresponds to a little endian 32 bit unsigned int
        logging.debug(image_size)
        self.socket.send(struct.pack(size_format, image_size))

        # Rewind back to the beginning of the buffer
        image_buffer.seek(0)

        # Write the entire image to the socket
        self.socket.send(image_buffer.read())

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel('DEBUG')
    streamer = VideoStreamClient('localhost', 4000)
    streamer.connect()

    for i in range(0, 1):
        with open('10122020_144526_744.jpeg', 'rb') as im:
            # Read from the image file object into an in-memory buffer
            im_io = io.BytesIO()
            im_io.write(im.read())

            # Send the image
            image_size = im_io.tell()  # Returns the size because the index into the buffer is currently at the end
            streamer.send_image(im_io, image_size)

        sleep(.05)

    streamer.close()
