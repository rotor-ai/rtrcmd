from vehicle.server import Server
from vehicle.vehicle_ctl import VehicleCtl
from common.command import Command
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
        def handle_get():

            # Get the current command from the vehicle
            return vehicle_ctl.get_cmd().to_json()

        def handle_post(json_in):
            cmd = Command()
            cmd.from_json(json_in)

            # Pass the new command to the vehicle
            vehicle_ctl.set_cmd(cmd)

        # Default to using the internal loopback address
        server_addr = '127.0.0.1'
        if 'VEHICLE' in os.environ:

            # If this is the vehicle, listen on all addresses
            server_addr = '0.0.0.0'

        server = Server('Vehicle', server_addr, 5000)
        server.add_endpoint('/command', get_func=handle_get, post_func=handle_post)
        server.run()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        vehicle_ctl.stop()
        server.stop()
