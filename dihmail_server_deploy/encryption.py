import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY_BYTES = 32  # AES-256
NONCE_BYTES = 12  # Recommended size for GCM

def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8")

def b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data.encode("utf-8"))

def encrypt_message(plaintext: str) -> dict:
    key = os.urandom(KEY_BYTES)
    nonce = os.urandom(NONCE_BYTES)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
    tag = encryptor.tag
    return {
        "ciphertext": b64(ciphertext),
        "key": b64(key),  # Insecure practice: key returned
        "nonce": b64(nonce),
        "tag": b64(tag),
    }

def decrypt_message(ciphertext_b64: str, key_b64: str, nonce_b64: str, tag_b64: str) -> str:
    key = b64decode(key_b64)
    nonce = b64decode(nonce_b64)
    tag = b64decode(tag_b64)
    ciphertext = b64decode(ciphertext_b64)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode("utf-8")
