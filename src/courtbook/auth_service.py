"""Business logic for registration and login (US-001, US-002)."""
from .repository import SqliteUserRepository, UserRepository
from .security import hash_password, verify_password
from .validation import ValidationError, validate_email, validate_registration

DEFAULT_ROLE = "client"


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, email: str, password: str, name: str, phone: str | None = None) -> int:
        validate_registration(email, password, phone)
        normalized = email.lower()
        if self.repository.find_by_email(normalized):
            raise UserAlreadyExistsError(normalized)
        password_hash, salt = hash_password(password)
        return self.repository.create(normalized, name, phone, password_hash, salt, DEFAULT_ROLE)

    def login(self, email: str, password: str) -> int:
        if not validate_email(email):
            raise ValidationError("Invalid email")
        user = self.repository.find_by_email(email.lower())
        if user is None or not verify_password(password, user["password_hash"], user["salt"]):
            raise InvalidCredentialsError()
        return user["id"]


def register_user(email, password, name, phone, db_path):
    try:
        user_id = AuthService(SqliteUserRepository(db_path)).register(email, password, name, phone)
    except ValidationError as e:
        return {"ok": False, "error": str(e)}
    except UserAlreadyExistsError:
        return {"ok": False, "error": "User already exists"}
    return {"ok": True, "user_id": user_id}


def login_user(email, password, db_path):
    try:
        user_id = AuthService(SqliteUserRepository(db_path)).login(email, password)
    except ValidationError as e:
        return {"ok": False, "error": str(e)}
    except InvalidCredentialsError:
        return {"ok": False, "error": "Invalid credentials"}
    return {"ok": True, "user_id": user_id}
