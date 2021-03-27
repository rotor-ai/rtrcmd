import requests
import logging
from common.trim import Trim


class RequestHandler(object):
    """
    Class to handle sending requests to the vehicle from the client
    """

    def __init__(self):
        self._ip = ""
        self._port = 5000
        self._timeout = .25
        self._proxy_address = ""
        self._proxy_port = 0
        self._use_proxy = False

    def set_endpoint(self, ip, port):
        self._ip = ip
        self._port = port

    def set_proxy(self, address, port):
        self._proxy_address = address
        self._proxy_port = port

    def is_using_proxy(self):
        return self._use_proxy

    def enable_proxy(self):
        self._use_proxy = True

    def disable_proxy(self):
        self._use_proxy = False

    def send_command(self, command):
        try:
            logging.debug(f"Posting command: {command.to_json()}")
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/command"
            r = requests.post(endpoint, None, command.to_json(), timeout=self._timeout)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def send_trim(self, trim):
        try:
            logging.debug(f"Posting trim: {trim.to_json()}")
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/trim"
            r = requests.post(endpoint, None, trim.to_json(), timeout=self._timeout)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def get_trim(self):
        try:
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/trim"
            r = requests.get(endpoint, timeout=self._timeout)
            if r.status_code != 200:
                logging.error(r.text)

            # Construct a trim object from the response
            trim = Trim()
            trim.from_json(r.json())
            return trim

        except Exception as e:
            logging.error(e)

        # Return a generic trim object
        return Trim()

    def send_image_stream_start(self, port):
        try:
            json_start = {'port': port, 'stream_images': True}
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/image_stream"
            r = requests.post(endpoint, None, json_start, timeout=self._timeout)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def send_image_stream_stop(self):
        try:
            json_stop = {'stream_images': False}
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/image_stream"
            logging.debug("Requesting video stream stop")
            r = requests.post(endpoint, None, json_stop, timeout=self._timeout)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def get_telemetry(self):
        try:
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/telemetry"
            logging.debug("Requesting current telemetry")
            r = requests.get(endpoint, timeout=self._timeout)
            if r.status_code != 200:
                logging.error(r.text)

            return r.json()

        except Exception as e:
            logging.error(e)

    def dest_port(self):
        return self._port

    def dest_ip(self):
        return self._ip

    def proxy_address(self):
        return self._proxy_address

    def proxy_port(self):
        return self._proxy_port
