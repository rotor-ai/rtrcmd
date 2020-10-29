from constants import Constants
from gpiozero import Servo
import logging
from command import Command


class Heading(object):

    def __init__(self):
        self.servo = Servo(Constants.GPIO_PIN_STEERING_SERVO)
        self.command = Command()

    def set_heading(self, heading):

        # If this is not a new command, ignore it
        if heading == self.command.get_heading():
            return

        # Set the heading
        logging.debug(f"Setting heading to {heading}")
        if heading < 0.0:
            self.servo.min()
        elif heading > 0.0:
            self.servo.max()
        else:
            self.servo.value = 0

        # Update our current command
        self.command.set_heading(heading)
