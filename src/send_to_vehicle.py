from common.config_handler import ConfigHandler
import os
import subprocess


"""
To use this script, you should define at least three fields in your config file:
    vehicle_ip : The destination ip address to send the source files to
    vehicle_src_dir : The source directory on the vehicle the source files should be placed
    vehicle_user : The username for the vehicle
    
    This script forces the use of ipv4, which I've found to help connection issues with ssh, so I put it here too. Not
    sure if it's totally necessary
"""
if __name__ == '__main__':
    config_handler = ConfigHandler()
    ip = config_handler.get_config_value_or('vehicle_ip', '127.0.0.1')
    vehicle_src_dir = config_handler.get_config_value_or('vehicle_src_dir', '/home/pi/rotor/src')
    user = config_handler.get_config_value_or('vehicle_user', 'pi')
    pwd = os.path.dirname(os.path.realpath(__file__))

    command = f"scp -4 -r {pwd}/* {user}@{ip}:{vehicle_src_dir}"
    print(command)
    subprocess.run(command, shell=True)
