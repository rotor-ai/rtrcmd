import os
from pathlib import Path
import json
from common.command import Command
import logging


class ConfigHandler(object):
    """
    Class to handle updating the configuration file on the client
    """

    def __init__(self):

        # Flag to indicate that the config file has been setup correctly
        self.ok = False
        self.command = Command()
        self.ip = "127.0.0.1"
        self.port = 5000

        # Check if there is a rotor directory defined
        self.cfg_filepath = Path()
        if "ROTOR_DIR" in os.environ:
            rotor_dir = os.getenv("ROTOR_DIR")
            self.cfg_filepath = Path(rotor_dir) / 'cfg.json'
        else:
            home = Path.home()
            self.cfg_filepath = home / 'rotor' / 'cfg.json'

        self.read_from_config()

    def read_from_config(self):
        # Try to read the initial configuration from the config file
        try:
            with open(self.cfg_filepath) as in_file:
                config_json = json.load(in_file)
                if 'trim_command' in config_json:
                    self.command.from_json(config_json['trim_command'])
                if 'vehicle_ip' in config_json:
                    self.ip = config_json['vehicle_ip']
                if 'vehicle_port' in config_json:
                    self.port = config_json['vehicle_port']
            self.ok = True

        except FileNotFoundError as e:

            # File is not there, make a new one
            self.update_config()
            self.ok = True

        except json.JSONDecodeError as e:

            # We couldn't parse the information in the file, log the error, then override
            logging.error("Unable to parse config file, no configurations will be written")

    def write_trim_to_config(self, command):
        self.command = command
        if self.ok:
            self.update_config()

    def write_vehicle_ip_to_config(self, ip):
        self.ip = ip
        if self.ok:
            self.update_config()

    def write_vehicle_port_to_config(self, port):
        self.port = port
        if self.ok:
            self.update_config()

    def update_config(self):
        try:
            with open(self.cfg_filepath, 'w') as config_file:
                config_json = {'trim_command': self.command.to_json(),
                               'vehicle_ip': self.ip,
                               'vehicle_port': self.port}
                json.dump(config_json, config_file, indent=4)

        except Exception as e:
            logging.error(e)

    def get_config_command(self):
        return self.command

    def get_config_vehicle_ip(self):
        return self.ip

    def get_config_vehicle_port(self):
        return self.port
