from vehicle.constants import Constants
from gpiozero import Servo
import logging
from common.command import Command


class Heading(object):

    def __init__(self):
        self.servo = Servo(Constants.GPIO_PIN_STEERING_SERVO)
        self.command = Command()

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
