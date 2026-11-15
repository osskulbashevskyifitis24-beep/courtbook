import re
import sqlite3


def register_user(email, password, name, phone, db_path):
    # validate email
    if email is None or email == "":
        return {"ok": False, "error": "Email is required"}
    if len(email) > 254:
        return {"ok": False, "error": "Email is too long"}
    if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", email):
        return {"ok": False, "error": "Invalid email"}
    # validate password
    if password is None or len(password) < 8:
        return {"ok": False, "error": "Password too short"}
    has_upper = False
    has_digit = False
    for ch in password:
        if ch.isupper():
            has_upper = True
        if ch.isdigit():
            has_digit = True
    if not has_upper or not has_digit:
        return {"ok": False, "error": "Weak password"}
    # validate phone
    if phone:
        if not phone.startswith("+380") or len(phone) != 13:
            return {"ok": False, "error": "Invalid phone"}
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        return {"ok": False, "error": "User already exists"}
    # TODO: hash password
    cur.execute(
        "INSERT INTO users (email, name, phone, password_hash, salt, role) VALUES (?, ?, ?, ?, ?, ?)",
        (email, name, phone, password, "", "client"),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return {"ok": True, "user_id": user_id}


def login_user(email, password, db_path):
    if email is None or email == "":
        return {"ok": False, "error": "Email is required"}
    if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", email):
        return {"ok": False, "error": "Invalid email"}
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, salt FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"ok": False, "error": "Invalid credentials"}
    if password != row[1]:
        return {"ok": False, "error": "Invalid credentials"}
    return {"ok": True, "user_id": row[0]}
