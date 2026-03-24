class DomainError(Exception):
    """Base exception for domain-related errors."""

    pass


class EmailError(DomainError):
    """Raised when email format validation fails."""

    pass
