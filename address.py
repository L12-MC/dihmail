import secrets
import string
from typing import Optional
from config import DOMAIN, ADDRESS_SEPARATOR, RANDOM_LOCAL_LENGTH, LEGACY_DOMAINS

ALPHABET = string.ascii_letters + string.digits

def build_address(local: str) -> str:
    return f"{local}{ADDRESS_SEPARATOR}{DOMAIN}"

def random_local(length: int = RANDOM_LOCAL_LENGTH) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

def generate_random_address() -> str:
    return build_address(random_local())

def is_valid_address(addr: str) -> bool:
    parts = addr.split(ADDRESS_SEPARATOR)
    if len(parts) != 2:
        return False
    local, domain = parts
    if domain != DOMAIN and domain not in LEGACY_DOMAINS:
        return False
    if not local:
        return False
    return True

def extract_local(addr: str) -> Optional[str]:
    if not is_valid_address(addr):
        return None
    return addr.split(ADDRESS_SEPARATOR)[0]
