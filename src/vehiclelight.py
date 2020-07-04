from time import time_ns
from gpiozero import PWMLED
from constants import Constants


class VehicleLight:

    def __init__(self, ledRef):
        self.ledRef = ledRef
        self.blinking = False
        self.nextBlinkTime = 0

    def set_off(self):
        self.ledRef.value = Constants.LIGHT_OFF_PWM_VAL

    def set_dim(self):
        self.ledRef.value = Constants.LIGHT_DIM_PWM_VAL

    def set_bright(self):
        self.ledRef.value = Constants.LIGHT_BRIGHT_PWM_VAL

    def start_blinking(self):
        self.blinking = True
        self.nextBlinkTime = self.now_wrapper() + Constants.LIGHT_BLINK_DURATION_NS

    # THIS METHOD IS NOT UNDER TEST
    def now_wrapper(self):
        return time_ns()

    # def update(self):
    #     now = time_ns()
    #     if self.blinking and now > self.nextBlinkTime:
    #         if self.ledRef.value == Constants.LIGHT_DIM_PWM_VAL:
    #             self.ledRef.value = Constants.LIGHT_BRIGHT_PWM_VAL
    #         else:
    #             self.ledRef.value = Constants.LIGHT_DIM_PWM_VAL
    #         self.nextBlinkTime = now + Constants.LIGHT_BLINK_DURATION_NS
