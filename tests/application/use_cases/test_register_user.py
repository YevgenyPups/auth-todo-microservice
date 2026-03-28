import pytest

from src.application.dto.user_dto import RegisterUserDTO
from src.domain.exceptions import (
    EmailAlreadyExistsError,
    EmailError,
    PasswordValidationError,
)


@pytest.mark.asyncio
async def test_register_user_success(register_user):
    input_data = RegisterUserDTO(email="test_user@example.com", password="password")
    user_dto = await register_user(input_data)

    assert user_dto.email == input_data.email
    assert user_dto.username.startswith("user_") is True


@pytest.mark.asyncio
async def test_register_user_invalid_email(register_user):
    with pytest.raises(EmailError):
        input_data = RegisterUserDTO(email="test_user@example", password="password")
        await register_user(input_data)


@pytest.mark.asyncio
async def test_register_user_invalid_password(register_user):
    with pytest.raises(PasswordValidationError):
        input_data = RegisterUserDTO(email="test_user52@example.com", password="pass12")
        await register_user(input_data)


@pytest.mark.asyncio
async def test_register_user_email_already_exists(register_user):
    input_data1 = RegisterUserDTO(email="same_email@example.com", password="password")
    await register_user(input_data1)

    with pytest.raises(EmailAlreadyExistsError):
        input_data2 = RegisterUserDTO(
            email="same_email@example.com", password="password2"
        )
        await register_user(input_data2)
