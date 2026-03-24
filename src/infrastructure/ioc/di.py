from dishka import Provider

from .providers import DBSessionProvider, SettingsProvider


def get_providers() -> dict[str, Provider]:
    """Return all DI providers grouped by domain."""

    return {"settings": SettingsProvider(), "db": DBSessionProvider()}
