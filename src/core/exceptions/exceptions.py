class BaseError(Exception):
    """Базовая ошибка"""

    def __init__(self, message: str, h: str | None = ""):
        self.message = message
        self.hidden = h
        super().__init__(self.message)


class ApplicationError(BaseError):
    """Базовый класс для всех ошибок приложения"""

    pass


class UoWError(BaseError):
    """Ошибка UoW"""


class MappingError(BaseError):
    """Ошибка маппинга"""


class UsecaseError(BaseError):
    """Ошибка Usecase"""


class HasherError(BaseError):
    """Ошибка Hasher"""
