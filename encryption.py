import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from config import MASTER_KEY_FILE

KEY_BYTES = 32  # AES-256
NONCE_BYTES = 12  # Recommended size for GCM
WRAPPED_PREFIX = "v2:"

def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8")

def b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data.encode("utf-8"))

def _load_master_key() -> bytes:
    # Prefer environment variable (base64-encoded 32 bytes)
    env = os.environ.get("DIHMAIL_MASTER_KEY", "").strip()
    if env:
        key = b64decode(env)
        if len(key) != KEY_BYTES:
            raise ValueError("DIHMAIL_MASTER_KEY must be base64 of 32 bytes")
        return key
    # Fall back to persistent file for stable key across restarts
    if os.path.exists(MASTER_KEY_FILE):
        with open(MASTER_KEY_FILE, "rb") as f:
            data = f.read().strip()
            try:
                key = base64.urlsafe_b64decode(data)
            except Exception:
                # If file stores raw bytes (older/manual), accept directly
                key = data
        if len(key) != KEY_BYTES:
            raise ValueError("master.key must contain 32 bytes (or base64 thereof)")
        return key
    # Create new random key and persist as base64
    key = os.urandom(KEY_BYTES)
    with open(MASTER_KEY_FILE, "wb") as f:
        f.write(base64.urlsafe_b64encode(key))
    return key

def _wrap_key(plain_key: bytes) -> str:
    master = _load_master_key()
    nonce = os.urandom(NONCE_BYTES)
    cipher = Cipher(algorithms.AES(master), modes.GCM(nonce), backend=default_backend())
    enc = cipher.encryptor()
    ckey = enc.update(plain_key) + enc.finalize()
    tag = enc.tag
    # Store as WRAPPED_PREFIX + nonce:tag:cipherkey (base64 urlsafe)
    return WRAPPED_PREFIX + ":".join([b64(nonce), b64(tag), b64(ckey)])

def _unwrap_key(wrapped: str) -> bytes:
    assert wrapped.startswith(WRAPPED_PREFIX)
    master = _load_master_key()
    _, payload = wrapped.split(WRAPPED_PREFIX, 1)
    parts = payload.split(":")
    if len(parts) != 3:
        raise ValueError("Invalid wrapped key format")
    nonce_b64, tag_b64, ckey_b64 = parts
    nonce = b64decode(nonce_b64)
    tag = b64decode(tag_b64)
    ckey = b64decode(ckey_b64)
    cipher = Cipher(algorithms.AES(master), modes.GCM(nonce, tag), backend=default_backend())
    dec = cipher.decryptor()
    pkey = dec.update(ckey) + dec.finalize()
    if len(pkey) != KEY_BYTES:
        raise ValueError("Unwrapped key has invalid length")
    return pkey

def encrypt_message(plaintext: str) -> dict:
    key = os.urandom(KEY_BYTES)
    nonce = os.urandom(NONCE_BYTES)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
    tag = encryptor.tag
    return {
        "ciphertext": b64(ciphertext),
        # Store per-message key encrypted-at-rest using server master key
        "key": _wrap_key(key),
        "nonce": b64(nonce),
        "tag": b64(tag),
    }

def decrypt_message(ciphertext_b64: str, key_b64: str, nonce_b64: str, tag_b64: str) -> str:
    # Backward-compatible: if not wrapped with WRAPPED_PREFIX, treat as legacy raw key
    if key_b64.startswith(WRAPPED_PREFIX):
        key = _unwrap_key(key_b64)
    else:
        key = b64decode(key_b64)
    nonce = b64decode(nonce_b64)
    tag = b64decode(tag_b64)
    ciphertext = b64decode(ciphertext_b64)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode("utf-8")
