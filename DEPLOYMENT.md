# DIH MAIL - Server Deployment Guide

## Quick Start

### 1. Desktop Application (Standalone .exe)
Run: `DihMail.exe`
- No Python required
- Works offline with local database
- Share `dihmail.db` file to sync between computers

### 2. Web Server (Broken)
Run: `python app.py` or `start_server.bat`
- Access from any browser: `http://SERVER-IP:5000`
- Multiple users can connect simultaneously
- Web interface with dark mode

## Files

### Client Application
- `DihMail.exe` - Standalone desktop app (no install needed)
- `dihmail.db` - Database (users, messages, aliases)

### Web Server
- `app.py` - Flask web server
- `start_server.bat` - Start web server script
- `templates/` - Web interface HTML
- `static/` - CSS, images, icons

## Network Setup

### Option 1: Shared Database (Desktop App)
1. Copy entire `DihMail` folder to network share
2. All users run `DihMail.exe` from network
3. Everyone shares the same `dihmail.db`

### Option 2: Web Server (Any Device)
1. Run `start_server.bat` on one computer
2. Find server IP: `ipconfig` (look for IPv4)
3. Open browser on any device: `http://SERVER-IP:5000`
4. Register/Login and use from anywhere

### Option 3: Cloud Server
Upload entire folder to server and run:
```bash
python app.py
```
Access from internet (configure firewall/port forwarding).

## Database Location

Default: `dihmail.db` in same folder as executable

To use network database, edit `config.py`:
```python
DB_FILE = "\\\\SERVER\\SharedFolder\\dihmail.db"  # Windows
DB_FILE = "/mnt/share/dihmail.db"  # Linux
```

## Security Notes

- Change Flask secret key in `app.py` for production
- Use HTTPS for internet deployment
- Passwords are bcrypt-hashed
- Messages encrypted with AES-256-GCM
- **Warning**: Encryption key stored with message (demo only)

## Requirements (for running from source)

```
pip install -r requirements.txt
```

- Python 3.12+
- Flask, bcrypt, cryptography, PySide6

## Support

Encrypted email system with:
- User authentication
- Random disposable aliases
- AES-256-GCM encryption
- Desktop GUI & Web interface
