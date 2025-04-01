import logging

from src.core.dto.role import RoleslistDTO
from src.core.exceptions.exceptions import UsecaseError
from src.core.interface.uow.uow_sql import IUowSQL


logger = logging.getLogger(__name__)


class Usecase:
    def __init__(self, uow_sql: IUowSQL) -> None:
        self._uow = uow_sql

    async def __call__(self) -> RoleslistDTO:
        try:
            async with self._uow as uow:
                res = await uow.role_repo.get_many()
        except Exception as e:
            logger.exception("Failed to return roles list")
            raise UsecaseError(f"Failed logic: {e}") from e
        return res
