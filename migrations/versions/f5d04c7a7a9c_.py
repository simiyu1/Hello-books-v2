"""empty message

Revision ID: f5d04c7a7a9c
Revises: b078bcb0c822
Create Date: 2018-06-25 12:07:12.669894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5d04c7a7a9c'
down_revision = 'b078bcb0c822'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_role_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_role_key', 'users', ['role'])
    # ### end Alembic commands ###