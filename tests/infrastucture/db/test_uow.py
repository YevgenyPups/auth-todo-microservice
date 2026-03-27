import pytest

from src.domain.entities import User as UserEntity
from src.domain.value_objects import Email


@pytest.mark.asyncio
async def test_uow_commit_saves_data(uow):
    user = UserEntity(email=Email("test@example.com"), password_hash=b"hash")
    async with uow:
        await uow.user_repo.save(user)

    async with uow:
        res = await uow.user_repo.exists_by_email("test@example.com")

    assert res is True


@pytest.mark.asyncio
async def test_uow_rollback_on_exception(uow):
    user = UserEntity(email=Email("test2@example.com"), password_hash=b"hash")

    with pytest.raises(ValueError):
        async with uow:
            await uow.user_repo.save(user)
            # make a fake error in transaction
            raise ValueError("Something went wrong")
    async with uow:
        res = await uow.user_repo.exists_by_email("test2@example.com")
    assert res is False
