"""empty message

Revision ID: 2c277fc68a7
Revises: 201e1e1e057
Create Date: 2015-03-26 15:52:07.013444

"""

# revision identifiers, used by Alembic.
revision = '2c277fc68a7'
down_revision = '201e1e1e057'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy_searchable import sync_trigger



def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()

    op.add_column('category', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_category_search_vector', 'category', ['search_vector'], unique=False, postgresql_using='gin')
    op.add_column('group', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_group_search_vector', 'group', ['search_vector'], unique=False, postgresql_using='gin')
    op.add_column('project', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_project_search_vector', 'project', ['search_vector'], unique=False, postgresql_using='gin')

    sync_trigger(conn, 'category', 'search_vector', ['name'])
    sync_trigger(conn, 'group', 'search_vector', ['name'])
    sync_trigger(conn, 'project', 'search_vector', ['name', 'summary'])

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_project_search_vector', table_name='project')
    op.drop_column('project', 'search_vector')
    op.drop_index('ix_group_search_vector', table_name='group')
    op.drop_column('group', 'search_vector')
    op.drop_index('ix_category_search_vector', table_name='category')
    op.drop_column('category', 'search_vector')
    ### end Alembic commands ###