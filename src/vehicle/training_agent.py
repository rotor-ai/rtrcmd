from common.config_handler import ConfigHandler
from datetime import datetime
from pathlib import Path
import logging
import json
import time
from threading import Thread


class TrainingAgent(object):
    """
    The training agent is responsible for saving a metadata file containing sensor information and command information
    in order to train a model
    """

    def __init__(self):
        self.config_handler = ConfigHandler.get_instance()
        self.data_dir = self.config_handler.get_config_value_or('data_dir', '/data')
        self.filepath = None
        self.data = None

        self.save_interval = 5  # Seconds between saves
        self.last_save = time.time()

    def init_new_log(self):
        filename = Path(datetime.now().strftime("data_%d%m%Y_%H%M%S.json"))
        self.filepath = Path(self.data_dir) / filename
        self.data = {'data': []}
        self.last_save = time.time()

    def finalize_log(self):
        thread = Thread(target=self._write_data_to_log, daemon=True)
        thread.start()

    def _write_data_to_log(self):

        logging.info(f"Writing training data to {self.filepath}")
        with open(self.filepath, 'w') as file:
            file.write(json.dumps(self.data, indent=4))

    def update_sensor_data(self, data):

        if self.filepath is None:
            raise Exception("Training log has not been initialized")

        self.data['data'].append(data)

        now = time.time()
        if now - self.last_save > self.save_interval:
            thread = Thread(target=self._write_data_to_log, daemon=True)
            thread.start()
            self.last_save = now
