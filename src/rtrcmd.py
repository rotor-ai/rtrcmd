# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
from gpiozero import PWMLED

from constants import Constants
from vehiclelight import VehicleLight

headlights = VehicleLight(PWMLED(Constants.GPIO_PIN_HEADLIGHTS))
driverSideTailLight = VehicleLight(PWMLED(Constants.GPIO_PIN_LEFT_TAILLIGHT))
passengerSideTailLight = VehicleLight(PWMLED(Constants.GPIO_PIN_RIGHT_TAILLIGHT))

items = [headlights, driverSideTailLight, passengerSideTailLight]

headlights.set_bright()
driverSideTailLight.start_blinking()
passengerSideTailLight.start_blinking()


while True:

	for item in items:
		item.update()

