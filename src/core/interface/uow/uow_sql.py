from abc import abstractmethod

from src.core.interface.repo.role_repo import IRoleRepo
from src.core.interface.repo.user_repo import IUserRepo
from src.core.interface.uow.base_uow import ISQLAlchemyUoWAsyncBase


class IUowSQL(ISQLAlchemyUoWAsyncBase):
    @property
    @abstractmethod
    def user_repo(self) -> IUserRepo: ...

    @property
    @abstractmethod
    def role_repo(self) -> IRoleRepo: ...
