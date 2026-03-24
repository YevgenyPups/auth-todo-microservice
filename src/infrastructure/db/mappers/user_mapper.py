from src.domain.entities import User as UserEntity
from src.domain.enums import UserRole
from src.domain.value_objects import Email, Username

from ..models import User as UserModel


class UserMapper:
    """
    Mapper class for converting between
    User domain entities and User db models.
    """

    @staticmethod
    def to_entity(user_model: UserModel) -> UserEntity:
        """Convert User sqlalchemy model to User domain entity."""

        return UserEntity(
            id=user_model.id,
            email=Email(user_model.email),
            password_hash=user_model.password_hash,
            username=Username(user_model.username),
            role=UserRole(user_model.role),
            is_confirmed=user_model.is_confirmed,
            is_active=user_model.is_active,
            is_deleted=user_model.is_deleted,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    @staticmethod
    def to_model(user_entity: UserEntity) -> UserModel:
        """Convert User domain entity to User sqlalchemy model."""

        return UserModel(
            id=user_entity.id,
            email=user_entity.email.value,
            password_hash=user_entity.password_hash,
            username=user_entity.username.value,
            role=user_entity.role.value,
            is_confirmed=user_entity.is_confirmed,
            is_active=user_entity.is_active,
            is_deleted=user_entity.is_deleted,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
        )
