import hashlib
import hmac
import os
import sqlite3

from .validation import ValidationError, validate_email, validate_registration


def register_user(email, password, name, phone, db_path):
    try:
        validate_registration(email, password, phone)
    except ValidationError as e:
        return {"ok": False, "error": str(e)}
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
    if cur.fetchone():
        conn.close()
        return {"ok": False, "error": "User already exists"}
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    cur.execute(
        "INSERT INTO users (email, name, phone, password_hash, salt, role) VALUES (?, ?, ?, ?, ?, ?)",
        (email.lower(), name, phone, pwd_hash.hex(), salt.hex(), "client"),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return {"ok": True, "user_id": user_id}


def login_user(email, password, db_path):
    if not validate_email(email):
        return {"ok": False, "error": "Invalid email"}
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, salt FROM users WHERE email = ?", (email.lower(),))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"ok": False, "error": "Invalid credentials"}
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(row[2]), 100000)
    if not hmac.compare_digest(pwd_hash.hex(), row[1]):
        return {"ok": False, "error": "Invalid credentials"}
    return {"ok": True, "user_id": row[0]}
