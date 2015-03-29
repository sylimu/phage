"""empty message

Revision ID: 4b5f6069c5df
Revises: 17fa4624585
Create Date: 2015-03-11 09:51:51.320315

"""

# revision identifiers, used by Alembic.
revision = '4b5f6069c5df'
down_revision = '17fa4624585'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('database', sa.Column('name_slug', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_database_name_slug'), 'database', ['name_slug'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_database_name_slug'), table_name='database')
    op.drop_column('database', 'name_slug')
    ### end Alembic commands ###