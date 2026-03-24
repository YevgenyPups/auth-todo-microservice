import pytest

from src.domain.exceptions import PasswordValidationError
from src.domain.password_validator import PasswordValidator


@pytest.mark.parametrize(
    "password",
    [
        "12345678",
        "a" * 128,
        "password123",
        "my_secret",
    ],
)
def test_valid_password(password):
    validator = PasswordValidator()
    validator(password)


@pytest.mark.parametrize(
    "password",
    [
        "",  # empty
        "1234567",  # too short
        "a" * 129,  # too long
    ],
)
def test_invalid_password(password):
    validator = PasswordValidator()
    with pytest.raises(PasswordValidationError):
        validator(password)
