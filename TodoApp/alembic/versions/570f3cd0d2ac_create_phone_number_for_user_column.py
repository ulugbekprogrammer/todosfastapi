"""Create phone number for user column

Revision ID:  
Revises: 
Create Date: 2025-03-16 12:19:16.555587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '570f3cd0d2ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')
