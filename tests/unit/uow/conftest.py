from unittest.mock import MagicMock, create_autospec
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.common.interface.uow.base_uow import ISQLAlchemyUoWAsyncBase
from src.data.uow.base_uow_impl import SQLAlchemyUoWAsyncBase
from src.core.common.interface.session import ISessionAsyncFactory, ISessionAsyncWrapper


@pytest.fixture(scope="function")
def mock_async_session() -> AsyncSession:
    """Создаем мок-объект для SQLAlchemy AsyncSession"""
    return create_autospec(AsyncSession, instance=True)


@pytest.fixture(scope="function")
def mock_async_session_wrapper(mock_async_session) -> ISessionAsyncWrapper:
    """Создаем мок-объект для AsyncSessionWrapper"""
    wrapper = create_autospec(ISessionAsyncWrapper, instance=True)
    factory_mock = create_autospec(ISessionAsyncFactory, instance=True)

    maker_mock = MagicMock(spec=async_sessionmaker)
    maker_mock.return_value = mock_async_session

    factory_mock.maker = maker_mock
    wrapper.factory = factory_mock

    return wrapper


@pytest.fixture(scope="function")
def uow(mock_async_session_wrapper: ISessionAsyncWrapper) -> ISQLAlchemyUoWAsyncBase:
    """Создаем UoW с мокнутым async_session_wrapper"""
    return SQLAlchemyUoWAsyncBase(mock_async_session_wrapper)
