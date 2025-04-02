import logging

from src.core.exceptions.exceptions import UsecaseError
from src.core.dto.user import UserDTO
from src.core.interface.uow.uow_sql import IUowSQL


logger = logging.getLogger(__name__)


class Usecase:
    def __init__(self, uow_sql: IUowSQL) -> None:
        self._uow = uow_sql

    async def __call__(self, user_id: int) -> UserDTO:
        try:
            async with self._uow as uow:
                res = await uow.user_repo.get_by_attr(mp_attr={"id": user_id})
        except Exception as e:
            logger.exception("Failed to return user")
            raise UsecaseError(f"Failed logic: {e}") from e
        return res
