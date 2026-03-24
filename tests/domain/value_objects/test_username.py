import pytest

from src.domain.exceptions import UsernameError
from src.domain.value_objects import Username


@pytest.mark.parametrize(
    "username",
    [
        "user_name",
        "pups123",
        "a" * 20,
        "a" * 4,
    ],
)
def test_valid_username(username):
    assert Username(username).value == username


@pytest.mark.parametrize(
    "username",
    [
        "a" * 3,  # too short
        "a" * 21,  # too long
        "user@name",  # invalid char
        "_john",  # starts with underscore
        "john_",  # ends with underscore
    ],
)
def test_invalid_username(username):
    with pytest.raises(UsernameError):
        Username(username)
