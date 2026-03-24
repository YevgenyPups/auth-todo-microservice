import pytest

from src.domain.exceptions import EmailError
from src.domain.value_objects import Email


@pytest.mark.parametrize(
    "email, expected",
    [
        ("user@example.com", "user@example.com"),
        ("USER@EXAMPLE.COM", "USER@example.com"),
        ("123@example.com", "123@example.com"),
    ],
)
def test_valid_email(email, expected):
    assert Email(email).value == expected


@pytest.mark.parametrize(
    "email",
    [
        "invalid",
        "user@",
        "@example.com",
        "user@example",
        "user@.com",
    ],
)
def test_invalid_email(email) -> None:
    with pytest.raises(EmailError):
        Email(email)
