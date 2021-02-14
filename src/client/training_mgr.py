from common.config_handler import ConfigHandler
from datetime import datetime
from pathlib import Path
import logging
import json
import time
from threading import Thread
import os


class TrainingMgr(object):
    """
    The training manager is responsible for saving a metadata file containing sensor information and command information
    in order to train a model
    """

    def __init__(self):
        self._config_handler = ConfigHandler.get_instance()

        # Get the data directory location
        self._data_dir = self._config_handler.get_config_value_or('training_data_dir', None)
        if self._data_dir is not None:
            logging.info(f"Using configured data directory {self._data_dir}")
        else:
            self._data_dir = Path(self._config_handler.rotor_dir()) / 'data'
            logging.info(f"No training data directory specified, using {self._data_dir}")

        if not os.path.exists(self._data_dir):
            os.mkdir(self._data_dir)

        self._filepath = None
        self._data = None

        self._save_interval = 5  # Seconds between saves
        self._last_save = time.time()

    def init_new_log(self):
        filename = Path(datetime.now().strftime("data_%d%m%Y_%H%M%S.json"))
        self._filepath = Path(self._data_dir) / filename
        self._data = {'data': []}
        self._last_save = time.time()

    def finalize_log(self):
        thread = Thread(target=self._write_data_to_log, daemon=True)
        thread.start()

    def _write_data_to_log(self):

        logging.info(f"Writing training data to {self._filepath}")
        with open(self._filepath, 'w') as file:
            file.write(json.dumps(self._data, indent=4))

    def add_image_telemetry(self, image, telemetry):

        if self._filepath is None:
            raise Exception("Training log has not been initialized")

        filename = datetime.now().strftime("%d%m%Y_%H%M%S_%f")[:-3] + ".jpeg"
        filepath = Path(self._data_dir) / Path(filename)
        image.save(filepath)

        telemetry['image_filename'] = filename
        self._data['data'].append(telemetry)

        now = time.time()
        if now - self._last_save > self._save_interval:
            thread = Thread(target=self._write_data_to_log, daemon=True)
            thread.start()
            self._last_save = now
