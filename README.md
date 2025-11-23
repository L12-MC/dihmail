# dihmail 🥀🥀

A minimal experimental encrypted messaging system with custom address format and symmetric encryption.

Address format: `<local>:dih:dihmail.org`
Example: `bA4rDhf3df8Jr8f3jJ34ucU:dih:dihmail.org`

Each user has a primary local part (e.g. `alice`) which is internally mapped to a primary address `alice:dih:dihmail.org`. Random disposable aliases can be generated that route to the primary.

Legacy addresses (`*:dih:dihmail.co`) remain valid for delivery; the system accepts both domains.

Encryption: Messages are encrypted with a freshly generated symmetric AES-256-GCM key. The per‑message key is now itself encrypted (“wrapped”) using a server master key (AES-256-GCM) and stored in wrapped form (prefix `v2:`). Legacy messages created before key wrapping still decrypt normally. This remains a demonstration system and should not be considered production‑secure.

## Installation

Install dependencies:
Install dependencies (Windows batch scripts and Linux shell versions are in `scripts/`):

```powershell
pip install -r requirements.txt
pip install pyinstaller
```

Or use the helper script (from project root):
```powershell
scripts\install.bat
```
Linux:
```bash
cd scripts
bash install.sh
```


Optional: point the application at a specific database file (shared web instance) by setting `DIHMAIL_DB_FILE` before starting:

```powershell
$env:DIHMAIL_DB_FILE = "C:\\path\\to\\shared\\dihmail.db"
python app.py
```

If unset, the app will auto-use `dihmail_server_deploy/dihmail.db` when that file exists, otherwise the local `dihmail.db` in the root folder.

## Web Application

Start the web server:

```powershell
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

Features:
- **Register**: Create a new account with username and password
- **Login**: Authenticate with bcrypt-hashed passwords
- **Dashboard**: View your primary address and generate random aliases
- **Send**: Send encrypted messages to any dihmail address
- **Inbox**: View received messages
- **Decrypt**: View decrypted message contents

The logo (`dihmail.png`) is displayed in the header of all pages.

## CLI Usage (Alternative)

Commands (PowerShell examples):

```powershell
python cli.py create-user alice
python cli.py alias alice
python cli.py send alice bA4rDhf3df8Jr8f3jJ34ucU:dih:dihmail.org "Hello encrypted world"
python cli.py inbox alice
```

Other commands:
- `rawmsg <message_id>`: show stored raw entry
- `decrypt <message_id>`: decrypt and show plaintext

**Note**: CLI user creation no longer supports password authentication. Use the web app for user registration with password protection.

## Security Caveats
- Per-message symmetric key is stored wrapped with a static server master key (improves at-rest posture but master key compromise exposes all messages).
- Legacy messages may store raw keys (still supported).
- No authentication, rate limiting, or spam controls beyond basic login.
- No forward secrecy, no multi-device key isolation, no metadata protection.
- Treat this as an educational prototype only.

### Master Key Management
Set an environment variable with a base64 32‑byte key before starting the server:

```powershell
$raw = [byte[]]::new(32); (New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes($raw);
$env:DIHMAIL_MASTER_KEY = [Convert]::ToBase64String($raw)
python app.py
```

If `DIHMAIL_MASTER_KEY` is absent, a `master.key` file is generated automatically.

