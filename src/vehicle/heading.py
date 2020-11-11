from gpiozero import Servo
import logging
from common.command import Command
from common.config_handler import ConfigHandler


class Heading(object):

    def __init__(self):
        self.command = Command()
        self.config_handler = ConfigHandler.get_instance()

        # Get the config value, then re-write it to the config. We do this so in the case that there is no config file
        # yet, it will create one with the default value
        steering_pin = self.config_handler.get_config_value_or('steering_pin', 13)
        self.config_handler.set_config_value('steering_pin', steering_pin)
        self.servo = Servo(steering_pin)

    def update_command(self, command):

        # If this is not a new command, ignore it
        if command.get_heading() == self.command.get_heading():
            return

        # Set the new heading
        self.command = command
        logging.debug(f"Setting heading to {self.command.get_heading()}")
        self.servo.value = self.command.get_heading()
