from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.database.holder import ModelBase
from src.data.mixin import TimeModelMixin


@dataclass
class User(TimeModelMixin, ModelBase):
    """Пользователь"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    second_name: Mapped[str | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    role_id: Mapped[str | None] = mapped_column(
        ForeignKey("roles.id", ondelete="SET NULL"), nullable=True, index=True
    )
    role: Mapped["Role"] = relationship(
        back_populates="users", lazy="selectin", uselist=False
    )


@dataclass
class Role(TimeModelMixin, ModelBase):
    """Роль"""

    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    users: Mapped[list["User"]] = relationship(
        back_populates="role",
        lazy="noload",
        uselist=True,
    )
