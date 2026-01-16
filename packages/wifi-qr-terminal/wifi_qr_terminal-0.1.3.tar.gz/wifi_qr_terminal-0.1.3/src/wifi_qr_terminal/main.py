import platform
import subprocess
import re
import sys
import qrcode
import io
from rich.console import Console
from rich.panel import Panel

console = Console()

class WiFiError(Exception):
    pass

def get_wifi_credentials():
    system = platform.system()
    if system == "Windows":
        return _get_windows_credentials()
    elif system == "Darwin": # macOS
        return _get_macos_credentials()
    elif system == "Linux":
        return _get_linux_credentials()
    else:
        raise WiFiError(f"Unsupported operating system: {system}")

def _get_windows_credentials():
    try:
        output = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='utf-8', errors='ignore')
        ssid_match = re.search(r"^\s*SSID\s*:\s*(.*)$", output, re.MULTILINE)
        if not ssid_match:
            raise WiFiError("Could not determine current Wi-Fi SSID. Are you connected?")
        ssid = ssid_match.group(1).strip()
        
        profile_cmd = f'netsh wlan show profile name="{ssid}" key=clear'
        profile_output = subprocess.check_output(profile_cmd, shell=True, encoding='utf-8', errors='ignore')
        
        pass_match = re.search(r"^\s*Key Content\s*:\s*(.*)$", profile_output, re.MULTILINE)
        if not pass_match:
             auth_match = re.search(r"^\s*Authentication\s*:\s*Open", profile_output, re.MULTILINE)
             if auth_match:
                 return ssid, "", "nopass"
             raise WiFiError("Could not retrieve password. Run as Administrator?")
        
        password = pass_match.group(1).strip()
        return ssid, password, "WPA"
        
    except subprocess.CalledProcessError as e:
        raise WiFiError(f"Failed to execute netsh: {e}")

def _get_macos_credentials():
    try:
        # Find the WiFi Device (usually en0)
        nw_list = subprocess.check_output(["networksetup", "-listallhardwareports"], encoding='utf-8')
        wifi_device = "en0" # Fallback
        lines = nw_list.split('\n')
        for i, line in enumerate(lines):
            if "Wi-Fi" in line:
                dev_line = lines[i+1]
                match = re.search(r"Device: (.*)", dev_line)
                if match:
                    wifi_device = match.group(1).strip()
                    break
        
        ssid_output = subprocess.check_output(["networksetup", "-getairportnetwork", wifi_device], encoding='utf-8')
        match = re.search(r"Current Wi-Fi Network: (.*)", ssid_output)
        if not match:
             raise WiFiError("Could not determine current Wi-Fi SSID. Are you connected?")
        
        ssid = match.group(1).strip()
        
        # Note: This usually triggers a system popup asking for permission
        cmd = ["security", "find-generic-password", "-wa", ssid]
        try:
            password = subprocess.check_output(cmd, encoding='utf-8', stderr=subprocess.PIPE).strip()
        except subprocess.CalledProcessError:
            raise WiFiError("Access denied to Keychain. Could not retrieve password.")
            
        return ssid, password, "WPA"

    except subprocess.CalledProcessError as e:
        raise WiFiError(f"System command failed: {e}")

def _get_linux_credentials():
    try:
        output = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], encoding='utf-8')
        ssid = None
        for line in output.splitlines():
            if line.startswith("yes:"):
                ssid = line.split(":", 1)[1]
                break
        
        if not ssid:
             raise WiFiError("Could not determine current Wi-Fi SSID (nmcli).")

        try:
             password = subprocess.check_output(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid], encoding='utf-8').strip()
        except subprocess.CalledProcessError:
             raise WiFiError("Permission denied. Try running with 'sudo'.")
        
        return ssid, password, "WPA"

    except FileNotFoundError:
        raise WiFiError("nmcli not found. Ensure NetworkManager is installed.")
    except subprocess.CalledProcessError as e:
        raise WiFiError(f"nmcli command failed: {e}")

def generate_qr_code_ascii(ssid, password, auth_type="WPA"):
    def escape(s):
        return s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace(':', '\\:')

    if auth_type == "nopass":
        wifi_str = f"WIFI:T:nopass;S:{escape(ssid)};;"
    else:
        wifi_str = f"WIFI:T:{auth_type};S:{escape(ssid)};P:{escape(password)};;"
    
    qr = qrcode.QRCode()
    qr.add_data(wifi_str)
    qr.make(fit=True)
    
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read()

def run():
    try:
        console.print("[bold blue]Scanning for Wi-Fi credentials...[/bold blue]")
        ssid, password, auth_type = get_wifi_credentials()
        
        console.print(f"[green]Found SSID:[/green] [bold]{ssid}[/bold]")
        
        qr_ascii = generate_qr_code_ascii(ssid, password, auth_type)
        
        console.print(Panel(qr_ascii, title="Scan Me", subtitle=ssid, expand=False))
        console.print("[dim]Use your phone camera to connect.[/dim]")

    except WiFiError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted.[/yellow]")
        sys.exit(0)

if __name__ == "__main__":
    run()