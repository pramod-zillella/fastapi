"""add content column to posts table

Revision ID: 7f78f66ec9a7
Revises: 56952aadc358
Create Date: 2024-10-06 13:23:05.000243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f78f66ec9a7'
down_revision: Union[str, None] = '56952aadc358'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
