from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, VARCHAR, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    """SQLAlchemy model for storing user data."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(
        VARCHAR(length=20), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(VARCHAR(length=320), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    role: Mapped[str] = mapped_column(
        VARCHAR(length=6),
        nullable=False,
    )
    is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, username={self.username}, email={self.email},"
            f"role={self.role}, is_confirmed={self.is_confirmed},"
            f"is_active={self.is_active}, is_deleted={self.is_deleted},"
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
