"""Business logic for registration and login (US-001, US-002)."""
from .repository import UserRepository
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
