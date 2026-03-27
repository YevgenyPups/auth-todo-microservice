import bcrypt


class PasswordHasher:
    """Bcrypt implementation of password hashing."""

    @staticmethod
    def hash(password: str) -> bytes:
        """Hash a plain text password using bcrypt."""

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def verify(password: str, password_hash: bytes) -> bool:
        """Verify a password against a bcrypt hash."""

        return bcrypt.checkpw(password.encode("utf-8"), password_hash)
