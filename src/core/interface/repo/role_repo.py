from src.core.dto.role import RoleCreateDTO, RoleDTO, RoleslistDTO
from src.core.interface.repo.base_repo import IBaseRepo


class IRoleRepo(
    IBaseRepo[
        RoleCreateDTO,
        RoleDTO,
        RoleslistDTO,
    ]
):
    """Интерфейс с специфичными для пользователя методами"""
