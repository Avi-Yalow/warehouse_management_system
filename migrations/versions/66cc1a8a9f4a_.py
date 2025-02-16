"""empty message

Revision ID: 66cc1a8a9f4a
Revises: 
Create Date: 2025-02-11 12:09:43.819456

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '66cc1a8a9f4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operation',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('operation_type', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('completed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='operation_product_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='operation_pkey')
    )
    # ### end Alembic commands ###
