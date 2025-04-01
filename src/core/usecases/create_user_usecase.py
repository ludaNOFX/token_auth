import logging

from src.core.entities.user import UserCreateEntity
from src.core.exceptions.exceptions import HasherError, UsecaseError
from src.core.interface.password_hasher import IPasswordHasher
from src.core.dto.user import UserCreateDTO, UserDTO
from src.core.interface.uow.uow_sql import IUowSQL


logger = logging.getLogger(__name__)


class Usecase:
    def __init__(self, uow_sql: IUowSQL, password_hasher: IPasswordHasher) -> None:
        self._uow = uow_sql
        self._hasher = password_hasher

    async def __call__(self, dto: UserCreateDTO) -> UserDTO:
        try:
            entity = UserCreateEntity(**dto.to_dict())
            hashed_password = self._hasher.hash_password(entity.password)
            entity.set_hash_password(hashed_password)

        except Exception as e:
            logger.exception(f"Failed to hash pass: {e}")
            raise HasherError(f"Failed logic: {e}") from e
        try:
            async with self._uow as uow:
                role = await uow.role_repo.get_by_attr(
                    mp_attr={"name": entity.role},
                )
                entity.set_role_id(role.id)
        except Exception as e:
            logger.exception(f"Failed to create user: {dto.login}")
            raise UsecaseError(f"Failed logic: {e}") from e
        try:
            async with self._uow as uow:
                dto_create = entity.entity_to_dto()
                res = await uow.user_repo.create(
                    dto=dto_create, exclude=["role_id", "updated_at"]
                )
                await uow.commit()
        except Exception as e:
            logger.exception(f"Failed to create user: {dto.login}")
            raise UsecaseError(f"Failed logic: {e}") from e
        return res
