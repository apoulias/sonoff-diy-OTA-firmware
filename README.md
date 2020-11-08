# sonoff-diy-OTA-firmware
Command line process to upload a new firmware Over the Air to Sonoff DIY devices.

1. Discover all Ewelink devices on the network using mDNS
2. Select the device to upload the new firmware
3. Start a HTTP server (thanks to RangeHTTPServer https://github.com/danvk/RangeHTTPServer) to serve the directory of the selected firmware.
4. Ensure the OTA functionality is unlocked, using the appropriate REST request.
5. POST request to the device providing the HTTP server link of the new firmware.
6. Hard coded sleep of 10 minutes to ensure that transmission is over. If it is over before that period, feel free to kill the proceess with Ctrl+C.

TO DO: create requirements.txt

This is a project intended to personal use. Use it at your OWN RISK.
