import pytest

from courtbook.auth_service import AuthService, InvalidCredentialsError, UserAlreadyExistsError
from courtbook.repository import InMemoryUserRepository
from courtbook.validation import ValidationError


@pytest.fixture
def service():
    return AuthService(InMemoryUserRepository())


class TestRegister:
    def test_should_return_user_id_when_data_is_valid(self, service):
        # Arrange
        email, password = "olena@courtbook.ua", "Court2026"
        # Act
        user_id = service.register(email, password, "Олена")
        # Assert
        assert user_id == 1

    def test_should_store_email_in_lowercase_when_registering(self, service):
        service.register("Olena@CourtBook.ua", "Court2026", "Олена")
        assert service.repository.find_by_email("olena@courtbook.ua") is not None

    def test_should_not_store_plain_password_when_registering(self, service):
        service.register("olena@courtbook.ua", "Court2026", "Олена")
        user = service.repository.find_by_email("olena@courtbook.ua")
        assert user["password_hash"] != "Court2026"

    def test_should_raise_error_when_email_already_registered(self, service):
        # Arrange
        service.register("olena@courtbook.ua", "Court2026", "Олена")
        # Act / Assert
        with pytest.raises(UserAlreadyExistsError):
            service.register("OLENA@courtbook.ua", "Court2026", "Олена")

    def test_should_raise_validation_error_when_password_weak(self, service):
        with pytest.raises(ValidationError):
            service.register("olena@courtbook.ua", "12345678", "Олена")


class TestLogin:
    def test_should_return_user_id_when_credentials_correct(self, service):
        user_id = service.register("ivan@courtbook.ua", "Tennis2026", "Іван")
        assert service.login("ivan@courtbook.ua", "Tennis2026") == user_id

    def test_should_raise_error_when_password_wrong(self, service):
        service.register("ivan@courtbook.ua", "Tennis2026", "Іван")
        with pytest.raises(InvalidCredentialsError):
            service.login("ivan@courtbook.ua", "Wrong2026")

    def test_should_raise_error_when_user_not_found(self, service):
        with pytest.raises(InvalidCredentialsError):
            service.login("nobody@courtbook.ua", "Tennis2026")
