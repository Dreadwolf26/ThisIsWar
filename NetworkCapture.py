import subprocess
import time

# Running airmon-ng via subprocess and starting monitor mode

# Printing the names of the wireless interfaces
def scan_adapters():
    result = subprocess.run(['iwconfig'], capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        for line in lines:
            print(line)
        print("Note: Please take note of your wireless adapter, it will be needed in the next step.")

#killing processes so the wireless adpater can be put into monitor mode
def start_monitor_mode():
    subprocess.run(['airmon-ng', 'check', 'kill'])
    print("Killing wireless processes before monitor mode")
    time.sleep(2)
    #starting monitor mode
    wireless_adapter_name = input("Please enter your wireless adapter name here: ")
    subprocess.run(['airmon-ng', 'start', wireless_adapter_name], capture_output=True, text=True)
    print(f"Monitor mode started on {wireless_adapter_name}")
    return wireless_adapter_name

#There is a bug in this one it will get to the first print line but will not run the subprocess to start the network scan
def capture_network(wireless_adapter_name):
    print("Starting network capture...")
    subprocess.run(['sudo','airodump-ng', wireless_adapter_name], capture_output=True, text=True)

#Capturing the scan data to a file
def crack_captured_data():
    capture_file = input("Please enter the name of the capture file (e.g., capture_data.cap): ")
    subprocess.run(['aircrack-ng', '-w', capture_file], capture_output=True, text=True)
    print('Attempting to crack captured data')

