"""Renaming tables Seller, Purchase

Revision ID: aec1688a7543
Revises: e07b1d939092
Create Date: 2024-04-16 16:29:04.566174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'aec1688a7543'
down_revision: Union[str, None] = 'e07b1d939092'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('purchase', 'deal')
    op.rename_table('seller', 'provider')
    op.alter_column('contract', 'seller_id', nullable=False, new_column_name='provider_id')
    op.alter_column('payment', 'purchase_id', nullable=False, new_column_name='deal_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    ...
    # ### end Alembic commands ###