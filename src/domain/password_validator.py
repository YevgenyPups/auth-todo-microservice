from dataclasses import dataclass
from typing import ClassVar

from .exceptions import PasswordValidationError


@dataclass(frozen=True, slots=True, repr=False)
class PasswordValidator:
    """
    Domain service for password validation.

    Validates password length constraints.
    """

    _min_length: ClassVar[int] = 8
    _max_length: ClassVar[int] = 128

    def __call__(self, password: str) -> None:
        """
        Validate password length.

        Raises:
            PasswordValidationError: If password length is outside allowed range
        """

        if not self._min_length <= len(password) <= self._max_length:
            raise PasswordValidationError(
                f"Password must be {self._min_length}-{self._max_length}"
                f"characters: {password}"
            )
