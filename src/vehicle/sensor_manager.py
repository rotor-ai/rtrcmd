from vehicle.distance_sensor import DistanceSensor
from common.config_handler import ConfigHandler
from common.mode import Mode, ModeType


class SensorManager(object):
    """
    The sensor manager collects data from all sensors configured on the vehicle. The sensors are listed as a
    configuration parameter called 'sensor_list'. In the configuration, the sensor list should look as follows:
    {
        "sensor_list": [
            distance_sensor,
            imu,
            ...
        ]
    }
    """

    def __init__(self):
        self.config_handler = ConfigHandler.get_instance()

        # Populate our sensor list from the config
        self.sensors = {}
        sensor_list = self.config_handler.get_config_value_or('sensor_list', [])
        for sensor in sensor_list:
            if sensor == 'distance_sensor':
                self.sensors['distance_sensor'] = DistanceSensor()

        self.mode = Mode()

    """
    When called, the collector will loop through all configured sensors and produce a json object with all available 
    data. The json object may be larger or smaller depending on the number of sensors configured.
    """
    def get_sensor_data(self) -> dict:

        # Construct a json object with all the latest data from our sensor list
        ret = {}
        for name, sensor in self.sensors.items():
            try:
                ret[name] = sensor.get_data()
            except (AttributeError, TypeError):
                raise AssertionError(f"{type(sensor).__name__} must implement the VehicleSensor interface")

        return ret

    """
    Calls vehicle_sensor.start() on all configured sensors
    """
    def start_sensors(self):
        for name, sensor in self.sensors.items():
            try:
                sensor.start()
            except (AttributeError, TypeError):
                raise AssertionError(f"{type(sensor).__name__} must implement the VehicleSensor interface")

    """
    Calls vehicle_sensor.stop() on all configured sensors
    """
    def stop(self):
        for name, sensor in self.sensors.items():
            try:
                sensor.stop()
            except (AttributeError, TypeError):
                raise AssertionError(f"{type(sensor).__name__} must implement the VehicleSensor interface")
