from vehicle.vehicle_sensor import VehicleSensor


class Camera(VehicleSensor):

    def __init__(self):
        self.pi_camera = None

    def get_data(self) -> dict:
        return {'filepath': 'None'}

    def get_name(self) -> str:
        return "camera"
