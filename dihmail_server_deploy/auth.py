import bcrypt
from db import create_user, find_user

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def register_user(local: str, password: str) -> int:
    existing = find_user(local)
    if existing:
        raise ValueError("User already exists")
    hashed = hash_password(password)
    return create_user(local, hashed)

def authenticate_user(local: str, password: str) -> bool:
    user = find_user(local)
    if not user:
        return False
    password_hash = user[2]
    if not password_hash:
        return False
    return verify_password(password, password_hash)
