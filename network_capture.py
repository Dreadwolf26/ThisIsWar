import os
import subprocess
import csv
import time
import glob

# Adapter name update as needed
WIRELESS_ADAPTER = os.getenv('WIRELESS_ADAPTER', 'wlan1')

# Killing processes so the wireless adapter can be put into monitor mode
def start_monitor_mode():
    subprocess.run(['airmon-ng', 'check', 'kill'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[INFO] Preparing adapter for monitor mode...")

    # Check if the adapter is already in monitor mode
    adapter_status = subprocess.run(['ifconfig', WIRELESS_ADAPTER], capture_output=True, text=True)
    if "Mode:Monitor" in adapter_status.stdout:
        print(f"[INFO] {WIRELESS_ADAPTER} is already in monitor mode. Resetting")
        reset_monitor_mode(WIRELESS_ADAPTER)

    # Start monitor mode
    result = subprocess.run(['airmon-ng', 'start', WIRELESS_ADAPTER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"[SUCCESS] Monitor mode started on {WIRELESS_ADAPTER}")
    else:
        print(f"[ERROR] Failed to start monitor mode on {WIRELESS_ADAPTER}")
    return WIRELESS_ADAPTER

# Reset the adapter from monitor mode to managed mode
def reset_monitor_mode(adapter_name):
    print(f"[INFO] Resetting {adapter_name} to managed mode...")
    subprocess.run(['ip', 'link', 'set', adapter_name, 'down'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['iwconfig', adapter_name, 'mode', 'managed'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ip', 'link', 'set', adapter_name, 'up'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[SUCCESS] {adapter_name} reset to managed mode.")

# Start airodump-ng with CSV output
def capture_network():
    print("[INFO] Starting network capture...")
    csv_prefix = "network_capture"
    csv_pattern = f"{csv_prefix}-*.csv"
    
    # Start airodump-ng with CSV output
    process = subprocess.Popen([
        'sudo', 'airodump-ng',
        '--write-interval', '1',
        '--output-format', 'csv',
        '--write', csv_prefix,
        WIRELESS_ADAPTER
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
    
    # Wait until at least one CSV file is created
    timeout = 15  # Timeout in seconds
    start_time = time.time()
    csv_file = None
    while True:
        csv_files = glob.glob(csv_pattern)
        if csv_files:
            csv_file = sorted(csv_files)[-1]  # Get the latest CSV file
            print(f"[INFO] CSV file detected: {csv_file}")
            break
        if time.time() - start_time > timeout:
            print(f"[ERROR] No CSV file created within {timeout} seconds. Exiting capture.")
            break
        time.sleep(1)
    
    if not csv_file:
        print("[ERROR] Failed to start network capture.")
    
    return process, csv_file

# Function to extract BSSIDs from CSV
def get_bssids_from_csv(csv_file):
    bssid_list = []
    try:
        with open(csv_file, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if len(row) > 13 and row[0].lower().count(':') == 5:
                    bssid = row[0].strip()
                    channel_str = row[3].strip()
                    try:
                        channel_int = int(channel_str)
                        channel = str(channel_int)
                        if bssid and channel:
                            bssid_list.append((bssid, channel))  # Collect BSSID and Channel
                    except ValueError:
                        pass
    except FileNotFoundError:
        print("[ERROR] CSV file not found. Start capturing network data first.")
    except Exception as e:
        print(f"[ERROR] Problem reading CSV file {csv_file}: {e}")
    return bssid_list
