from gpiozero import Servo
import logging
from common.command import Command


class Heading(object):

    def __init__(self, config_handler):
        self.command = Command()
        self.config_handler = config_handler

        # Get the config value, then re-write it to the config. We do this so in the case that there is no config file
        # yet, it will create one with the default value
        steering_pin = self.config_handler.get_config_value_or('steering_pin', 13)
        self.config_handler.set_config_value('steering_pin', steering_pin)
        self.servo = Servo(steering_pin)

    def update_command(self, command):

        # If this is not a new command, ignore it
        if (command.get_heading() == self.command.get_heading()) and \
           (command.get_heading_trim() == self.command.get_heading_trim()) and \
           (command.get_heading_max() == self.command.get_heading_max()) and \
           (command.get_heading_min() == self.command.get_heading_min()):
            return

        # Update our current command
        self.command = command

        # Process the new heading and check bounds
        trimmed_heading = self.command.get_heading() + self.command.get_heading_trim()
        if trimmed_heading > self.command.get_heading_max():
            trimmed_heading = self.command.get_heading_max()
        elif trimmed_heading < self.command.get_heading_min():
            trimmed_heading = self.command.get_heading_min()

        # Set the new heading
        logging.debug(f"Setting heading to {trimmed_heading}")
        self.servo.value = trimmed_heading
