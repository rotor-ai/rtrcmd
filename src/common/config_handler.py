import os
from pathlib import Path
import json
import logging
from multiprocessing import Lock


class ConfigHandler(object):
    __instance = None

    @staticmethod
    def get_instance():
        if ConfigHandler.__instance is None:
            ConfigHandler()

        return ConfigHandler.__instance

    def __init__(self):

        # Verify that this is not being
        if ConfigHandler.__instance is not None:
            raise Exception("Config handler is a singleton, use the get_instance() method to retrieve the global "
                            "config handler.")
        else:
            ConfigHandler.__instance = self

        # Flag to indicate that the config file has been setup correctly
        self.ok = False
        self.lock = Lock()  # Mutex lock so the config can be edited by multiple threads at the same time
        self.config = {}

        # Check if there is a rotor directory defined
        self.cfg_filepath = Path()
        if "ROTOR_DIR" in os.environ:
            rotor_dir = os.getenv("ROTOR_DIR")
            self.cfg_filepath = Path(rotor_dir) / 'cfg.json'
        else:

            # Use a global config filepath
            self.cfg_filepath = '/etc/rotor/cfg.json'
        logging.info(f"Using configuration file {self.cfg_filepath}")

        self._load_config()

    def _load_config(self):
        # Try to read the initial configuration from the config file
        try:
            with open(self.cfg_filepath) as in_file:
                with self.lock:
                    self.config = json.load(in_file)
            self.ok = True

        except FileNotFoundError as e:

            # File is not there, make a new one
            self._update_config()
            self.ok = True

        except json.JSONDecodeError as e:

            # We couldn't parse the information in the file, log the error, then override
            logging.error("Unable to parse config file, no configurations will be written")

    def _update_config(self):
        try:
            with open(self.cfg_filepath, 'w') as config_file:
                with self.lock:
                    json.dump(self.config, config_file, indent=4)

        except Exception as e:
            logging.error(e)

    def set_config_value(self, key, value):
        with self.lock:
            self.config[key] = value

        if self.ok:
            self._update_config()

    def get_config_value_or(self, key, default):
        with self.lock:
            if key in self.config:
                return self.config[key]
            else:
                return default
