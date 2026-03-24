import re
from dataclasses import dataclass
from typing import ClassVar

from ..exceptions import UsernameError


@dataclass(frozen=True, slots=True, repr=False)
class Username:
    """
    Username Value Object representing a validated name of user.

    Rules:
    - Length: 4-20 characters
    - Allowed: a-z, A-Z, 0-9, underscore (_)
    - Cannot start or end with underscore
    """

    _min_length: ClassVar[int] = 4
    _max_length: ClassVar[int] = 20
    _regex: ClassVar[re.Pattern] = re.compile(r"^\w+$")

    value: str

    def __post_init__(self) -> None:
        """
        Validate username immediately after initialization.

        Raises:
            UsernameError: If the username  format is invalid
        """

        if not self._min_length <= len(self.value) <= self._max_length:
            raise UsernameError(
                f"Length of username must be"
                f"{self._min_length}-{self._max_length} characters: {self.value}"
            )

        if not self._regex.match(self.value):
            raise UsernameError(f"Invalid characters in username: {self.value}")

        if self.value.startswith("_") or self.value.endswith("_"):
            raise UsernameError(
                f"Username cannot start or end with underscore: {self.value}"
            )

    def __repr__(self) -> str:
        return f"Username({self.value!r})"
