#!/usr/bin/env python3
"""
Generate encrypted password for SQL update.
Run this locally with TOKEN_ENCRYPTION_KEY set.
"""
import os
from cryptography.fernet import Fernet

password = "AVrYTecGag7hXwl5CgI3"
encryption_key = os.environ.get("TOKEN_ENCRYPTION_KEY")

if not encryption_key:
    print("ERROR: TOKEN_ENCRYPTION_KEY not set")
    print("Get it from: render env-vars list -s srv-d50p4ns9c44c738capjg")
    exit(1)

fernet = Fernet(encryption_key.encode())
encrypted = fernet.encrypt(password.encode())

print(f"Encrypted password (hex): {encrypted.hex()}")
print(f"\nSQL command:")
print(f"UPDATE personal_bots SET encrypted_password = '\\x{encrypted.hex()}' WHERE user_id = 'vikunja:ivan';")

