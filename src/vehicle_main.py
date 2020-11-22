from vehicle.server import Server
from vehicle.vehicle_ctl import VehicleCtl
from common.command import Command
from common.trim import Trim
from common.config_handler import ConfigHandler
from common.mode import Mode, ModeType
from vehicle.sensor_manager import SensorManager
from threading import Lock
import time
import logging

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    mode = Mode()
    mode_lock = Lock()  # Lock to guard against any threading weirdness when changing the mode

    try:

        # Create the vehicle controller
        vehicle_ctl = VehicleCtl()
        vehicle_ctl.start()

        # Create the server. This requires that we define some GET and POST request handlers for our endpoints.
        def handle_command_get():
            return vehicle_ctl.get_cmd().to_json()

        def handle_command_post(json_in):

            cmd = Command()
            cmd.from_json(json_in)
            vehicle_ctl.set_cmd(cmd)

        def handle_trim_get():
            return vehicle_ctl.get_trim().to_json()

        def handle_trim_post(json_in):

            trim = Trim()
            trim.from_json(json_in)
            vehicle_ctl.set_trim(trim)

        def handle_mode_get():

            with mode_lock:
                return mode.to_json()

        def handle_mode_post(json_in):

            with mode_lock:
                mode.from_json(json_in)
                if mode.get_mode() == ModeType.NORMAL:

                    # TODO: Set to normal mode
                    logging.info("Setting to normal mode")
                elif mode.get_mode() == ModeType.TRAIN:

                    # TODO: Set to training mode
                    logging.info("Setting to training mode")
                elif mode.get_mode() == ModeType.AUTO:

                    # TODO: Set to auto mode
                    logging.info("Setting to auto mode")

            return mode.to_json()

        # Set the server address
        config_handler = ConfigHandler.get_instance()
        server_ip = config_handler.get_config_value_or('server_ip', '127.0.0.1')
        server_port = config_handler.get_config_value_or('server_port', 5000)

        server = Server('Vehicle', server_ip, server_port)
        server.add_endpoint('/command', 'command', get_func=handle_command_get, post_func=handle_command_post)
        server.add_endpoint('/trim', 'trim', get_func=handle_trim_get, post_func=handle_trim_post)
        server.add_endpoint('/mode', 'train', get_func=handle_mode_get, post_func=handle_mode_post)
        server.run()

        # Create the sensor data collector
        sensor_mgr = SensorManager(vehicle_ctl)
        sensor_mgr.start_sensors()

        # Run forever
        while True:

            data = sensor_mgr.get_sensor_data()

            with mode_lock:
                if mode.get_mode() == ModeType.TRAIN:

                    # TODO: Collect and label an image
                    pass

                elif mode.get_mode() == ModeType.AUTO:

                    # TODO: Figure out what we should do
                    pass

                else:
                    # Do nothing...
                    pass

            time.sleep(0.1)

    except KeyboardInterrupt:
        vehicle_ctl.stop()
        server.stop()
        sensor_mgr.stop_sensors()
