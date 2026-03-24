class DomainError(Exception):
    """Base exception for domain-related errors."""

    pass


class EmailError(DomainError):
    """Raised when email format validation fails."""

    pass


class UsernameError(DomainError):
    """Raised when username validation fails."""

    pass
