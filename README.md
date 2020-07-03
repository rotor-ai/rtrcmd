#### PyCharm Development Setup:

* Open project.
* Right click `src` folder and mark as `Sources Root`
* Go to `File > Settings` and setup a virtual Python 3.8 interpreter for the project.
    
    The [`python3-distutils`](https://packages.ubuntu.com/focal/python3-distutils) 
    package my need to be installed on some linux systems in order to retrieve dependencies
    
    
#### Running on Raspberry Pi:
* Add an entry in `/etc/hosts` for `rc`. This should point to the IP address for your Raspberry Pi (RPi)
* In terminal, run `$ ./send-to-pi.sh` to send the src folder to an RPi on your network.