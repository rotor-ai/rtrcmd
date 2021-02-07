from vehicle.server import Server
from vehicle.vehicle_manager import VehicleManager
from common.command import Command
from common.trim import Trim
from common.config_handler import ConfigHandler
import logging
from time import sleep


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    try:

        # Create the vehicle manager
        vehicle_mgr = VehicleManager()

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

        def handle_data_get():
            return vehicle_mgr.get_sensor_data()

        def handle_image_stream_get():
            return vehicle_mgr.image_stream_running()

        def handle_image_stream_post(json_in):
            if 'stream_images' not in json_in:
                raise Exception("No \'stream_images\' key in POST")
            elif json_in['stream_images']:
                if 'ip' not in json_in:
                    raise Exception("No \'ip\' key in POST")
                if 'port' not in json_in:
                    raise Exception("No \'port\' key in POST")
                else:
                    vehicle_mgr.start_image_stream(json_in['ip'], json_in['port'])
            else:
                vehicle_mgr.stop_image_stream()

        # Set the server address
        config_handler = ConfigHandler.get_instance()
        server_ip = config_handler.get_config_value_or('server_ip', '127.0.0.1')
        server_port = config_handler.get_config_value_or('server_port', 5000)

        server = Server('Vehicle', server_ip, server_port)
        server.add_endpoint('/command', 'command', get_func=handle_command_get, post_func=handle_command_post)
        server.add_endpoint('/trim', 'trim', get_func=handle_trim_get, post_func=handle_trim_post)
        server.add_endpoint('/data', 'data', get_func=handle_data_get)
        server.add_endpoint('/image_stream', 'image_stream', get_func=handle_image_stream_get,
                            post_func=handle_image_stream_post)
        server.run()

        # Run forever
        while True:
            sleep(.1)

    except KeyboardInterrupt:
        vehicle_mgr.stop()
        server.stop()
