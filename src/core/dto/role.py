from dataclasses import dataclass

from src.core.enums.role import RoleEnum
from src.core.dto.base_dto import BaseDTO, BaseListDTO


@dataclass
class RoleCreateDTO(BaseDTO):
    """DTO для создания пользователя"""

    name: RoleEnum


@dataclass
class RoleDTO(RoleCreateDTO):
    """Базовый DTO для пользователя"""

    id: int
    created_at: int
    updated_at: int


@dataclass
class RoleUpdateDTO(RoleCreateDTO):
    """DTO для обновления пользователя"""


@dataclass
class RoleslistDTO(BaseListDTO[BaseDTO]): ...
