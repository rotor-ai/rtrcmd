from common.config_handler import ConfigHandler
import os

"""
This function is used to generate a systemd service unit file. To install as a service, follow the following steps:
1. Add the following values to your config file:
    - 'vehicle_src_dir' - the path to the 'src' directory on the pi
    - 'vehicle_cfg_dir' - the path to the directory where you are storing your vehicle-side config file
2. Run this script to generate the rotor.service file
3. Copy all files over to the pi src directory using 'send_to_vehicle.py'
4. Copy the rotor.service file into /lib/systemd/system
5. Reload systemd with 'sudo systemctl daemon-reload'
6. Start the rotor service with 'sudo systemctl restart rotor.service'
7. Enable the rotor service to start automatically on boot with 'sudo systemctl enable rotor.service'
"""
if __name__ == '__main__':
    config_handler = ConfigHandler.get_instance()
    vehicle_src_dir = config_handler.get_config_value_or('vehicle_src_dir', '/home/pi/rotor/src')
    vehicle_cfg_dir = config_handler.get_config_value_or('vehicle_cfg_dir', '/etc/rotor')
    pwd = os.path.dirname(os.path.realpath(__file__))

    file_str = f"[Unit]\n" \
               f"Description=Rotor Vehicle Service\n" \
               f"After=multi-user.target\n\n" \
               f"[Service]\n" \
               f"Type=idle\n" \
               f"Environment=ROTOR_DIR={vehicle_cfg_dir}\n" \
               f"ExecStart=/usr/bin/python3 -u {vehicle_src_dir}/vehicle_main.py\n\n" \
               f"[Install]\n" \
               f"WantedBy=multi-user.target"

    with open('rotor.service', 'w') as f:
        f.write(file_str)
