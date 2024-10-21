"""update task table

Revision ID: 9aae8e445c09
Revises: e1a1c31e81d8
Create Date: 2024-10-21 17:19:30.228664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aae8e445c09'
down_revision: Union[str, None] = 'e1a1c31e81d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('task', 'createdAt', new_column_name='created_at')
    op.alter_column('task', 'updatedAt', new_column_name='updated_at')


def downgrade() -> None:
    op.alter_column('task', 'created_at', new_column_name='createdAt')
    op.alter_column('task', 'updated_at', new_column_name='updatedAt')
