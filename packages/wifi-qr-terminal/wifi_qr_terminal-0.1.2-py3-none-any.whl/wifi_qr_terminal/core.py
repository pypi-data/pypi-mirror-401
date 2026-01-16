import platform
import subprocess
import re
import sys
import qrcode
import io

class WiFiError(Exception):
    pass

def get_wifi_credentials():
    system = platform.system()
    if system == "Windows":
        return _get_windows_credentials()
    elif system == "Darwin":
        return _get_macos_credentials()
    elif system == "Linux":
        return _get_linux_credentials()
    else:
        raise WiFiError(f"Unsupported operating system: {system}")

def _get_windows_credentials():
    # 1. Get current connected SSID
    try:
        # 'netsh wlan show interfaces' is reliable for finding the connected SSID
        output = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='utf-8', errors='ignore')
        ssid_match = re.search(r"^\s*SSID\s*:\s*(.*)$", output, re.MULTILINE)
        if not ssid_match:
            raise WiFiError("Could not determine current Wi-Fi SSID. Are you connected?")
        ssid = ssid_match.group(1).strip()
        
        # 2. Get password for that SSID
        # 'netsh wlan show profile name="SSID" key=clear'
        profile_cmd = f'netsh wlan show profile name="{ssid}" key=clear'
        profile_output = subprocess.check_output(profile_cmd, shell=True, encoding='utf-8', errors='ignore')
        
        # Look for "Key Content            : password"
        pass_match = re.search(r"^\s*Key Content\s*:\s*(.*)$", profile_output, re.MULTILINE)
        if not pass_match:
             # It might be an open network or we don't have permission to see the key
             # But on Windows, if it's your profile, you usually see it.
             # Check if authentication is Open
             auth_match = re.search(r"^\s*Authentication\s*:\s*Open", profile_output, re.MULTILINE)
             if auth_match:
                 return ssid, "", "nopass"
             raise WiFiError("Could not retrieve password. Make sure you are running as Administrator if needed.")
        
        password = pass_match.group(1).strip()
        return ssid, password, "WPA" # Assuming WPA/WPA2 as default for secured networks
        
    except subprocess.CalledProcessError as e:
        raise WiFiError(f"Failed to execute netsh: {e}")

def _get_macos_credentials():
    try:
        # 1. Get current SSID
        # /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I
        # OR networksetup -getairportnetwork en0 (but en0 isn't always wifi)
        # Using networksetup is safer for standard PATH, but might need device name.
        # Let's try finding the device first.
        nw_list = subprocess.check_output(["networksetup", "-listallhardwareports"], encoding='utf-8')
        wifi_device = None
        lines = nw_list.split('\n')
        for i, line in enumerate(lines):
            if "Wi-Fi" in line:
                # The next line usually has 'Device: en0'
                dev_line = lines[i+1]
                match = re.search(r"Device: (.*)", dev_line)
                if match:
                    wifi_device = match.group(1).strip()
                    break
        
        if not wifi_device:
            # Fallback to en0
            wifi_device = "en0"

        ssid_output = subprocess.check_output(["networksetup", "-getairportnetwork", wifi_device], encoding='utf-8')
        # Output format: "Current Wi-Fi Network: MySSID"
        match = re.search(r"Current Wi-Fi Network: (.*)", ssid_output)
        if not match:
             raise WiFiError("Could not determine current Wi-Fi SSID. Are you connected?")
        
        ssid = match.group(1).strip()
        
        # 2. Get Password using security command
        # security find-generic-password -ga "SSID"
        # The password is usually printed to stderr: "password: "xyz""
        cmd = ["security", "find-generic-password", "-wa", ssid]
        
        # Note: This will trigger a system popup!
        try:
            password = subprocess.check_output(cmd, encoding='utf-8', stderr=subprocess.PIPE).strip()
        except subprocess.CalledProcessError:
            raise WiFiError("Could not retrieve password. Access denied to Keychain.")
            
        return ssid, password, "WPA"

    except subprocess.CalledProcessError as e:
        raise WiFiError(f"System command failed: {e}")

def _get_linux_credentials():
    try:
        # Using nmcli
        # 1. Get active connection SSID
        # nmcli -t -f active,ssid dev wifi | grep '^yes'
        output = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], encoding='utf-8')
        ssid = None
        for line in output.splitlines():
            if line.startswith("yes:"):
                ssid = line.split(":", 1)[1]
                break
        
        if not ssid:
             raise WiFiError("Could not determine current Wi-Fi SSID (nmcli).")

        # 2. Get password
        # nmcli -s -g 802-11-wireless-security.psk connection show "SSID"
        # This requires permissions.
        try:
             password = subprocess.check_output(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid], encoding='utf-8').strip()
        except subprocess.CalledProcessError:
             raise WiFiError("Could not retrieve password. Try running with 'sudo'.")
        
        return ssid, password, "WPA"

    except FileNotFoundError:
        raise WiFiError("nmcli not found. Ensure NetworkManager is installed.")
    except subprocess.CalledProcessError as e:
        raise WiFiError(f"nmcli command failed: {e}")

def generate_qr_code_ascii(ssid, password, auth_type="WPA"):
    # Schema: WIFI:T:WPA;S:MyNetwork;P:mypass;;
    # Special characters in SSID/Pass need escaping? Actually the standard is simple:
    # colon, semicolon, comma need escaping with backslash.
    # But qrcode lib handles byte generation. We just need the string.
    
    def escape(s):
        return s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace(':', '\\:')

    if auth_type == "nopass":
        wifi_str = f"WIFI:T:nopass;S:{escape(ssid)};;"
    else:
        wifi_str = f"WIFI:T:{auth_type};S:{escape(ssid)};P:{escape(password)};;"
    
    qr = qrcode.QRCode()
    qr.add_data(wifi_str)
    qr.make(fit=True)
    
    # Render to string
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read(), wifi_str
