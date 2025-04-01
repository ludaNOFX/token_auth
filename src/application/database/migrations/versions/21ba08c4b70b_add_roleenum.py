"""add roleEnum

Revision ID: 21ba08c4b70b
Revises:
Create Date: 2025-04-01 10:49:33.303410

"""

from collections.abc import Sequence
from alembic import op

from src.application.database.migrations.const.enum import RoleEnumType


# revision identifiers, used by Alembic.
revision: str = "21ba08c4b70b"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    RoleEnumType.create(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    """Downgrade schema."""
    RoleEnumType.drop(op.get_bind(), checkfirst=False)
