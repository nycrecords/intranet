"""added monitor table

Revision ID: 044e18572cbe
Revises: ea83afbe3ffc
Create Date: 2023-08-07 15:45:48.602737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '044e18572cbe'
down_revision = 'ea83afbe3ffc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monitor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('status_code', sa.String(), nullable=True),
    sa.Column('current_timestamp', sa.DateTime(), nullable=True),
    sa.Column('last_success_timestamp', sa.DateTime(), nullable=True),
    sa.Column('response_header', sa.String(), nullable=True),
    sa.Column('use_ssl', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('monitor')
    # ### end Alembic commands ###
