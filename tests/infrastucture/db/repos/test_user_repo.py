import pytest

from src.domain.entities import User as UserEntity
from src.domain.value_objects import Email


@pytest.mark.asyncio
async def test_created_user_exists(user_repo):
    user_entity = UserEntity(email=Email("test@example.com"), password_hash=b"hash")
    await user_repo.save(user_entity)

    assert await user_repo.exists_by_email(user_entity.email.value) is True


@pytest.mark.asyncio
async def test_not_created_user_not_exists(user_repo):
    assert await user_repo.exists_by_email("test@example.com") is False
