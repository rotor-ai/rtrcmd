import requests
import logging
from common.trim import Trim


class CommandHandler(object):
    """
    Class to handle sending commands to the vehicle from the client
    """

    def __init__(self):
        self.ip = ""
        self.port = 5000

    def set_endpoint(self, ip, port):
        self.ip = ip
        self.port = port

    def send_command(self, command):
        try:
            logging.info(f"Posting command: {command.to_json()}")
            endpoint = "http://" + self.ip + ":" + str(self.port) + "/command"
            r = requests.post(endpoint, None, command.to_json(), timeout=.5)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def send_trim(self, trim):
        try:
            logging.info(f"Posting trim: {trim.to_json()}")
            endpoint = "http://" + self.ip + ":" + str(self.port) + "/trim"
            r = requests.post(endpoint, None, trim.to_json(), timeout=.5)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)

    def get_trim(self):
        try:
            endpoint = "http://" + self.ip + ":" + str(self.port) + "/trim"
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
            endpoint = "http://" + self.ip + ":" + str(self.port) + "/mode"
            r = requests.post(endpoint, None, mode.to_json(), timeout=.5)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)
