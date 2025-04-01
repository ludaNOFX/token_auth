from datetime import datetime

from sqlalchemy import inspect, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped


# class DictModelMixin:
#     """Миксин преобразования модели в словарь"""

#     def to_dict(self) -> dict:
#         """Преобразование в словарь
#         *Тип datetime конвертируется в int(timestamp)

#         **Example:**
#         '''
#             python:
#         >> MyModel.to_dict()
#         >> _
#         >> returns {"age": 5, "name": "arnold"}
#         '''
#         """

#         d = {}
#         for x in self.__table__.columns:  # type: ignore
#             val = getattr(self, x.name)
#             if isinstance(val, datetime):
#                 val = int(val.timestamp())
#             d[x.name] = val

#         for key, prop in inspect(self.__class__).all_orm_descriptors.items():
#             if isinstance(prop, hybrid_property):
#                 d[key] = getattr(self, key)

#         return d


class DictModelMixin:
    """Миксин преобразования модели в словарь с возможностью исключения полей"""

    @classmethod
    def get_excluded_fields(cls) -> list[str]:
        """Возвращает список полей, которые нужно исключить при преобразовании в словарь"""  # noqa: E501
        return [
            "password",
        ]  # Базовый список исключаемых полей

    def to_dict(self, exclude: list[str] | None = None) -> dict:
        """Преобразование в словарь с исключением указанных полей

        Args:
            exclude: Дополнительные поля для исключения (добавляются к get_excluded_fields())

        Returns:
            Словарь с данными модели, исключая чувствительные поля

        Example:
            >>> user.to_dict()
            {'id': 1, 'name': 'John'}  # без поля password

            >>> user.to_dict(exclude=['token'])
            {'id': 1, 'name': 'John'}  # без password и token
        """  # noqa: E501
        if exclude is None:
            exclude = []

        # Объединяем базовые исключаемые поля с переданными
        excluded_fields = set(self.get_excluded_fields() + exclude)

        d = {}

        # Обрабатываем обычные колонки
        for column in self.__table__.columns:  # type: ignore
            if column.name in excluded_fields:
                continue

            val = getattr(self, column.name)
            if isinstance(val, datetime):
                val = int(val.timestamp())
            d[column.name] = val

        # Обрабатываем hybrid-свойства
        for key, prop in inspect(self.__class__).all_orm_descriptors.items():  # type: ignore
            if key in excluded_fields:
                continue

            if isinstance(prop, hybrid_property):
                d[key] = getattr(self, key)

        return d


class TimeModelMixin:
    """Миксин добавления полей created_at, updated_at, которые автоматичесческий проставляються при создании и обновлении соответственно."""  # noqa: E501

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
