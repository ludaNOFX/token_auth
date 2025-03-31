class BaseError(Exception):
    """Базовая ошибка"""

    def __init__(self, message: str, h: str | None = ""):
        self.message = message
        self.hidden = h
        super().__init__(self.message)


class UoWError(BaseError):
    """Ошибка UoW"""
