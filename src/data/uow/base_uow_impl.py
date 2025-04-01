from typing_extensions import Self
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import UoWError
from src.core.interface.session import ISessionAsyncWrapper
from src.core.interface.uow.base_uow import ISQLAlchemyUoWAsyncBase


class SQLAlchemyUoWAsyncBase(ISQLAlchemyUoWAsyncBase):
    """Tested"""

    def __init__(self, session_wrapper: ISessionAsyncWrapper) -> None:
        self.session_wrapper = session_wrapper
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise UoWError("Session is not setup")
        return self._session

    async def __aenter__(self, *args) -> Self:
        self._session = self.session_wrapper.factory.maker()
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()
        self._session = None

    async def commit(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise UoWError(f"Error on commit: {e}") from e

    async def flush(self):
        try:
            await self.session.flush()
        except Exception as e:
            await self.session.rollback()
            raise UoWError(f"Error on flush: {e}") from e

    async def rollback(self):
        await self.session.rollback()
