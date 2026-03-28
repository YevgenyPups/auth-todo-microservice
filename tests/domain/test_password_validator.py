import pytest

from src.domain.exceptions import PasswordValidationError


@pytest.mark.parametrize(
    "password",
    [
        "12345678",
        "a" * 128,
        "password123",
        "my_secret",
    ],
)
def test_valid_password(password, password_validator):
    assert password_validator(password) is None


@pytest.mark.parametrize(
    "password",
    [
        "",  # empty
        "1234567",  # too short
        "a" * 129,  # too long
    ],
)
def test_invalid_password(password, password_validator):
    with pytest.raises(PasswordValidationError):
        password_validator(password)
