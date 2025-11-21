import os

DOMAIN = "dihmail.org"
ADDRESS_SEPARATOR = ":dih:"
RANDOM_LOCAL_LENGTH = 24

DEFAULT_DB_FILE = "dihmail.db"
WEB_DB_CANDIDATE = os.path.join("dihmail_server_deploy", "dihmail.db")
DB_FILE = os.environ.get("DIHMAIL_DB_FILE") or (WEB_DB_CANDIDATE if os.path.exists(WEB_DB_CANDIDATE) else DEFAULT_DB_FILE)

MASTER_KEY_FILE = "master.key"
LEGACY_DOMAINS = ["dihmail.co"]
