import sqlite3
from config import DB_FILE

SCHEMA = [
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, local TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS aliases (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, local TEXT UNIQUE NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))",
    "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender_local TEXT NOT NULL, recipient_local TEXT NOT NULL, ciphertext TEXT NOT NULL, key TEXT NOT NULL, nonce TEXT NOT NULL, tag TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
    "CREATE TABLE IF NOT EXISTS attachments (id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER NOT NULL, filename TEXT NOT NULL, mime_type TEXT NOT NULL, key TEXT NOT NULL, ciphertext TEXT NOT NULL, nonce TEXT NOT NULL, tag TEXT NOT NULL, size INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(message_id) REFERENCES messages(id))"
]

def get_conn():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    for stmt in SCHEMA:
        cur.execute(stmt)
    conn.commit()
    conn.close()

def create_user(local: str, password_hash: str = "") -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(local, password_hash) VALUES (?, ?)", (local, password_hash))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

def find_user(local: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, local, password_hash FROM users WHERE local=?", (local,))
    row = cur.fetchone()
    conn.close()
    return row

def update_password_hash(local: str, password_hash: str) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password_hash=? WHERE local=?", (password_hash, local))
    conn.commit()
    conn.close()

def create_alias(user_id: int, local: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO aliases(user_id, local) VALUES (?,?)", (user_id, local))
    conn.commit()
    alias_id = cur.lastrowid
    conn.close()
    return alias_id

def find_alias(local: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, local FROM aliases WHERE local=?", (local,))
    row = cur.fetchone()
    conn.close()
    return row

def store_message(sender_local: str, recipient_local: str, payload: dict) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages(sender_local, recipient_local, ciphertext, key, nonce, tag) VALUES (?,?,?,?,?,?)",
        (sender_local, recipient_local, payload["ciphertext"], payload["key"], payload["nonce"], payload["tag"])
    )
    conn.commit()
    mid = cur.lastrowid
    conn.close()
    return mid

def store_attachment(message_id: int, filename: str, mime_type: str, payload: dict, size: int) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attachments(message_id, filename, mime_type, key, ciphertext, nonce, tag, size) VALUES (?,?,?,?,?,?,?,?)",
        (message_id, filename, mime_type, payload["key"], payload["ciphertext"], payload["nonce"], payload["tag"], size)
    )
    conn.commit()
    aid = cur.lastrowid
    conn.close()
    return aid

def list_attachments(message_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, filename, mime_type, size FROM attachments WHERE message_id=? ORDER BY id", (message_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_attachment(aid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, message_id, filename, mime_type, key, ciphertext, nonce, tag, size, created_at FROM attachments WHERE id=?", (aid,))
    row = cur.fetchone()
    conn.close()
    return row

def list_messages_for_user(primary_local: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, sender_local, recipient_local, created_at FROM messages WHERE recipient_local=? ORDER BY id DESC", (primary_local,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_message(mid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, sender_local, recipient_local, ciphertext, key, nonce, tag, created_at FROM messages WHERE id=?", (mid,))
    row = cur.fetchone()
    conn.close()
    return row
