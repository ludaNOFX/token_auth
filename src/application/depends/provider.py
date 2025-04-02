from collections.abc import Generator

from src.core.interface.password_hasher import IPasswordHasher
from src.core.interface.uow.uow_sql import IUowSQL
from src.data.uow.uow_sql_impl import SQLUow
from src.application.database.async_session import (
    SessionAsyncFactory,
    SessionAsyncWrapper,
    _create_engine,
)
from src.application.settings import settings
from src.infra.password_hasher_impl import PasswordHasher

engine = _create_engine(settings.DATABASE_ASYNC_URL)
session_factory = SessionAsyncFactory(engine=engine)
session_wrapper = SessionAsyncWrapper(factory=session_factory)


def get_uow_sql() -> Generator[IUowSQL, None, None]:
    yield SQLUow(session_wrapper=session_wrapper)


def get_password_hasher() -> Generator[IPasswordHasher, None, None]:
    yield PasswordHasher()
