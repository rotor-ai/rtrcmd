
class SensorDataCollector(object):

    def __init__(self):
        self.sensors = []

    def register_sensor(self, vehicle_sensor):
        self.sensors.append(vehicle_sensor)

    def get_data(self) -> dict:

        # Construct a json object with all the latest data from our sensor list
        ret = {}
        for sensor in self.sensors:
            try:
                ret[sensor.get_name()] = sensor.get_data()
            except (AttributeError, TypeError):
                raise AssertionError(f"{type(sensor).__name__} must implement the VehicleSensor interface")

        return ret
