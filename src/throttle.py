from constants import Constants
from gpiozero import Servo
import logging
from command import Command


class Throttle(object):

    def __init__(self):
        self.servo = Servo(Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER)
        self.command = Command()

    def update_command(self, command):

        # If this is not a new command, ignore it
        if (command.get_throttle() == self.command.get_throttle()) and \
           (command.get_throttle_fwd_min() == self.command.get_throttle_fwd_min()) and \
           (command.get_throttle_rev_max() == self.command.get_throttle_rev_max()) and \
           (command.get_throttle_fwd_max() == self.command.get_throttle_fwd_max()) and \
           (command.get_throttle_rev_min() == self.command.get_throttle_rev_min()):
            return

        # Update our current command
        self.command = command

        # Process the new heading and check bounds
        trimmed_throttle = self.command.get_throttle()
        if 0.0 < trimmed_throttle < self.command.get_throttle_fwd_min():
            trimmed_throttle = self.command.get_throttle_fwd_min()
        elif trimmed_throttle > self.command.get_throttle_fwd_max():
            trimmed_throttle = self.command.get_throttle_fwd_max()
        elif self.command.get_throttle_rev_min() < trimmed_throttle > 0.0:
            trimmed_throttle = self.command.get_throttle_rev_min()
        elif trimmed_throttle < self.command.get_throttle_rev_max():
            trimmed_throttle = self.command.get_throttle_rev_max()

        # Set the new heading
        logging.debug(f"Setting throttle to {trimmed_throttle}")
        self.servo.value = trimmed_throttle
