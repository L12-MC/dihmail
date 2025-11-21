from address import build_address, generate_random_address, extract_local, is_valid_address
from db import create_user, find_user, create_alias, find_alias, store_message, list_messages_for_user, get_message
from encryption import encrypt_message, decrypt_message
from typing import Optional, Dict

# Primary user address is just local part; address built when displayed.

def ensure_user(local: str):
    existing = find_user(local)
    if existing:
        return existing[0]
    return create_user(local)

def new_alias_for_user(user_local: str) -> str:
    user = find_user(user_local)
    if not user:
        raise ValueError("User does not exist")
    random_addr = generate_random_address()
    rand_local = extract_local(random_addr)
    create_alias(user[0], rand_local)
    return random_addr

def resolve_recipient(addr: str) -> Optional[str]:
    if not is_valid_address(addr):
        return None
    local = extract_local(addr)
    # If local matches a primary user
    user = find_user(local)
    if user:
        return user[1]
    # If local matches an alias, map back to the owning user's primary local
    alias = find_alias(local)
    if alias:
        owner_id = alias[1]
        # fetch owner
        # naive second lookup
        for_primary = find_user_by_id(owner_id)
        return for_primary[1] if for_primary else None
    return None

def find_user_by_id(uid: int):
    # Simple helper; not exported in db
    import sqlite3
    from config import DB_FILE
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, local, password_hash FROM users WHERE id=?", (uid,))
    row = cur.fetchone()
    conn.close()
    return row

def send_message(sender_local: str, recipient_addr: str, plaintext: str) -> Dict:
    # sender must exist
    if not find_user(sender_local):
        raise ValueError("Sender does not exist")
    resolved = resolve_recipient(recipient_addr)
    if not resolved:
        raise ValueError("Recipient address not found")
    payload = encrypt_message(plaintext)
    mid = store_message(sender_local, resolved, payload)
    return {"message_id": mid, **payload}

def get_inbox(user_local: str):
    if not find_user(user_local):
        raise ValueError("User does not exist")
    return list_messages_for_user(user_local)

def get_message_detail(mid: int):
    row = get_message(mid)
    if not row:
        raise ValueError("Message not found")
    keys = ["id","sender_local","recipient_local","ciphertext","key","nonce","tag","created_at"]
    return dict(zip(keys,row))

def decrypt_message_id(mid: int) -> str:
    detail = get_message_detail(mid)
    return decrypt_message(detail["ciphertext"], detail["key"], detail["nonce"], detail["tag"])
