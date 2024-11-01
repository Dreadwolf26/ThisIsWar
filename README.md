# **ThisIsWar: Wardriving Automation**

### **About This Project**

ThisIsWar is a set of scripts that automate **wardriving** and **Wi-Fi penetration testing** tasks. It helps with network monitoring, changing MAC addresses, deauthenticating devices, and capturing WPA/WPA2 handshakes. It’s built for **educational purposes** to help users learn about network security, ethical hacking, and wardriving techniques. I did not include the handshake cracking logic you will need to figure that on your own. I take no liability for the use of these files.

### **What is Wardriving?**

**Wardriving** involves driving around with a Wi-Fi-enabled device to detect and map wireless networks. This project can be used to gather information about available networks and perform basic penetration testing tasks (with permission!).

### **Important Disclaimer**

> **This tool is meant for educational purposes only. Use it responsibly!**  
> The author does **NOT** take any responsibility for how this tool is used. **Do not use this tool to target networks without permission, as it is illegal and unethical.** Misusing these scripts could get you into serious legal trouble. Always have explicit permission before testing or mapping any network!

### **Requirements**

To run these scripts, you’ll need:

1. A **Linux-based OS** (e.g., Ubuntu, Kali Linux).
2. **Root permissions** (most operations require them).
3. Install the following packages:
   - **Aircrack-ng:** For Wi-Fi monitoring, attacks, and wardriving.
     ```bash
     sudo apt-get update
     sudo apt-get install aircrack-ng
     ```
   - **macchanger:** For changing the MAC address.
     ```bash
     sudo apt-get install macchanger
     ```

### **How to Set It Up**

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Dreadwolf26/ThisIsWar.git
   ```
2. Go into the project directory:
   ```bash
   cd ThisIsWar
   ```

### **Finding Your Wireless Adapter Name**

Before using these scripts, you need to identify your wireless adapter's name:

1. **Run the following command in your terminal:**
   ```bash
   iwconfig
   ```
2. You’ll see a list of network interfaces. Look for the interface that shows Wi-Fi properties (e.g., signal strength, mode, frequency). Common names include `wlan0`, `wlp2s0`, or similar.

### **Updating the Adapter Name in the Scripts**

To make these scripts work, you need to update the adapter name directly in the script files:

1. **Open `network_capture.py` in a text editor:**
   ```bash
   nano network_capture.py
   ```
2. **Find the line:**
   ```python
   WIRELESS_ADAPTER = 'default_adapter_name'
   ```
3. Replace `'default_adapter_name'` with the name of your wireless adapter (e.g., `'wlan0'` or `'wlp2s0'`).

**Repeat the same process in `deauth.py` and `mac_change.py`:**

1. **Open each file:**
   ```bash
   nano deauth.py
   ```
   ```bash
   nano mac_change.py
   ```
2. **Find and update the line in both files:**
   ```python
   WIRELESS_ADAPTER = 'default_adapter_name'
   ```
3. Replace `'default_adapter_name'` with your actual adapter name, as found using `iwconfig`.

### **How to Use**

#### **Run the Main Script**

Once you’ve updated the adapter name, you can run the main script to start the automation process, which includes enabling monitor mode, changing MAC addresses, detecting and mapping networks, deauthenticating devices, and attempting handshake captures:

```bash
sudo python3 main.py
```

#### **What Each Script Does**

- **`network_capture.py`:** Puts your adapter in monitor mode, captures network data, and extracts BSSIDs and channels from detected networks.
- **`deauth.py`:** Deauthenticates devices connected to target networks and attempts to capture WPA/WPA2 handshakes.
- **`mac_change.py`:** Changes the MAC address of your Wi-Fi adapter before proceeding with the next deauthentication attempt.
- **`main.py`:** Brings everything together to automate wardriving and Wi-Fi penetration testing.

### **Be Responsible**

- **Only use this tool on networks you own or have explicit permission to test and map.**
- The primary goal is to enhance your skills in network security while respecting privacy and legal boundaries.
- **Wardriving should be conducted responsibly**—comply with local laws and always respect others' privacy.

### **Future Ideas**

- Implement a GUI to make the process more user-friendly.
- Improve error handling for more reliable automation.
- implement captured data clean up. Alot of file generate through the process. I will find a way to automate, clean and compile the captured handshakes. I will leave the .kismet data as is. 
- Adding GPS locations for visulaization

### **Contributing**

Contributions are welcome! If you have ideas to improve **ThisIsWar**, feel free to fork the repo, make changes, and submit a pull request.

### **License**

This project is under the MIT License. See the `LICENSE` file for details.
