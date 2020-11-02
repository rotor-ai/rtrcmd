import os
from pathlib import Path
import json
from common.command import Command
import logging


class ConfigHandler(object):

    def __init__(self):

        # Flag to indicate that the config file has been setup correctly
        self.ok = False

        # Check if there is a rotor directory defined
        self.cfg_filepath = Path()
        if "ROTOR_DIR" in os.environ:
            rotor_dir = os.getenv("ROTOR_DIR")
            self.cfg_filepath = Path(rotor_dir) / 'cfg.json'
        else:
            home = Path.home()
            self.cfg_filepath = home / 'rotor' / 'cfg.json'

        # Try to read the initial configuration from the config file
        self.command = Command()
        try:
            with open(self.cfg_filepath) as in_file:
                command_json = json.load(in_file)
                self.command.from_json(command_json)
            self.ok = True

        except FileNotFoundError as e:

            # File is not there, make a new one
            self.write_to_config(self.command)
            self.ok = True

        except json.JSONDecodeError as e:

            # We couldn't parse the information in the file, log the error, then override
            logging.error("Unable to parse config file, no configurations will be written")

    def write_to_config(self, command):
        self.command = command
        if self.ok:
            try:
                with open(self.cfg_filepath, 'w') as config_file:
                    json.dump(self.command.to_json(), config_file)
            except Exception as e:
                logging.error(e)

    def get_config_command(self):
        return self.command
