"""empty message

Revision ID: 3d7384fe644
Revises: 1a54c4cacbe
Create Date: 2015-03-24 13:47:51.125132

"""

# revision identifiers, used by Alembic.
revision = '3d7384fe644'
down_revision = '1a54c4cacbe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('git_url', sa.String(length=400), nullable=True))
    op.drop_column('project', 'github_url')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('github_url', sa.VARCHAR(length=400), autoincrement=False, nullable=True))
    op.drop_column('project', 'git_url')
    ### end Alembic commands ###
