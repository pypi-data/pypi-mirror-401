# WiFi QR Terminal

A Python CLI tool that retrieves your currently connected (or stored) Wi-Fi SSID and password, then generates a QR code directly in your terminal. This allows you to easily share your Wi-Fi connection with mobile devices without typing out long passwords.

## Installation

```bash
pip install wifi-qr-terminal
```

## Usage

Simply run:

```bash
wifi-qr
```

### Options

- `--timeout <seconds>`: Clears the screen and exits after the specified number of seconds. specific for security.
- `--no-color`: Disable colored output (useful for some terminals).
- `--help`: Show help message.

```bash
wifi-qr --timeout 30
```

## OS Support & Permissions

The tool uses system commands to retrieve credentials.

### Windows
Uses `netsh`.
- generally works without Admin if checking the *currently connected* profile or profiles owned by the user.
- If it fails, try running the terminal as Administrator.

### macOS
Uses `security` and `networksetup`.
- You will likely see a system popup asking for permission to access the Keychain to retrieve the Wi-Fi password. This is normal macOS security behavior.
- Click "Allow" to proceed.

### Linux
Uses `nmcli` (NetworkManager).
- Typically does not require `sudo` if the user has permissions to view network secrets, but on some systems/distros, you might need to run:
  ```bash
  sudo wifi-qr
  ```

## Security Note

Passwords are displayed on screen (encoded in the QR). Be aware of your surroundings when running this tool. Use the `--timeout` feature to minimize exposure time.
