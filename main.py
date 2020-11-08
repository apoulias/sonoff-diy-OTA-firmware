from zeroconf import ServiceBrowser, Zeroconf, IPVersion
from simple_term_menu import TerminalMenu
import os
import time
import hashlib
import multiprocessing
import requests
import socket

import server

DEVEL = False


class ZeroconfListener():
    """
    Listener definition used by Zeroconf.
    Collects all discovered devices into the discovered list.
    """
    def __init__(self, discovered):
        self.discovered = discovered

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))
        print('\n')

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            id_ = info.properties["id".encode()].decode()
            ip = info.parsed_addresses(IPVersion.V4Only)[0]
            port = info.port
            print("discovered {} {} {}".format(id_, ip, port))
            self.discovered.append((id_, ip, port))


def get_ip():
    """Get the ip of the host computer"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('1.1.1.1', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def main():
    """
    1. Identify all sonoff diy devices and select one to upload the 
       firmware
    2. Enter the filepath of the new firmware
    3. Potential security issue: Start a HTTP server, serving at the 
       directory of the selected firmware !!!
    4. Send a POST request to the device to unlock OTA
    5. Send a POST request to the device to get the new firmware, 
       served from the HTTP server
    6. Wait for 10 minutes(hardcoded) to finish the file transmission.
       If the Sonoff device has rebooted, feel free to kill the process
       with Ctrl+C.

    Good luck
    """
    zeroconf = Zeroconf()
    print("Browsing sonoff devices...\n\n")
    discovered = []
    listener = ZeroconfListener(discovered)
    browser = ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener, delay=1000)
    try:
        input("Press enter to stop discovering...\n\n")
    finally:
        zeroconf.close()
    
    if not discovered and not DEVEL:
        raise Exception("Nothing is discovered...")

    if DEVEL and not discovered:
        discovered.append(("1000b8df0d", "192.168.20.187", "8081"))

    print("Totaly {} devices were discovered...\n".format(len(discovered)))
    print("Select from the list:\n")
    options = ["{}: {} {}".format(d[0], d[1], d[2]) for d in discovered]
    terminal_menu = TerminalMenu(options)
    i = terminal_menu.show()

    id_ = discovered[i][0]
    ip = discovered[i][1]
    port = discovered[i][2]
    print("Selected device: {} with ip: {}\n".format(id_, ip))

    firmware = input("Enter the filepath of the firmware:\n")
    if not os.path.isfile(firmware):
        raise Exception("{} is not a file".format(firmware))
    
    directory = os.path.dirname(firmware)
    
    # Start http file server
    p = multiprocessing.Process(target=server.main, args=(directory,))
    p.start()
    time.sleep(15)

    try:
        # Unlock OTA
        print("OTA unlock")
        url = "http://{}:{}/zeroconf/ota_unlock".format(ip, port)
        data = {"deviceid": id_,
                "data": {}}
        ret = requests.post(url, json=data)
        print(ret)
        
        time.sleep(15)

        # Upload new firware
        print("OTA flash")
        url = "http://{}:{}/zeroconf/ota_flash".format(ip, port)
        sha256 = hashlib.sha256(open(firmware, "rb").read()).hexdigest()
        download_url = "http://{}:8000/{}".format(get_ip(), os.path.basename(firmware))
        data = {"deviceid": id_,
                "data": {"downloadUrl": download_url,
                        "sha256sum": sha256}}
        ret = requests.post(url, json=data)
        print(ret)

        print()
        print("Wait for maximum 10 minutes...")
        print("If the firmware is updated and a tasmota wifi network appears, stop the process with Ctl+C")
        time.sleep(600)

    finally:
        p.terminate()


if __name__ == '__main__':
    main()
