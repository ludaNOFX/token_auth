from abc import ABC, abstractmethod
from typing_extensions import Self
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.common.interface.session import ISessionAsyncWrapper


class ISQLAlchemyUoWAsyncBase(ABC):
    """Интерфейс базового асинхронного UoW"""

    @abstractmethod
    def __init__(self, session_wrapper: ISessionAsyncWrapper) -> None:
        """Инициализация

        Args:
            session_wrapper (ISessionAsyncWrapper): Асинхронная обертка для генерации сессии
        """  # noqa: E501

    @property
    @abstractmethod
    def session(self) -> AsyncSession:
        """Сессия

        Данная сессия доступна только после входа в контекст

        Returns:
            AsyncSession: Асинхронная сессия SQLAlchemy
        """

    @abstractmethod
    async def __aenter__(self, *args) -> Self:
        """Вход в контекстный менеджер

        Происходит создание сессии

        Returns:
            Self: ISQLAlchemyUoWAsyncBase
        """

    @abstractmethod
    async def __aexit__(self, *args):
        """Выход из контекстного менеджера

        Происходит кореектное завершение работы с сессией
        """

    @abstractmethod
    async def commit(self):
        """Отправка изменений в БД"""

    @abstractmethod
    async def flush(self):
        """Создание точки фиксации

        Отправка изменений в SQLAlchemy UoW
        """

    @abstractmethod
    async def rollback(self):
        """Откат изменений, до точки фиксации"""
