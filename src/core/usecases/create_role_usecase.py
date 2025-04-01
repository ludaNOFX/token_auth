import logging
from src.core.exceptions.exceptions import UsecaseError
from src.core.dto.role import RoleCreateDTO, RoleDTO
from src.core.interface.uow.uow_sql import IUowSQL

logger = logging.getLogger(__name__)


class Usecase:
    def __init__(self, uow_sql: IUowSQL) -> None:
        self._uow = uow_sql

    async def __call__(self, dto: RoleCreateDTO) -> RoleDTO:
        try:
            async with self._uow as uow:
                res = await uow.role_repo.create(dto=dto)
                await uow.commit()
        except Exception as e:
            logger.exception(f"Failed to create role: {dto}")
            raise UsecaseError(f"Failed logic: {e}") from e
        return res
