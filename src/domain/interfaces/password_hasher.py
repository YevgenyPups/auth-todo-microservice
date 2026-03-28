from typing import Protocol


class IPasswordHasher(Protocol):
    """Protocol for password hashing and verification."""

    @staticmethod
    def hash(password: str) -> bytes:
        """Hash a plain text password."""
        ...

    @staticmethod
    def verify(password: str, password_hash: bytes) -> bool:
        """Verify a password against its hash."""
        ...
