import requests
import logging


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
            r = requests.post(endpoint, None, command.to_json(), timeout=.1)
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)
