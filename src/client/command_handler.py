import requests
import logging


class CommandHandler(object):
    """
    Class to handle sending commands to the vehicle from the client
    """

    def __init__(self):
        self.endpoint = ""

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def send_command(self, command):
        try:
            logging.info(f"Posting command: {command.to_json()}")
            r = requests.post(self.endpoint, None, command.to_json())
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)
