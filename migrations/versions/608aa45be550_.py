"""empty message

Revision ID: 608aa45be550
Revises: 
Create Date: 2022-05-23 19:04:44.224647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '608aa45be550'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('author_id', sa.Integer(), nullable=False))
    op.drop_constraint('comments_author_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'users', ['author_id'], ['id'], ondelete='CASCADE')
    op.drop_column('comments', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('author', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_author_fkey', 'comments', 'users', ['author'], ['id'])
    op.drop_column('comments', 'author_id')
    # ### end Alembic commands ###
