from domain.interfaces.password_hasher import IPasswordHasher
from domain.interfaces.uow import IUnitOfWork
from domain.password_validator import PasswordValidator
from src.domain.entities import User as UserEntity
from src.domain.value_objects import Email

from ..dto.user_dto import RegisterUserDTO, UserDTO


class RegisterUser:

    def __init__(
        self,
        uow: IUnitOfWork,
        password_validator: PasswordValidator,
        password_hasher: IPasswordHasher,
    ):
        self._uow = uow
        self._password_validator = password_validator
        self._password_hasher = password_hasher

    async def __call__(self, input: RegisterUserDTO) -> UserDTO:

        self._password_validator(input.password)
        password_hash = self._password_hasher.hash(input.password)
        user_entity = UserEntity(email=Email(input.email), password_hash=password_hash)

        await self._uow.user_repo.save(user_entity)

        return UserDTO.from_entity(user_entity)
