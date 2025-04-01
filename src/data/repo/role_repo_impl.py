from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interface.repo.role_repo import IRoleRepo
from src.core.dto.role import RoleDTO, RoleslistDTO, RoleCreateDTO, RoleUpdateDTO
from src.data.dao.base_dao_sql import DAOBaseSQL
from src.data.models.models import RoleModel
from src.data.dao.base_dao_sql import MapperProtocol


class RoleMapper(MapperProtocol[RoleModel, RoleDTO, RoleslistDTO]):
    @staticmethod
    def to_dto(model: RoleModel, exclude_fields: list[str] | None = None) -> RoleDTO:
        return RoleDTO.from_dict(model.to_dict(exclude=exclude_fields))

    @staticmethod
    def to_list_dto(
        seq: Sequence[RoleDTO],
        total: int,
        offset: int,
        limit: int,
    ) -> RoleslistDTO:
        return RoleslistDTO(
            items=seq,
            total=total,
            offset=offset,
            limit=limit,
        )


class RoleRepo(
    DAOBaseSQL[RoleModel, RoleDTO, RoleCreateDTO, RoleUpdateDTO, RoleslistDTO], IRoleRepo
):
    model = RoleModel
    root_dto = RoleDTO
    create_dto = RoleCreateDTO
    update_dto = RoleUpdateDTO
    list_dto = RoleslistDTO
    mapper = RoleMapper

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
