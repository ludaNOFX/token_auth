from dataclasses import dataclass
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums.role import RoleEnum
from src.application.database.holder import ModelBase
from src.data.mixin import TimeModelMixin


@dataclass
class UserModel(TimeModelMixin, ModelBase):
    """Пользователь"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    second_name: Mapped[str | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    role_id: Mapped[int | None] = mapped_column(
        ForeignKey("roles.id", ondelete="SET NULL"), nullable=True, index=True
    )
    role: Mapped["RoleModel"] = relationship(
        back_populates="users", lazy="selectin", uselist=False
    )

    def __repr__(self) -> str:
        return f"<User: {self.login}"


@dataclass
class RoleModel(TimeModelMixin, ModelBase):
    """Роль"""

    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, name="role_enum"), nullable=False, unique=True
    )
    users: Mapped[list["UserModel"]] = relationship(
        back_populates="role",
        lazy="noload",
        uselist=True,
    )
