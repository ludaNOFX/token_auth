from datetime import datetime
from sqlalchemy import inspect, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped


class DictModelMixin:
    """Миксин преобразования модели в словарь"""

    def to_dict(self) -> dict:
        """Преобразование в словарь
        *Тип datetime конвертируется в int(timestamp)

        **Example:**
        '''
            python:
        >> MyModel.to_dict()
        >> _
        >> returns {"age": 5, "name": "arnold"}
        '''
        """

        d = {}
        for x in self.__table__.columns:  # type: ignore
            val = getattr(self, x.name)
            if isinstance(val, datetime):
                val = int(val.timestamp())
            d[x.name] = val

        for key, prop in inspect(self.__class__).all_orm_descriptors.items():  # type: ignore
            if isinstance(prop, hybrid_property):
                d[key] = getattr(self, key)

        return d


class TimeModelMixin:
    """Миксин добавления полей created_at, updated_at, которые автоматичесческий проставляються при создании и обновлении соответственно."""  # noqa: E501

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
