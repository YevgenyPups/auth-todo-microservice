from src.domain.entities import User as UserEntity
from src.domain.exceptions import EmailAlreadyExistsError
from src.domain.interfaces.password_hasher import IPasswordHasher
from src.domain.interfaces.uow import IUnitOfWork
from src.domain.password_validator import PasswordValidator
from src.domain.value_objects import Email

from ..dto.user_dto import RegisterUserDTO, UserDTO


class RegisterUser:
    """
    Use case for user registration.

    Handles the business logic for creating a new user account:
    - Validates password strength
    - Hashes the password for secure storage
    - Creates a domain entity
    - Persists the user via Unit of Work
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        password_validator: PasswordValidator,
        password_hasher: IPasswordHasher,
    ) -> None:
        """Initialize the RegisterUser use case."""

        self._uow = uow
        self._password_validator = password_validator
        self._password_hasher = password_hasher

    async def __call__(self, input: RegisterUserDTO) -> UserDTO:
        """
        Execute the user registration process.

        Args:
            input: Registration data transfer object

        Returns:
            UserDTO: Created user data without sensitive information

        Raises:
            PasswordValidationError: If password doesn't suit security requirements
            EmailAlreadyExistsError: If email is already registered
        """

        self._password_validator(input.password)
        password_hash = self._password_hasher.hash(input.password)
        user_entity = UserEntity(email=Email(input.email), password_hash=password_hash)

        async with self._uow:
            if await self._uow.user_repo.exists_by_email(user_entity.email.value):
                raise EmailAlreadyExistsError("User with this email already exists.")

            await self._uow.user_repo.save(user_entity)

        return UserDTO.from_entity(user_entity)
