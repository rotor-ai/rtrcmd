from constants import Constants
from gpiozero import Servo
import logging
from command import Command


class Throttle(object):

    def __init__(self):
        self.servo = Servo(Constants.GPIO_PIN_ELECTRONIC_SPEED_CONTROLLER)
        self.command = Command()

    def set_throttle(self, throttle):

        # If this is not a new command, ignore it
        if throttle == self.command.get_throttle():
            return

        # Set the throttle
        logging.debug(f"Setting throttle to {throttle}")
        if throttle < 0.0:
            self.servo.min()
        elif throttle > 0.0:
            self.servo.max()
        else:
            self.servo.value = 0

        # Update our current command
        self.command.set_throttle(throttle)
