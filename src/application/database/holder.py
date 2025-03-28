from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.data.mixin import DictModelMixin


convention = {
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s",
}

meta = MetaData(naming_convention=convention)


class ModelBase(DeclarativeBase, DictModelMixin):
    metadata = meta
