#Rotor.ai Command Line ESC Interface
#2020 Robbie and Stu

from gpiozero import PWMLED
from signal import pause
from time import time_ns

LIGHT_OFF_VAL = 0.0
LIGHT_DIM_VAL = 0.02
LIGHT_BRIGHT_VAL = 1.0
LIGHT_BLINK_DURATION_NS = pow(10,9)/2

class VehicleLight:

	def __init__(self, PinId):
		self.pinId = PinId
		self.ledRef = PWMLED(PinId)
		self.blinking = False
		self.nextBlinkTime = 0

	def off(self):
		self.ledRef.value = LIGHT_OFF_VAL

	def dim(self):
		self.ledRef.value = LIGHT_DIM_VAL

	def bright(self):
		self.ledRef.value = LIGHT_BRIGHT_VAL

	def blink(self):
		self.blinking = True
		self.nextBlinkTime = time_ns() + LIGHT_BLINK_DURATION_NS

	def update(self):
		now = time_ns()
		if self.blinking and now > self.nextBlinkTime:
			if self.ledRef.value == LIGHT_DIM_VAL:
				self.ledRef.value = LIGHT_BRIGHT_VAL
			else:
				self.ledRef.value = LIGHT_DIM_VAL
			self.nextBlinkTime = now + LIGHT_BLINK_DURATION_NS

headlights = VehicleLight(2)
driverSideTailLight = VehicleLight(3)
passengerSideTailLight = VehicleLight(4)

items = [headlights, driverSideTailLight, passengerSideTailLight]

headlights.bright()
driverSideTailLight.dim()
passengerSideTailLight.blink()


while True:

	for item in items:
		item.update()

