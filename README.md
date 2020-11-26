# sonoff-diy-OTA-firmware
Command line process to upload a new firmware Over the Air to Sonoff DIY devices using the REST API http://developers.sonoff.tech/basicr3-rfr3-mini-http-api.html.

Created using Python 3.8 on Ubuntu 20.04 and tested on Sonoff Basic R3 and Sonoff Mini. 

### The Sonoff device must be on DIY mode and on the same network(sonoffDiy) with the computer running this script.
This requires:
* DIY 1.0:
  * Jumper on the designated pins
  * Wifi network with SSID: sonoffDiy and password: 20170618sn
* DIY 2.0: Check http://developers.sonoff.tech/sonoff-diy-mode-api-protocol.html

## Recommended use:
### AppImage:
* If on Linux, download and execute the AppImage from the releases page.

### Python virtual environment (Linux & Windows):
1. Create a virtual environment (venv or conda or something else): 
```
python3 -m venv /path/to/new/virtual/environment
```
or 
```
conda create -n <environment_name> python=3.8
```
2. Activate the environment according to your virtual environment.
3. Install the dependencies:
```
pip3 install -r requirements.txt
```
4. Execute the script:
```
python main.py
```
The commands may differ to Windows.

## Do not try to flash firmware that is larger than 508KB. Use something like the tasmota-lite.bin and later from within tasmota, flash the complete firmware.

## Process steps:
1. Download the firmware file (for example tasmota-lite.bin).
2. Run the main.py script.
3. Wait until your device gets discovered. If so, the discovery stops by pressing Enter. The process detects all Ewelink devices on the network using mDNS (thanks to zeroconf https://pypi.org/project/zeroconf).
4. Select the device to upload the new firmware.
5. The HTTP server starts(thanks to RangeHTTPServer https://github.com/danvk/RangeHTTPServer) to serve the directory of the selected firmware.
6. The process makes sure the OTA functionality is unlocked, using the appropriate REST request.
7. Send a POST request to the device providing the HTTP server link of the new firmware.
8. Sleep of 10 minutes to make sure that the transmission is over. If you see it is over(Tasmota wifi appears), kill the proceess with Ctrl-C.

Notes:
* If the device doesn't respond to mDNS messages remove the power source and connect it again while the discovery is in progress.

Dependencies: 
* https://pypi.org/project/rangehttpserver/
* https://pypi.org/project/zeroconf
* https://pypi.org/project/requests/
* https://pypi.org/project/simple-term-menu/

## TODO: 
* Handle requests error codes.
* Add a Dockerfile.

These scripts were quickly developed for my own needs to flash new firmware into sonoff devices since the existing tools seemed too complicated and couldn't manage to use it on Linux. I don't guarantee it works on any cases.
Please use it at your OWN RISK.
