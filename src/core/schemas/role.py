from collections.abc import Sequence
from pydantic import BaseModel

from src.core.enums.role import RoleEnum


class RoleCreateSchema(BaseModel):
    name: RoleEnum


class RoleSchema(BaseModel):
    id: int
    name: RoleEnum
    created_at: int
    updated_at: int


class ListRoleSchema(BaseModel):
    total: int | None = None
    offset: int = 0
    limit: int = 100
    items: Sequence[RoleSchema] | None = None
