from src.application.settings import settings, Local  # type: ignore

assert isinstance(
    settings, Local
), "Running tests on prod db? Ye? pls run terminal: export PROJ_ENV=local"

settings: Local = settings
