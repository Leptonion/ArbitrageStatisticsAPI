"""First

Revision ID: e07b1d939092
Revises: 
Create Date: 2024-04-11 15:46:35.703909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e07b1d939092'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=50), nullable=False),
    sa.Column('position', sa.String(length=15), nullable=False),
    sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('add_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('contact', sa.String(length=100), nullable=False),
    sa.Column('from_source', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('seller',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('platform', sa.String(length=15), nullable=False),
    sa.Column('branch', sa.String(length=50), nullable=False),
    sa.Column('site', sa.String(length=250), nullable=True),
    sa.Column('contact', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contract',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('price_per_day', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=False),
    sa.Column('doc_link', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agent.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['seller.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('contract_id', sa.Integer(), nullable=True),
    sa.Column('full_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agent.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['contract_id'], ['contract.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purchase_id', sa.Integer(), nullable=True),
    sa.Column('pay_value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('create_date', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['purchase_id'], ['purchase.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    op.drop_table('purchase')
    op.drop_table('contract')
    op.drop_table('seller')
    op.drop_table('client')
    op.drop_table('agent')
    # ### end Alembic commands ###
