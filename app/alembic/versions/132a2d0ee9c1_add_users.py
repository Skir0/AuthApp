"""add services

Revision ID: 132a2d0ee9c1
Revises: 10b0813ef688
Create Date: 2026-09-19 14:22:52.639161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '132a2d0ee9c1'
down_revision: Union[str, Sequence[str], None] = '10b0813ef688'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
