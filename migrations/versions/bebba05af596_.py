"""empty message

Revision ID: bebba05af596
Revises: a7ab67490064
Create Date: 2020-10-19 10:14:46.305821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bebba05af596'
down_revision = 'a7ab67490064'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_notification_read_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_notification_read_time')
    # ### end Alembic commands ###
