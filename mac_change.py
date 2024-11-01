#This script will bring the adapter down and change the mac 
# address and bring it back up into monitor mode. 

import subprocess
import os
from network_capture import start_monitor_mode

#update this line with your adapter name
WIRELESS_ADAPTER = os.getenv('WIRELESS_ADAPTER', 'wlan1')


def mac_address_change():
    try:
        print("[SUCCESS] Changing MAC")
        #bringing the interface down
        subprocess.run(['iwconfig',WIRELESS_ADAPTER, 'down'],check=True)
        #Changing the MAC address
        subprocess.run(['macchanger','-r',WIRELESS_ADAPTER],check=True)
        #putting adapter back in monitor mode
        start_monitor_mode()
    except Exception as e:
        print(f'[ERROR] Changing MAC: {e}')