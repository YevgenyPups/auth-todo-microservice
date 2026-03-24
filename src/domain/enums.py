from enum import StrEnum


class UserRole(StrEnum):
    """Defines possible user roles in the system."""

    ADMIN = "admin"
    CLIENT = "client"
