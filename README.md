#### PyCharm Development Setup:

1. Open project.
1. Right click `src` folder and mark as `Sources Root`
1. Go to `File > Settings` and setup a virtual Python 3.8 interpreter for the project.
    
    ⚠ On Ubuntu, the [`python3-distutils`](https://packages.ubuntu.com/focal/python3-distutils) package 
    is required to setup a virtual Python Interpreter in PyCharm.
    
    ⚠ On Ubuntu, PyQt5 will require the [libxcb-xinerama0](https://packages.ubuntu.com/focal/libxcb-xinerama0) package, as noted in [this forum post](https://forum.qt.io/topic/93247/qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found/4).
      
#### Configuring the Raspberry Pi:
* You will need the following packages installed locally on the pi:
    
    [`pip`](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers)
    
    [`gpiozero`](https://gpiozero.readthedocs.io/en/stable/installing.html)
    
    [`pigpio`](http://abyz.me.uk/rpi/pigpio/download.html) also available [via pip](https://pypi.org/project/pigpio/)

    [`pytorch`](https://www.spinellis.gr/blog/20200317/index.html) (must be built from source)

* Make sure your RPi is setup with SSH enabled by running `$ sudo raspi-config`

* Once SSH is installed, you'll need to login to the pi and run:
```
$ mkdir rotor
$ echo "
{
    \"is_vehicle\": true,
    \"server_ip\": \"0.0.0.0\",
    \"server_port\": 5000,
    \"speed_control_pin\": 12,
    \"steering_pin\": 13
}" > ~/rotor/cfg.json
```

#### Sending code to your Raspberry Pi:
1. On your dev machine, add an entry in `/etc/hosts` for `rc`. This should point to the IP address for your Raspberry Pi (RPi)
    ```
    192.168.x.x  rc
    ```
   
1. Edit your `.bashrc` file and add an export for ROTOR_DIR at the end of the file
   ```
        export ROTOR_DIR=/home/stu/
   ```
   Make sure to `$ source ~/.bashrc` when you're done

1. Create a new config file to point to your vehicle
   ```
    $ echo "
    {
        \"vehicle_ip\":\"rc\",
        \"vehicle_src_dir\":\"/home/pi/rotor/src\",
        \"vehicle_user\": \"pi\"
    }" > $ROTOR_DIR/cfg.json
   ```
1. In terminal, run `$ python3 ./src/send_to_vehicle.py` 

#### Starting the vehicle:
1) Turn on the ESC (Electronic Speed Controller)
2) Start the pigpio daemon
3) Start the rtrcmd program
    ```
    $ python3 rotor/vehicle_main.py
   ```
   
#### RPI shutdown procedure:
1) Turn off the ESC
2) Stop the rtrcmd program by pressing `ctr c`, 
    or if running in the background, you can kill the process with:
    ```
    pkill -9 python3
   ```
3) Stop the pigpio damean