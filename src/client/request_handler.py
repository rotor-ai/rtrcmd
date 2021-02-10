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

    def set_endpoint(self, ip, port):
        self._ip = ip
        self._port = port

    def send_command(self, command):
        try:
            logging.info(f"Posting command: {command.to_json()}")
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/command"
            r = requests.post(endpoint, None, command.to_json(), timeout=.5)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def send_trim(self, trim):
        try:
            logging.info(f"Posting trim: {trim.to_json()}")
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/trim"
            r = requests.post(endpoint, None, trim.to_json(), timeout=.5)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def get_trim(self):
        try:
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/trim"
            r = requests.get(endpoint, timeout=.5)
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

    def send_mode(self, mode):
        try:
            logging.info(f"Posting mode: {mode.to_json()}")
            endpoint = "http://" + self._ip + ":" + str(self._port) + "/mode"
            r = requests.post(endpoint, None, mode.to_json(), timeout=.5)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def dest_port(self):
        return self._port

    def dest_ip(self):
        return self._ip
