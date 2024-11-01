import os
import traceback
from scapy.all import *

def find_cap_files(directory):
    """
    Walks through the given directory and returns a list of all .cap files.
    :param directory: Path to directory to search in.
    :return: List of paths to .cap files.
    """
    cap_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.cap'):
                    cap_files.append(os.path.join(root, file))
        if not cap_files:
            print(f"[WARN] No .cap files found in specified directory: {directory}")
    except Exception as e:
        print(f"[ERROR] Failed to find .cap files in {directory}: {e}")
        traceback.print_exc()
    return cap_files

def analyze_handshake(cap_file):
    """
    Analyzes a given .cap file to check if it contains a WPA handshake.
    :param cap_file: Path to the .cap file.
    :return: Boolean indicating if the handshake was found.
    """
    try:
        # Check if the file is empty
        if os.stat(cap_file).st_size == 0:
            print(f"[WARN] Empty .cap file: {cap_file}")
            return False

        packets = rdpcap(cap_file)
        eapol_packets = [pkt for pkt in packets if pkt.haslayer(EAPOL)]
        
        if len(eapol_packets) >= 2:
            print(f"[SUCCESS] Handshake found in {cap_file}")
            return True
        else:
            print(f"[INFO] No handshake found in {cap_file}")
            return False

    except FileNotFoundError:
        print(f"[ERROR] File not found: {cap_file}")
    except Scapy_Exception as scapy_e:
        print(f"[ERROR] Scapy error while reading {cap_file}: {scapy_e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error reading {cap_file}: {e}")
        traceback.print_exc()
    return False

def main():
    directory = os.getcwd()
    print(f"[INFO] Searching for .cap files in directory: {directory}")

    cap_files = find_cap_files(directory)

    if not cap_files:
        print("[ERROR] No .cap files found. Exiting...")
        return

    handshake_count = 0

    for cap_file in cap_files:
        if analyze_handshake(cap_file):
            handshake_count += 1

    print(f"[INFO] Total .cap files analyzed: {len(cap_files)}")
    print(f"[INFO] Handshakes found: {handshake_count}")

if __name__ == "__main__":
    main()
