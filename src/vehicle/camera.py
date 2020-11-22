from vehicle.vehicle_sensor import VehicleSensor


class Camera(VehicleSensor):

    def __init__(self):
        self.pi_camera = None

    def get_data(self) -> dict:
        return {'filepath': 'None'}

    def start(self):
        pass

    def stop(self):
        pass
