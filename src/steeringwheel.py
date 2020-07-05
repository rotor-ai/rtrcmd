from vehicledevice import VehicleDevice


class SteeringWheel(VehicleDevice):

    def __init__(self, servo):
        self.servo_ref = servo

    def update(self):
        pass
