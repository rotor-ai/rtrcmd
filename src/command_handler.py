import requests
import logging


class CommandHandler(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def send_command(self, command):
        try:
            logging.info(f"Posting command: {command.to_json()}")
            r = requests.post(self.endpoint, None, command.to_json())
            if r.status_code != 200:
                logging.error(r.text)
        except Exception as e:
            logging.error(e)
