from unittest.mock import MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.common.exceptions import UoWError
from src.core.common.interface.session import ISessionAsyncWrapper
from src.core.common.interface.uow.base_uow import ISQLAlchemyUoWAsyncBase


pytestmark = pytest.mark.uow


async def test_context_manager(
    uow: ISQLAlchemyUoWAsyncBase,
    mock_async_session_wrapper: MagicMock,
    mock_async_session: AsyncSession,
):
    async with uow as uow:
        assert uow.session is mock_async_session

        mock_async_session_wrapper.factory.maker.assert_called_once()

    mock_async_session.rollback.assert_called_once()
    mock_async_session.close.assert_called_once()


async def test_commit_success(
    uow: ISQLAlchemyUoWAsyncBase,
    mock_async_session: AsyncSession,
):
    async with uow as uow:
        await uow.commit()
        mock_async_session.commit.assert_called_once()


async def test_commit_failure(
    uow: ISQLAlchemyUoWAsyncBase,
    mock_async_session: AsyncSession,
):
    mock_async_session.commit.side_effect = Exception("Commit failure")
    async with uow as uow:
        with pytest.raises(UoWError) as exc_info:
            await uow.commit()
        mock_async_session.rollback.assert_called_once()
        assert str(exc_info.value) == "Error on commit: Commit failure"


async def test_flush_success(
    uow: ISQLAlchemyUoWAsyncBase,
    mock_async_session: AsyncSession,
):
    async with uow as uow:
        await uow.flush()
        mock_async_session.flush.assert_called_once()


async def test_flush_failure(
    uow: ISQLAlchemyUoWAsyncBase,
    mock_async_session: AsyncSession,
):
    mock_async_session.flush.side_effect = Exception("Flush failure")
    async with uow as uow:
        with pytest.raises(UoWError) as exc_info:
            await uow.flush()
        mock_async_session.rollback.assert_called_once()
        assert str(exc_info.value) == "Error on flush: Flush failure"


async def test_rollback(
    uow: ISQLAlchemyUoWAsyncBase,
    mock_async_session: AsyncSession,
):
    async with uow as uow:
        await uow.rollback()
        mock_async_session.rollback.assert_called_once()
