# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
from gpiozero import PWMLED

from vehiclelight import VehicleLight

headlights = VehicleLight(PWMLED(2))
driverSideTailLight = VehicleLight(PWMLED(3))
passengerSideTailLight = VehicleLight(PWMLED(4))

items = [headlights, driverSideTailLight, passengerSideTailLight]

headlights.set_bright()
driverSideTailLight.start_blinking()
passengerSideTailLight.start_blinking()


while True:

	for item in items:
		item.update()

