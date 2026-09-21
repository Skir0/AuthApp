"""add services

Revision ID: 10b0813ef688
Revises: df800b2cee7a
Create Date: 2026-09-19 14:22:15.566623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10b0813ef688'
down_revision: Union[str, Sequence[str], None] = 'df800b2cee7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
