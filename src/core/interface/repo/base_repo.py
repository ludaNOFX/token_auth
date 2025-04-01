from abc import ABC, abstractmethod
from typing import Generic, TypeVar
import typing

from src.core.dto.base_dto import BaseDTO, BaseListDTO

CreateDTO = TypeVar("CreateDTO", bound=BaseDTO)
RootDTO = TypeVar("RootDTO", bound=BaseDTO)
ListDTO = TypeVar("ListDTO", bound=BaseListDTO[BaseDTO])


class IBaseRepo(ABC, Generic[CreateDTO, RootDTO, ListDTO]):
    @abstractmethod
    async def create(
        self,
        *,
        dto: CreateDTO,
        check_duplicates: bool = True,
        duplicate_fields: list[str] | None = None,
        exclude: list[str] | None = None,
    ) -> RootDTO:
        """Базовый метод создания"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_attr(
        self, *, mp_attr: typing.Any, exclude: list[str] | None = None
    ) -> RootDTO:
        """Базовый метод возвращающий объект по любому полю"""
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, *, exclude: list[str] | None = None) -> ListDTO:
        """Базовый метод возвращающий много объектов"""
        raise NotImplementedError

    @abstractmethod
    async def count(
        self,
        *,
        filters: dict[str, typing.Any] | None = None,
        custom_filter: typing.Any | None = None,
    ) -> int:
        """Базовый метод кол-во объектов"""
        raise NotImplementedError
