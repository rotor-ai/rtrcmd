from vehicle.server import Server
from vehicle.vehicle_ctl import VehicleCtl
from common.command import Command
from common.config_handler import ConfigHandler
import time
import logging
import os

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    try:

        # Create the vehicle controller
        vehicle_ctl = VehicleCtl()
        vehicle_ctl.run()

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
            print("Handling mode get")

        def handle_mode_post(json_in):
            print("Handling mode post")

        # Set the server address
        config_handler = ConfigHandler.get_instance()
        server_ip = config_handler.get_config_value_or('server_ip', '127.0.0.1')
        server_port = config_handler.get_config_value_or('server_port', 5000)

        server = Server('Vehicle', server_ip, server_port)
        server.add_endpoint('/command', 'command', get_func=handle_command_get, post_func=handle_command_post)
        server.add_endpoint('/mode', 'train', get_func=handle_mode_get, post_func=handle_mode_post)
        server.run()

        # Collect images
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        vehicle_ctl.stop()
        server.stop()
