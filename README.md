#### PyCharm Development Setup:

* Open project.
* Right click `src` folder and mark as `Sources Root`
* Go to `File > Settings` and setup a virtual Python 3.8 interpreter for the project.
    
    The [`python3-distutils`](https://packages.ubuntu.com/focal/python3-distutils) 
    package my need to be installed on some linux systems in order to retrieve dependencies
    
    
#### Sending code to the Raspberry Pi:
* On your dev machine, add an entry in `/etc/hosts` for `rc`. This should point to the IP address for your Raspberry Pi (RPi)
* In terminal, run `$ ./send-to-pi.sh` to send the src folder to an RPi on your network.

#### Configuring the Raspberry Pi:
* You will need the following packages installed locally on the pi:
    
    [`pip`](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers)
    
    [`gpiozero`](https://gpiozero.readthedocs.io/en/stable/installing.html)
    
    [`pigpio`](http://abyz.me.uk/rpi/pigpio/download.html) also available [via pip](https://pypi.org/project/pigpio/)

#### Starting the program:
1) Turn on the ESC
2) Start the pigpio damean
3) Start the rtrcmd program
    ```
    $ python3 rtrcmd/rtrcmd.py
   ```
   
#### RPI shutdown proceedure:
1) Turn off the ESC
2) Stop the rtrcmd program
3) Stop the pigpio damean