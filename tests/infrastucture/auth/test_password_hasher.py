import pytest

from src.infrastructure.auth.password_hasher import PasswordHasher


@pytest.fixture(scope="module")
def password_hasher():
    return PasswordHasher()


def test_password_verify_valid(password_hasher):
    password = "password"
    password_hash = password_hasher.hash(password)

    assert password_hasher.verify(password, password_hash) is True


def test_password_verify_invalid(password_hasher):
    password = "password"
    invalid_password = "password2"
    password_hash = password_hasher.hash(password)

    assert password_hasher.verify(invalid_password, password_hash) is False
