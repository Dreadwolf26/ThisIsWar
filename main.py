from NetworkCapture import *
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
    time.sleep(2)
    capture_network(adapter_name)