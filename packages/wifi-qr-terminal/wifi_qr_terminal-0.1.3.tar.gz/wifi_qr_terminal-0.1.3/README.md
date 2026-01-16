# WiFi QR Terminal

A Python CLI tool that retrieves your currently connected (or stored) Wi-Fi SSID and password, then generates a QR code directly in your terminal. This allows you to easily share your Wi-Fi connection with mobile devices without typing out long passwords.

## Installation

### From PyPI (Recommended for users)
```bash
pip install wifi-qr-terminal
```

### From Source (For development)
```bash
git clone https://github.com/albizzy/wifi-qr-terminal.git
cd wifi-qr-terminal
pip install -e .
```

## Usage

After installation, you can run the tool using the command line:

```bash
wifi-qr
```

### Alternative Execution
If the `wifi-qr` command is not found (common on Windows if your Python Scripts folder is not in your PATH), you can run it directly via Python:

```bash
# Run as a module
python -m wifi_qr_terminal
```

### Options

- `--timeout <seconds>`: Clears the screen and exits after the specified number of seconds. specific for security.
- `--no-color`: Disable colored output (useful for some terminals).
- `--help`: Show help message.

Example with timeout:
```bash
wifi-qr --timeout 30
```

## Troubleshooting

### "Command not found: wifi-qr"
This usually means the directory where Python installs scripts (e.g., `C:\Python3XX\Scripts` on Windows or `~/.local/bin` on Linux) is not in your system's PATH.

**Fix:** Use the module execution method:
```bash
python -m wifi_qr_terminal
```

### "Access denied" / "Permission denied"
- **Windows:** Run your terminal as **Administrator**.
- **macOS:** You will see a popup asking for Keychain access. Click **Allow**.
- **Linux:** Run with `sudo`:
  ```bash
  sudo wifi-qr
  # OR
  sudo python3 -m wifi_qr_terminal
  ```

## OS Support

This tool attempts to auto-detect your OS and use native commands:
- **Windows**: Uses `netsh`
- **macOS**: Uses `security` and `networksetup`
- **Linux**: Uses `nmcli` (NetworkManager)

## Security Note

Passwords are displayed on screen (encoded in the QR). Be aware of your surroundings when running this tool. Use the `--timeout` feature to minimize exposure time.
