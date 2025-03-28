from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from src.core.interface.session import ISessionAsyncFactory, ISessionAsyncWrapper


def _create_engine(url: str, echo: bool = False) -> AsyncEngine:
    """Создание AsyncEngine SQLAlchemy

    Args:
        url (str): Connection string
        echo (bool, optional): Отображать отправляемые запросы. Default False.

    Returns:
        AsyncEngine: Асинхронный движок SQLAlchemy
    """
    return create_async_engine(
        url=url,
        future=True,
        echo=echo,
        pool_pre_ping=False,
        pool_size=20,
        max_overflow=10,
        pool_recycle=1200,
        pool_timeout=6000,
    )


class SessionAsyncFactory(ISessionAsyncFactory):
    """Холдер для async_sessionmaker"""

    def __init__(self, engine: AsyncEngine) -> None:
        """Инициализация

        Args:
            engine (AsyncEngine): Асинхронный движок SQLAlchemy
        """
        self._maker = async_sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
        )

    @property
    def maker(self) -> async_sessionmaker:
        """Получить async_sessionmaker

        Returns:
            async_sessionmaker: Фабрика сессий SQLAlchemy
        """
        return self._maker


class SessionAsyncWrapper(ISessionAsyncWrapper):
    """Обертка для получения сессии SQLAlchemy"""

    def __init__(self, factory: ISessionAsyncFactory) -> None:
        """Инициализация

        Args:
            factory (ISessionAsyncFactory): Холдер для async_sessionmaker
        """
        self._factory = factory

    @property
    def factory(self) -> ISessionAsyncFactory:
        """Возвращает входящую при инициализации фабрику

        Returns:
            ISessionAsyncFactory: Холдер для async_sessionmaker
        """
        return self._factory

    def t(self) -> AbstractAsyncContextManager[AsyncSession]:
        """Получить сессию (Контекстный менеджер)

        Raises:
            e(SQLAlchemyError): Если произошла ошибка при создании сессии или выполнении операций

        Returns:
            AbstractAsyncContextManager[AsyncSession]: Асинхронный контекстный менеджер для работы с сессией

        Yields:
            Iterator[AbstractAsyncContextManager[AsyncSession]]: Сессия SQLAlchemy
        """  # noqa: E501

        @asynccontextmanager
        async def _session_generator() -> AsyncGenerator[AsyncSession, None]:
            async with self.factory.maker() as session:
                try:
                    yield session
                except Exception as e:
                    await session.rollback()
                    raise e
                finally:
                    await session.close()

        return _session_generator()
