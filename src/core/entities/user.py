from dataclasses import dataclass

from src.core.dto.user import UserCreateDTO
from src.core.enums.role import RoleEnum


@dataclass
class UserCreateEntity:
    login: str
    role: RoleEnum
    password: str
    first_name: str | None = None
    second_name: str | None = None
    description: str | None = None
    role_id: int | None = None

    def set_hash_password(self, password: str) -> None:
        self.password = password

    def set_role_id(self, role_id: int) -> None:
        self.role_id = role_id

    def entity_to_dto(self) -> UserCreateDTO:
        return UserCreateDTO(
            login=self.login,
            password=self.password,
            first_name=self.first_name,
            second_name=self.second_name,
            description=self.description,
            role_id=self.role_id,
        )
