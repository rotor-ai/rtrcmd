from vehicle.server import Server
from vehicle.vehicle_manager import VehicleManager
from common.command import Command
from common.trim import Trim
from common.config_handler import ConfigHandler
from common.mode import Mode
from vehicle.sensor_manager import SensorManager
import time
import logging


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    try:

        # Create the vehicle manager
        vehicle_mgr = VehicleManager()

        # Create the sensor manager
        sensor_mgr = SensorManager()
        sensor_mgr.start_sensors()

        # Create the server. This requires that we define some GET and POST request handlers for our endpoints.
        def handle_command_get():
            return vehicle_mgr.get_command().to_json()

        def handle_command_post(json_in):
            cmd = Command()
            cmd.from_json(json_in)
            vehicle_mgr.set_command(cmd)

        def handle_trim_get():
            return vehicle_mgr.get_trim().to_json()

        def handle_trim_post(json_in):
            trim = Trim()
            trim.from_json(json_in)
            vehicle_mgr.set_trim(trim)

        def handle_mode_get():
            return vehicle_mgr.get_mode().to_json()

        def handle_mode_post(json_in):
            mode = Mode()
            mode.from_json(json_in)
            vehicle_mgr.set_mode(mode)
            sensor_mgr.set_mode(mode)

        # Set the server address
        config_handler = ConfigHandler.get_instance()
        server_ip = config_handler.get_config_value_or('server_ip', '127.0.0.1')
        server_port = config_handler.get_config_value_or('server_port', 5000)

        server = Server('Vehicle', server_ip, server_port)
        server.add_endpoint('/command', 'command', get_func=handle_command_get, post_func=handle_command_post)
        server.add_endpoint('/trim', 'trim', get_func=handle_trim_get, post_func=handle_trim_post)
        server.add_endpoint('/mode', 'train', get_func=handle_mode_get, post_func=handle_mode_post)
        server.run()

        # Run forever and continually update the vehicle manager with sensor data
        while True:
            data = sensor_mgr.get_sensor_data()
            vehicle_mgr.update_sensor_data(data)
            time.sleep(0.1)

    except KeyboardInterrupt:
        vehicle_mgr.stop()
        server.stop()
        sensor_mgr.stop_sensors()
