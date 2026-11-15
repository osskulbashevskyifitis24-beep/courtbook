import sqlite3

from .security import hash_password, verify_password
from .validation import ValidationError, validate_email, validate_registration

DEFAULT_ROLE = "client"


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
    password_hash, salt = hash_password(password)
    cur.execute(
        "INSERT INTO users (email, name, phone, password_hash, salt, role) VALUES (?, ?, ?, ?, ?, ?)",
        (email.lower(), name, phone, password_hash, salt, DEFAULT_ROLE),
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
    if row is None or not verify_password(password, row[1], row[2]):
        return {"ok": False, "error": "Invalid credentials"}
    return {"ok": True, "user_id": row[0]}
