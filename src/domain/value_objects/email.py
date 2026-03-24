from dataclasses import dataclass

from email_validator import EmailNotValidError, validate_email

from ..exceptions import EmailError


@dataclass(frozen=True, slots=True, repr=False)
class Email:
    """Email value object with RFC 5322 validation."""

    value: str

    def __post_init__(self) -> None:
        """Validate and normalize email address."""

        try:
            validated = validate_email(self.value, check_deliverability=False)
            object.__setattr__(self, "value", validated.normalized)
        except EmailNotValidError as e:
            raise EmailError(f"Invalid email: {e}")

    def __repr__(self) -> str:
        return f"Email({self.value!r})"
