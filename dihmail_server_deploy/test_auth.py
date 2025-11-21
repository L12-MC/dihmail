from auth import register_user, authenticate_user, hash_password
from db import init_db, find_user
import sqlite3

print("=== Testing Registration and Login Flow ===\n")

# Initialize database
init_db()

# Test user credentials
test_local = "testuser123"
test_password = "mypassword456"

print(f"1. Attempting to register user: {test_local}")
print(f"   Password: {test_password}")

try:
    # Register the user
    user_id = register_user(test_local, test_password)
    print(f"   ✓ User registered successfully with ID: {user_id}")
except ValueError as e:
    print(f"   ✗ Registration failed: {e}")
    # User might already exist, continue with login test

# Verify user was stored
print(f"\n2. Checking database for user: {test_local}")
user = find_user(test_local)
if user:
    print(f"   ✓ User found in database")
    print(f"   - ID: {user[0]}")
    print(f"   - Local: {user[1]}")
    print(f"   - Hash (first 60 chars): {user[2][:60]}")
else:
    print(f"   ✗ User not found in database!")

# Test authentication
print(f"\n3. Testing authentication with correct password")
auth_result = authenticate_user(test_local, test_password)
print(f"   Result: {auth_result}")
if auth_result:
    print(f"   ✓ Authentication successful!")
else:
    print(f"   ✗ Authentication failed!")
    
    # Debug: manually check password
    print("\n   Debug: Manual password verification")
    import bcrypt
    stored_hash = user[2]
    manual_check = bcrypt.checkpw(test_password.encode("utf-8"), stored_hash.encode("utf-8"))
    print(f"   - Manual bcrypt check: {manual_check}")

# Test with wrong password
print(f"\n4. Testing authentication with wrong password")
auth_wrong = authenticate_user(test_local, "wrongpassword")
print(f"   Result: {auth_wrong}")
if not auth_wrong:
    print(f"   ✓ Correctly rejected wrong password")
else:
    print(f"   ✗ ERROR: Accepted wrong password!")

print("\n=== Test Complete ===")
