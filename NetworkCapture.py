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

def capture_network(wireless_adapter_name):
    process = subprocess.Popen(['airodump-ng', wireless_adapter_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    print("Starting network scan... (Press Ctrl+C to stop)")

    try:
        for line in iter(process.stdout.readline, b''):  # Use iter to read lines until empty
            output = line.decode('utf-8')
            print(output.strip())

    except KeyboardInterrupt:
        print("\nStopping network scan...")
        process.kill()

    finally:
        process.wait()




