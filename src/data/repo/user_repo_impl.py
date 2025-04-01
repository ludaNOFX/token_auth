from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interface.repo.user_repo import IUserRepo
from src.core.dto.user import UserCreateDTO, UserDTO, UserUpdateDTO, UserslistDTO
from src.data.dao.base_dao_sql import DAOBaseSQL
from src.data.models.models import UserModel
from src.data.dao.base_dao_sql import MapperProtocol


class UserMapper(MapperProtocol[UserModel, UserDTO, UserslistDTO]):
    @staticmethod
    def to_dto(model: UserModel, exclude_fields: list[str] | None = None) -> UserDTO:
        return UserDTO.from_dict(model.to_dict(exclude=exclude_fields))

    @staticmethod
    def to_list_dto(
        seq: Sequence[UserDTO],
        total: int,
        offset: int,
        limit: int,
    ) -> UserslistDTO:
        return UserslistDTO(
            items=seq,
            total=total,
            offset=total,
            limit=total,
        )


class UserRepo(
    DAOBaseSQL[UserModel, UserDTO, UserCreateDTO, UserUpdateDTO, UserslistDTO], IUserRepo
):
    model = UserModel
    root_dto = UserDTO
    create_dto = UserCreateDTO
    update_dto = UserUpdateDTO
    list_dto = UserslistDTO
    mapper = UserMapper

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
