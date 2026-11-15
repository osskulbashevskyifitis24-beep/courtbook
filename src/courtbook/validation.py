"""Validation rules for user input (US-001)."""
import re

EMAIL_MAX_LENGTH = 254
PASSWORD_MIN_LENGTH = 8
PHONE_PREFIX = "+380"
PHONE_LENGTH = 13
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class ValidationError(ValueError):
    """Raised when user input does not satisfy validation rules."""


def validate_email(email: str) -> bool:
    if not isinstance(email, str):
        raise TypeError("email must be a string")
    if not email or len(email) > EMAIL_MAX_LENGTH:
        return False
    return bool(EMAIL_PATTERN.match(email))


def validate_password(password: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if len(password) < PASSWORD_MIN_LENGTH:
        return False
    has_upper = any(ch.isupper() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    return has_upper and has_digit


def validate_phone(phone: str | None) -> bool:
    if not phone:
        return True  # phone is optional
    return phone.startswith(PHONE_PREFIX) and len(phone) == PHONE_LENGTH and phone[1:].isdigit()


def validate_registration(email: str, password: str, phone: str | None = None) -> None:
    if not validate_email(email):
        raise ValidationError("Invalid email")
    if not validate_password(password):
        raise ValidationError("Weak password")
    if not validate_phone(phone):
        raise ValidationError("Invalid phone")
