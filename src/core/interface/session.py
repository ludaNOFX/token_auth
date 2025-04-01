from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class ISessionAsyncFactory(ABC):
    @property
    @abstractmethod
    def maker(self) -> async_sessionmaker: ...


class ISessionAsyncWrapper(ABC):
    @property
    @abstractmethod
    def factory(self) -> ISessionAsyncFactory: ...

    @abstractmethod
    def t(self) -> AbstractAsyncContextManager[AsyncSession]: ...
