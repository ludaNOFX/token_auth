from dataclasses import dataclass

from src.core.dto.base_dto import BaseDTO, BaseListDTO
from src.core.enums.role import RoleEnum


@dataclass
class UserDTO(BaseDTO):
    """Базовый DTO для пользователя"""

    id: int
    login: str
    role: RoleEnum | None = None
    first_name: str | None = None
    second_name: str | None = None
    description: str | None = None
    created_at: int | None = None
    updated_at: int | None = None
    role_id: int | None = None


@dataclass
class UserCreateDTO(BaseDTO):
    """DTO для создания пользователя"""

    login: str
    password: str
    role: RoleEnum | None = None
    role_id: int | None = None
    first_name: str | None = None
    second_name: str | None = None
    description: str | None = None


@dataclass
class UserUpdateDTO(BaseDTO):
    """DTO для обновления пользователя"""

    login: str | None = None
    role: RoleEnum | None = None
    role_id: int | None = None
    first_name: str | None = None
    second_name: str | None = None
    description: str | None = None
    password: str | None = None


@dataclass
class UserslistDTO(BaseListDTO[BaseDTO]): ...
