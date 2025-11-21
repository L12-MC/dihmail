# dihmail

A minimal experimental encrypted messaging system with custom address format and symmetric encryption.

Address format: `<randomLocal>:dih:domain.com`
Example: `bA4rDhf3df8Jr8f3jJ34ucU:dih:domain.com`

Each user has a primary local part (e.g. `alice`) which is internally mapped to a primary address `alice:dih:domain.com`. Random disposable aliases can be generated that route to the primary.

Encryption: Messages are encrypted with a freshly generated symmetric AES-256-GCM key. The base64-encoded key, nonce and tag are stored and returned alongside the ciphertext (this COMPLETELY removes confidentiality against the storage provider and is for demonstration only). Do NOT use this architecture for real secure messaging.

## Installation

Install dependencies:

```powershell
pip install -r requirements.txt
```

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
python cli.py send alice bA4rDhf3df8Jr8f3jJ34ucU:dih:domain.com "Hello encrypted world"
python cli.py inbox alice
```

Other commands:
- `rawmsg <message_id>`: show stored raw entry
- `decrypt <message_id>`: decrypt and show plaintext

**Note**: CLI user creation no longer supports password authentication. Use the web app for user registration with password protection.

## Security Caveats
- The symmetric key is stored with the message; this is insecure.
- No authentication, rate limiting, or spam controls.
- AES-GCM is used correctly for integrity, but key handling defeats the purpose.

## License
No license specified. Use at your own risk.
