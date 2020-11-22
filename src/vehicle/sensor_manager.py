from vehicle.distance_sensor import DistanceSensor
from vehicle.camera import Camera
from common.config_handler import ConfigHandler


class SensorManager(object):
    """
    The sensor manager collects data from all sensors configured on the vehicle. The sensors are listed as a
    configuration parameter called 'sensor_list'. In the configuration, the sensor list should look as follows:
    {
        "sensor_list": [
            camera,
            distance_sensor,
            imu,
            ...
        ]
    }
    """

    def __init__(self, vehicle_ctl):
        self.config_handler = ConfigHandler.get_instance()
        self.vehicle_ctl = vehicle_ctl

        # Populate our sensor list from the config
        self.sensors = {}
        sensor_list = self.config_handler.get_config_value_or('sensor_list', [])
        for sensor in sensor_list:
            if sensor == 'camera':
                self.sensors['camera'] = Camera()
            elif sensor == 'distance_sensor':
                self.sensors['distance_sensor'] = DistanceSensor()

    """
    When called, the collector will loop through all configured sensors and produce a json object with all available 
    data. The json object may be larger or smaller depending on the number of sensors configured.
    """
    def get_sensor_data(self) -> dict:

        # Construct a json object with all the latest data from our sensor list
        ret = {'vehicle_ctl': self.vehicle_ctl.get_data()}
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
    def stop_sensors(self):
        for name, sensor in self.sensors.items():
            try:
                sensor.stop()
            except (AttributeError, TypeError):
                raise AssertionError(f"{type(sensor).__name__} must implement the VehicleSensor interface")
