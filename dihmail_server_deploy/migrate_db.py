import sqlite3
import os
from config import DB_FILE

def migrate_database():
    """Migrate database to add password_hash column if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        print("No database exists yet - will be created with new schema")
        return
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Check if password_hash column exists
    cur.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cur.fetchall()]
    
    if "password_hash" not in columns:
        print("Migrating database: adding password_hash column...")
        try:
            cur.execute("ALTER TABLE users ADD COLUMN password_hash TEXT NOT NULL DEFAULT ''")
            conn.commit()
            print("Migration successful!")
        except Exception as e:
            print(f"Migration failed: {e}")
            conn.rollback()
    else:
        print("Database already has password_hash column")
    
    conn.close()

if __name__ == "__main__":
    migrate_database()
