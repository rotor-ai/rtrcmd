from gpiozero import Servo
import logging
from common.command import Command


class Throttle(object):

    def __init__(self, config_handler):
        self.command = Command()
        self.config_handler = config_handler

        # Get the config value, then re-write it to the config. We do this so in the case that there is no config file
        # yet, it will create one with the default value
        speed_control_pin = self.config_handler.get_config_value_or('speed_control_pin', 12)
        self.config_handler.set_config_value('speed_control_pin', speed_control_pin)
        self.servo = Servo(speed_control_pin)

    def update_command(self, command):

        if command.get_throttle() == self.command.get_throttle() and \
           command.get_throttle_fwd_min() == self.command.get_throttle_fwd_min() and \
           command.get_throttle_fwd_max() == self.command.get_throttle_fwd_max() and \
           command.get_throttle_rev_min() == self.command.get_throttle_rev_min() and \
           command.get_throttle_rev_max() == self.command.get_throttle_rev_max():
            return

        # Process the new heading and check bounds
        self.command = command
        trimmed_throttle = self.command.get_throttle()
        if 0.0 < trimmed_throttle < self.command.get_throttle_fwd_min():
            trimmed_throttle = self.command.get_throttle_fwd_min()
        elif trimmed_throttle > self.command.get_throttle_fwd_max():
            trimmed_throttle = self.command.get_throttle_fwd_max()
        elif self.command.get_throttle_rev_min() < trimmed_throttle < 0.0:
            trimmed_throttle = self.command.get_throttle_rev_min()
        elif trimmed_throttle < self.command.get_throttle_rev_max():
            trimmed_throttle = self.command.get_throttle_rev_max()

        # Set the new heading
        logging.debug(f"Setting throttle to {trimmed_throttle}")
        self.servo.value = trimmed_throttle
