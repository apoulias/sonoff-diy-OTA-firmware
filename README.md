# sonoff-diy-OTA-firmware
Command line process to upload a new firmware Over the Air to Sonoff DIY devices.

Created using Python 3.8 and tested on Sonoff Basic R3. 

### The Sonoff device must be on DIY mode and on the same network as the computer running this script.

## Recommended use:
1. Create a virtual environment (venv, conda or whatever): 
```
python3 -m venv /path/to/new/virtual/environment
```
or 
```
conda create -n venv <environment_name>
```
2. Activate the environment.
3. Install the requirements.txt
```
pip3 install -r requirements.txt
```
4. python main.py

## Followed process:
1. Discover all Ewelink devices on the network using mDNS (thanks to zeroconf https://pypi.org/project/zeroconf).
2. Select the device to upload the new firmware.
3. Start a HTTP server (thanks to RangeHTTPServer https://github.com/danvk/RangeHTTPServer) to serve the directory of the selected firmware.
4. Ensure the OTA functionality is unlocked, using the appropriate REST request.
5. POST request to the device providing the HTTP server link of the new firmware.
6. Hard coded sleep of 10 minutes to ensure that transmission is over. If it is over before that period, feel free to kill the proceess with Ctrl+C.

TO DO: add requirements.txt

This is a project intended to personal use. Use it at your OWN RISK.
