"""Data access layer for users."""
import sqlite3
from typing import Protocol


class UserRepository(Protocol):
    def find_by_email(self, email: str) -> dict | None: ...
    def create(self, email: str, name: str, phone: str | None,
               password_hash: str, salt: str, role: str) -> int: ...


class SqliteUserRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def find_by_email(self, email):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(row) if row else None

    def create(self, email, name, phone, password_hash, salt, role):
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO users (email, name, phone, password_hash, salt, role) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (email, name, phone, password_hash, salt, role),
            )
            return cur.lastrowid


class InMemoryUserRepository:
    """Stores users in a dict; used in unit tests instead of a real database."""

    def __init__(self):
        self.users = {}

    def find_by_email(self, email):
        return self.users.get(email)

    def create(self, email, name, phone, password_hash, salt, role):
        user_id = len(self.users) + 1
        self.users[email] = {
            "id": user_id, "email": email, "name": name, "phone": phone,
            "password_hash": password_hash, "salt": salt, "role": role,
        }
        return user_id
