# Rotor.ai Command Line ESC Interface
# Copyright 2020 Robbie and Stu
from vehicleLight import VehicleLight

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

