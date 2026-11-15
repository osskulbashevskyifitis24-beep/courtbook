import pytest

from courtbook.validation import (ValidationError, validate_email, validate_password,
                                  validate_phone, validate_registration)


class TestValidateEmail:
    def test_should_return_true_when_email_is_valid(self):
        # Arrange
        email = "player@courtbook.ua"
        # Act
        result = validate_email(email)
        # Assert
        assert result is True

    def test_should_return_false_when_email_has_no_at_symbol(self):
        # Arrange
        email = "playercourtbook.ua"
        # Act
        result = validate_email(email)
        # Assert
        assert result is False

    def test_should_return_false_when_email_is_empty(self):
        assert validate_email("") is False

    def test_should_return_false_when_email_longer_than_254(self):
        # Arrange
        email = "a" * 250 + "@b.ua"
        # Act / Assert
        assert validate_email(email) is False

    def test_should_raise_typeerror_when_email_is_none(self):
        with pytest.raises(TypeError):
            validate_email(None)


class TestValidatePassword:
    def test_should_return_true_when_password_meets_all_requirements(self):
        assert validate_password("Court2026") is True

    def test_should_return_false_when_password_is_too_short(self):
        assert validate_password("Ab1") is False

    def test_should_return_true_when_password_is_exactly_min_length(self):
        assert validate_password("Abcdefg1") is True

    def test_should_return_false_when_password_has_no_digit(self):
        assert validate_password("CourtBook") is False

    def test_should_return_false_when_password_has_no_uppercase(self):
        assert validate_password("court2026") is False

    def test_should_raise_typeerror_when_password_is_none(self):
        with pytest.raises(TypeError):
            validate_password(None)


class TestValidatePhone:
    @pytest.mark.parametrize("phone", ["+380671234567", None, ""])
    def test_should_return_true_when_phone_valid_or_empty(self, phone):
        assert validate_phone(phone) is True

    @pytest.mark.parametrize("phone", ["0671234567", "+38067123456", "+380abcdefghi"])
    def test_should_return_false_when_phone_invalid(self, phone):
        assert validate_phone(phone) is False


def test_should_raise_validation_error_when_registration_data_invalid():
    with pytest.raises(ValidationError):
        validate_registration("bad-email", "Court2026")
