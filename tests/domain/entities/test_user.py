from datetime import datetime
from uuid import UUID

from src.domain.entities import User
from src.domain.enums import UserRole
from src.domain.value_objects import Email


def test_create_user_with_min_fields():
    email = Email("test@example.com")
    password_hash = b"hashed_password"

    user = User(email=email, password_hash=password_hash)

    assert user.email == email
    assert user.password_hash == password_hash


def test_user_has_generated_id():
    user = User(email=Email("test@example.com"), password_hash=b"hash")

    assert isinstance(user.id, UUID)


def test_user_has_generated_username():
    user = User(email=Email("test@example.com"), password_hash=b"hash")

    assert user.username.value.startswith("user_")


def test_user_has_default_role():
    user = User(email=Email("test@example.com"), password_hash=b"hash")

    assert user.role == UserRole.CLIENT


def test_user_has_default_flags():
    user = User(email=Email("test@example.com"), password_hash=b"hash")

    assert user.is_active is False
    assert user.is_confirmed is False
    assert user.is_deleted is False


def test_user_has_timestamps():
    user = User(email=Email("test@example.com"), password_hash=b"hash")

    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert user.created_at <= user.updated_at
