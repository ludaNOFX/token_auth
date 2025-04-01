"""Потом создаю интерфейс для расширения функционала если нужно будет"""

from src.core.dto.user import UserCreateDTO, UserDTO, UserslistDTO
from src.core.interface.repo.base_repo import IBaseRepo


class IUserRepo(IBaseRepo[UserCreateDTO, UserDTO, UserslistDTO]):
    """Интерфейс с специфичными для пользователя методами"""
