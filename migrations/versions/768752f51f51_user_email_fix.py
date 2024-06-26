"""User.email fix

Revision ID: 768752f51f51
Revises: bd5c704186b5
Create Date: 2024-04-21 10:32:06.485478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '768752f51f51'
down_revision: Union[str, None] = 'bd5c704186b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'mail', nullable=False, new_column_name='email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    ...
    # ### end Alembic commands ###
