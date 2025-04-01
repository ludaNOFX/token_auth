from src.core.interface.repo.role_repo import IRoleRepo
from src.data.repo.role_repo_impl import RoleRepo
from src.core.interface.repo.user_repo import IUserRepo
from src.core.interface.uow.uow_sql import IUowSQL
from src.data.repo.user_repo_impl import UserRepo
from src.data.uow.base_uow_impl import SQLAlchemyUoWAsyncBase


class SQLUow(SQLAlchemyUoWAsyncBase, IUowSQL):
    @property
    def user_repo(self) -> IUserRepo:
        return UserRepo(session=self.session)

    @property
    def role_repo(self) -> IRoleRepo:
        return RoleRepo(session=self.session)
