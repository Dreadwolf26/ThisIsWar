import csv
import re

def parse_csv(filepath, log_callback=None):
    """
    Parse the CSV file to retrieve AP and client information.
    :param filepath: Path to the CSV file.
    :param log_callback: Optional logging function.
    :return: Tuple of (ap_list, client_list).
    """
    ap_list = []
    client_list = []

    def log(message):
        if log_callback:
            log_callback(message)
        else:
            print(message)

    try:
        with open(filepath, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            client_section = False

            for row in csvreader:
                # Skip empty or malformed rows
                if not row or len(row) < 4:
                    continue

                # Start of client section
                if row[0].strip() == "Station MAC":
                    client_section = True
                    continue

                if client_section:
                    # Parsing clients
                    if len(row) > 5:
                        client_mac = row[0].strip()
                        ap_bssid = row[5].strip()

                        # Validate MAC addresses
                        if validate_mac(client_mac) and validate_mac(ap_bssid):
                            client_list.append((client_mac, ap_bssid))
                else:
                    # Parsing APs
                    bssid = row[0].strip()
                    channel = row[3].strip()

                    # Validate BSSID and channel
                    if validate_mac(bssid):
                        try:
                            channel = str(int(channel))  # Ensure channel is an integer string
                            ap_list.append((bssid, channel))
                        except ValueError:
                            log(f"[WARN] Skipping AP with invalid channel value: {channel}")

    except FileNotFoundError:
        log(f"[ERROR] File not found: {filepath}")
    except Exception as e:
        log(f"[ERROR] Unexpected error while parsing CSV: {e}")

    return ap_list, client_list

def validate_mac(mac_address):
    """
    Validate a MAC address.
    :param mac_address: MAC address to validate.
    :return: Boolean indicating if the MAC address is valid.
    """
    mac_pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
    return bool(re.match(mac_pattern, mac_address))

if __name__ == "__main__":
    # Example usage
    ap_list, client_list = parse_csv("network_capture-01.csv")
    print("[INFO] Access Points:", ap_list)
    print("[INFO] Clients:", client_list)
