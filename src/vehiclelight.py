from time import time_ns
from constants import Constants
from vehicledevice import VehicleDevice


class VehicleLight(VehicleDevice):


    def __init__(self, logger, ledRef) -> None:
        super().__init__(logger)
        self.ledRef = ledRef
        self.ledRef.value = 0
        self.blinking = False
        self.nextBlinkTime = 0

    def set_off(self):
        self.ledRef.value = Constants.LIGHT_OFF_PWM_VAL
        self.blinking = False
        self.logger.info("Turning off vehicleLight")

    def set_dim(self):
        self.ledRef.value = Constants.LIGHT_DIM_PWM_VAL
        self.blinking = False
        self.logger.info("Setting vehicleLight to dim")

    def set_bright(self):
        self.ledRef.value = Constants.LIGHT_BRIGHT_PWM_VAL
        self.blinking = False
        self.logger.info("Setting vehicleLight to full brightness")

    def start_blinking(self):
        self.blinking = True
        self.nextBlinkTime = self.now_wrapper() + Constants.LIGHT_BLINK_DURATION_NS
        self.ledRef.value = Constants.LIGHT_BRIGHT_PWM_VAL
        self.logger.info("Started blinking vehicleLight")

    # THIS METHOD IS NOT UNDER TEST
    def now_wrapper(self):
        return time_ns()

    def update(self):
        if self.blinking and self.now_wrapper() >= self.nextBlinkTime:
            self.ledRef.value = Constants.LIGHT_BRIGHT_PWM_VAL if self.ledRef.value == Constants.LIGHT_DIM_PWM_VAL else Constants.LIGHT_DIM_PWM_VAL
            self.nextBlinkTime = self.now_wrapper() + Constants.LIGHT_BLINK_DURATION_NS
