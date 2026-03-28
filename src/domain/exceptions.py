class DomainError(Exception):
    """Base exception for domain-related errors."""

    pass


class EmailError(DomainError):
    """Raised when email format validation fails."""

    pass


class UsernameError(DomainError):
    """Raised when username validation fails."""

    pass


class PasswordValidationError(DomainError):
    """Raised when password validation fails (length, complexity, etc.)."""

    pass


class EmailAlreadyExistsError(DomainError):
    """Raised when email is already registered."""

    pass
