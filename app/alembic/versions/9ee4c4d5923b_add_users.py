"""add services

Revision ID: 9ee4c4d5923b
Revises: 132a2d0ee9c1
Create Date: 2026-09-19 14:23:59.827216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ee4c4d5923b'
down_revision: Union[str, Sequence[str], None] = '132a2d0ee9c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
