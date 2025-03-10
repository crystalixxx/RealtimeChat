"""empty message

Revision ID: c2141fc20a10
Revises: 548e630d33d8
Create Date: 2024-10-29 21:53:40.273825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2141fc20a10'
down_revision: Union[str, None] = '548e630d33d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_superadmin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_superadmin')
    # ### end Alembic commands ###
