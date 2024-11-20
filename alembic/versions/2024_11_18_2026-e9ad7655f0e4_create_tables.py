"""create tables

Revision ID: e9ad7655f0e4
Revises: 
Create Date: 2024-11-18 20:26:11.857858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9ad7655f0e4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reminds',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.SMALLINT(), nullable=False),
    sa.Column('user_chat_id', sa.BIGINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_chat_id')
    )
    op.create_table('salary',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_chat_id', sa.BIGINT(), nullable=False),
    sa.Column('base_hours', sa.Float(), nullable=False),
    sa.Column('overtime', sa.Float(), nullable=False),
    sa.Column('earned', sa.Float(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('period', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_chat_id', sa.BIGINT(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('overtime', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings')
    op.drop_table('salary')
    op.drop_table('reminds')
    # ### end Alembic commands ###