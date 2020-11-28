from common.config_handler import ConfigHandler
import subprocess


if __name__ == '__main__':
    config_handler = ConfigHandler()
    ip = config_handler.get_config_value_or('vehicle_ip', '127.0.0.1')
    user = config_handler.get_config_value_or('vehicle_user', 'pi')

    command = f"rsync -v {user}@{ip}:/data/* ../data"
    print(command)
    subprocess.run(command, shell=True)
