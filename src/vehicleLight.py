from time import time_ns
from gpiozero import PWMLED
from constants import Constants

class VehicleLight:

	def __init__(self, PinId):
		self.pinId = PinId
		self.ledRef = PWMLED(PinId)
		self.blinking = False
		self.nextBlinkTime = 0

	def off(self):
		self.ledRef.value = Constants.LIGHT_OFF_PWM_VAL

	def dim(self):
		self.ledRef.value = Constants.LIGHT_DIM_PWM_VAL

	def bright(self):
		self.ledRef.value = Constants.LIGHT_BRIGHT_PWM_VAL

	def blink(self):
		self.blinking = True
		self.nextBlinkTime = time_ns() + Constants.LIGHT_BLINK_DURATION_NS

	def update(self):
		now = time_ns()
		if self.blinking and now > self.nextBlinkTime:
			if self.ledRef.value == Constants.LIGHT_DIM_PWM_VAL:
				self.ledRef.value = Constants.LIGHT_BRIGHT_PWM_VAL
			else:
				self.ledRef.value = Constants.LIGHT_DIM_PWM_VAL
			self.nextBlinkTime = now + Constants.LIGHT_BLINK_DURATION_NS