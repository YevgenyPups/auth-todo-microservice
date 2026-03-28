from dishka import Provider

from .providers import (
    DBSessionProvider,
    HelperProvider,
    MapperProvider,
    RepoProvider,
    SettingsProvider,
    UOWProvider,
    UseCaseProvider,
)


def get_providers() -> dict[str, Provider]:
    """Return all DI providers grouped by domain."""

    return {
        "settings": SettingsProvider(),
        "db": DBSessionProvider(),
        "mappers": MapperProvider(),
        "repos": RepoProvider(),
        "uow": UOWProvider(),
        "use_cases": UseCaseProvider(),
        "helpers": HelperProvider(),
    }
