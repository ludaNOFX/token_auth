import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from src.core.enums.role import RoleEnum


Base = declarative_base()

RoleEnumType: sa.Enum = sa.Enum(
    RoleEnum,
    name="role_enum",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)
