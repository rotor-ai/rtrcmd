from vehicle.server import Server
from vehicle.vehicle_ctl import VehicleCtl
from common.command import Command
from common.config_handler import ConfigHandler
from common.mode import Mode, ModeType
from vehicle.sensor_data_collector import SensorDataCollector
from vehicle.camera import Camera
from threading import Lock
import time
import logging
import os

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    mode = Mode()
    mode_lock = Lock()  # Lock to guard against any threading weirdness when changing the mode
    collector = SensorDataCollector()

    try:

        # Create the vehicle controller
        vehicle_ctl = VehicleCtl()
        vehicle_ctl.run()
        collector.register_sensor(vehicle_ctl)

        # Create the camera
        camera = Camera()
        collector.register_sensor(camera)

        # Create some functions to handle a GET and POST request
        def handle_command_get():

            # Get the current command from the vehicle
            return vehicle_ctl.get_cmd().to_json()

        def handle_command_post(json_in):

            cmd = Command()
            cmd.from_json(json_in)

            # Pass the new command to the vehicle
            vehicle_ctl.set_cmd(cmd)

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
        server.add_endpoint('/mode', 'train', get_func=handle_mode_get, post_func=handle_mode_post)
        server.run()

        # Run forever
        while True:

            data = collector.get_data()

            with mode_lock:
                if mode.get_mode() == ModeType.TRAIN:

                    # Collect and label an image
                    pass

                elif mode.get_mode() == ModeType.AUTO:

                    # Figure out what we should do
                    pass

                else:
                    # Do nothing...
                    pass

            time.sleep(0.1)

    except KeyboardInterrupt:
        vehicle_ctl.stop()
        server.stop()
