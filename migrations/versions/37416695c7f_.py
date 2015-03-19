"""empty message

Revision ID: 37416695c7f
Revises: 20180558979
Create Date: 2015-03-18 16:49:53.568838

"""

# revision identifiers, used by Alembic.
revision = '37416695c7f'
down_revision = '20180558979'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('contributors_count', sa.Integer(), nullable=True))
    op.add_column('project', sa.Column('downloads_count', sa.Integer(), nullable=True))
    op.add_column('project', sa.Column('forks_count', sa.Integer(), nullable=True))
    op.add_column('project', sa.Column('open_issues_count', sa.Integer(), nullable=True))
    op.add_column('project', sa.Column('python_three_compatible', sa.Boolean(), nullable=True))
    op.add_column('project', sa.Column('starred_count', sa.Integer(), nullable=True))
    op.add_column('project', sa.Column('watchers_count', sa.Integer(), nullable=True))
    op.drop_column('project', 'total_downloads')
    op.drop_column('project', 'number_of_contributors')
    op.drop_column('project', 'open_issues')
    op.drop_column('project', 'watchers')
    op.drop_column('project', 'forks')
    op.drop_column('project', 'starred')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('starred', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('project', sa.Column('forks', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('project', sa.Column('watchers', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('project', sa.Column('open_issues', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('project', sa.Column('number_of_contributors', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('project', sa.Column('total_downloads', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('project', 'watchers_count')
    op.drop_column('project', 'starred_count')
    op.drop_column('project', 'python_three_compatible')
    op.drop_column('project', 'open_issues_count')
    op.drop_column('project', 'forks_count')
    op.drop_column('project', 'downloads_count')
    op.drop_column('project', 'contributors_count')
    ### end Alembic commands ###