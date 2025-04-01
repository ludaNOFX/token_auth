from collections.abc import Sequence
import typing
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import IntegrityError

from src.core.dto.base_dto import BaseDTO, BaseListDTO
from src.application.database.holder import ModelBase

# Исправленные TypeVar с правильной вариативностью
ContraModelType = typing.TypeVar("ContraModelType", contravariant=True, bound=ModelBase)
ModelType = typing.TypeVar("ModelType", bound=ModelBase)  # invariant
RootTypeDTO = typing.TypeVar("RootTypeDTO", bound=BaseDTO)  # invariant
CreateTypeDTO = typing.TypeVar("CreateTypeDTO", bound=BaseDTO)  # invariant
UpdateTypeDTO = typing.TypeVar("UpdateTypeDTO", bound=BaseDTO)  # invariant
ListTypeDTO = typing.TypeVar(
    "ListTypeDTO", covariant=True, bound=BaseListDTO[BaseDTO]
)  # invariant  # noqa: E501


class MapperProtocol(
    typing.Protocol[
        ContraModelType,
        RootTypeDTO,
        ListTypeDTO,
    ]
):
    @staticmethod
    def to_dto(
        model: ContraModelType,
        exclude_fields: list[str] | None = None,
    ) -> RootTypeDTO: ...

    @staticmethod
    def to_list_dto(
        seq: Sequence[RootTypeDTO],
        total: int,
        offset: int,
        limit: int,
    ) -> ListTypeDTO: ...


class DAOBaseSQL(
    typing.Generic[
        ModelType,
        RootTypeDTO,
        CreateTypeDTO,
        UpdateTypeDTO,
        ListTypeDTO,
    ]
):
    model: type[ModelType]
    root_dto: type[RootTypeDTO]
    create_dto: type[CreateTypeDTO]
    update_dto: type[UpdateTypeDTO]
    list_dto: type[ListTypeDTO]
    mapper: type[MapperProtocol[ModelType, RootTypeDTO, ListTypeDTO]]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise AttributeError("Session was not setup!")
        return self._session

    def _validate_filters(self, **filters: typing.Any) -> dict[str, typing.Any]:
        valid_filters = {}
        mapper = inspect(self.model)

        for field_name, value in filters.items():
            if field_name in mapper.attrs:
                valid_filters[field_name] = value
            else:
                raise ValueError(
                    f"Поле {field_name} не существует в модели {self.model.__name__}"
                )

        return valid_filters

    async def _get_by_fields(self, **filters: typing.Any) -> ModelType | None:
        valid_filters = self._validate_filters(**filters)
        result = await self.session.execute(select(self.model).filter_by(**valid_filters))
        return result.scalars().first()

    async def create(
        self,
        *,
        dto: CreateTypeDTO,
        check_duplicates: bool = True,
        duplicate_fields: list[str] | None = None,
        exclude: list[str] | None = None,
    ) -> RootTypeDTO:
        """
        Создать объект с проверкой на дубликаты.

        Args:
            dto: DTO для создания
            check_duplicates: Проверять ли дубликаты перед созданием
            duplicate_fields: Поля для проверки дубликатов (если None, проверяются все поля DTO)

        Returns:
            Созданный объект в виде DTO

        Raises:
            ValueError: Если объект с такими параметрами уже существует
            IntegrityError: Если произошла ошибка уникальности в БД
        """  # noqa: E501
        data = dto.to_dict()

        if check_duplicates:
            # Определяем поля для проверки дубликатов
            fields_to_check = duplicate_fields or list(data.keys())
            duplicate_filters = {
                field: data[field] for field in fields_to_check if field in data
            }

            if duplicate_filters:
                existing = await self._get_by_fields(**duplicate_filters)
                if existing is not None:
                    raise ValueError(
                        f"Объект {self.model.__name__} с такими параметрами уже существует"  # noqa: E501
                    )  # noqa: E501

        try:
            obj = self.model(**data)
            self.session.add(obj)
            await self.session.flush()
            await self.session.refresh(obj)
            return self.mapper.to_dto(obj, exclude_fields=exclude)
        except IntegrityError as e:
            if "duplicate key" in str(e).lower():
                raise ValueError("Объект с такими параметрами уже существует") from e
            raise

    async def get_by_attr(
        self, *, mp_attr: typing.Any, exclude: list[str] | None = None
    ) -> RootTypeDTO:
        fields_to_check = list(mp_attr.keys())
        filters = {field: mp_attr[field] for field in fields_to_check if field in mp_attr}
        existing = await self._get_by_fields(**filters)
        if existing is None:
            raise ValueError(
                f"Объекта {self.model.__name__} с такими параметрами не существует"
            )  # noqa: E501

        return self.mapper.to_dto(existing, exclude_fields=exclude)

    # TODO Сюда можно добавить базовый фильтр и расширить функционал DAO
    async def count(
        self,
        *,
        filters: dict[str, typing.Any] | None = None,
        custom_filter: typing.Any | None = None,
    ) -> int:
        """
        Подсчитывает количество записей с возможностью фильтрации

        Args:
            filters: Словарь вида {"поле": "значение"} для простых фильтров
            custom_filter: Произвольное SQLAlchemy условие для сложных фильтров
        """
        stmt = select(func.count()).select_from(self.model)

        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)

        if custom_filter:
            stmt = stmt.where(custom_filter)

        return (await self.session.execute(stmt)).scalar_one() or 0

    async def get_many(
        self,
        *,
        exclude: list[str] | None = None,
        offset: int = 0,
        limit: int = 100,
        filters: dict[str, typing.Any] | None = None,
        custom_filter: dict[str, typing.Any] | None = None,
    ) -> ListTypeDTO:
        total = await self.count(filters=filters, custom_filter=custom_filter)

        # Получаем пагинированные данные
        stmt = select(self.model).offset(offset).limit(limit)

        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)

        if custom_filter:
            stmt = stmt.where(**custom_filter)

        result = await self.session.execute(stmt)
        dto_list = [
            self.mapper.to_dto(model, exclude_fields=exclude)
            for model in result.scalars()
        ]

        return self.mapper.to_list_dto(
            seq=dto_list, total=total, offset=offset, limit=limit
        )
