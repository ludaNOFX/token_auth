from collections.abc import Sequence
from pydantic import BaseModel, field_validator

from src.core.enums.role import RoleEnum


class UserCreateSchema(BaseModel):
    login: str
    password: str
    role: RoleEnum
    first_name: str | None = None
    second_name: str | None = None
    description: str | None = None

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserSchema(BaseModel):
    id: int
    login: str
    role: RoleEnum | None = None
    first_name: str | None = None
    second_name: str | None = None
    description: str | None = None
    created_at: int | None = None
    updated_at: int | None = None


class ListUserSchema(BaseModel):
    total: int | None = None
    offset: int = 0
    limit: int = 100
    items: Sequence[UserSchema] | None = None
