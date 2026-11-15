"""Business logic for registration and login (US-001, US-002)."""
from .repository import SqliteUserRepository, UserRepository
from .security import hash_password, verify_password
from .validation import ValidationError, validate_email, validate_registration

DEFAULT_ROLE = "client"


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, email: str, password: str, name: str, phone: str | None = None) -> dict:
        try:
            validate_registration(email, password, phone)
        except ValidationError as e:
            return {"ok": False, "error": str(e)}
        normalized = email.lower()
        if self.repository.find_by_email(normalized):
            return {"ok": False, "error": "User already exists"}
        password_hash, salt = hash_password(password)
        user_id = self.repository.create(normalized, name, phone, password_hash, salt, DEFAULT_ROLE)
        return {"ok": True, "user_id": user_id}

    def login(self, email: str, password: str) -> dict:
        if not validate_email(email):
            return {"ok": False, "error": "Invalid email"}
        user = self.repository.find_by_email(email.lower())
        if user is None or not verify_password(password, user["password_hash"], user["salt"]):
            return {"ok": False, "error": "Invalid credentials"}
        return {"ok": True, "user_id": user["id"]}


def register_user(email, password, name, phone, db_path):
    return AuthService(SqliteUserRepository(db_path)).register(email, password, name, phone)


def login_user(email, password, db_path):
    return AuthService(SqliteUserRepository(db_path)).login(email, password)
