import logging
import socket
import struct


class ImageStreamClient(object):

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = False

    def connect(self, ip, port):
        try:
            self._socket.connect((ip, port))
            self._connected = True
        except Exception as e:
            logging.error(f"Could not connect image stream client due to {e}")
            self._connected = False

    def send_image(self, image_buffer, image_len):

        if not self._connected:
            raise Exception("Image stream client not connected")

        try:
            # Send the length of the image
            size_format = '<L'  # Corresponds to a little endian 32 bit unsigned int
            self._socket.send(struct.pack(size_format, image_len))

            # Rewind back to the beginning of the buffer
            image_buffer.seek(0)

            # Write the entire image to the socket
            self._socket.send(image_buffer.read())

        except BrokenPipeError as e:
            logging.error("Broken pipe, closing image stream socket")
            self._socket.close()
            self._connected = False

    def is_connected(self):
        return self._connected

    def close(self):
        self._socket.close()
