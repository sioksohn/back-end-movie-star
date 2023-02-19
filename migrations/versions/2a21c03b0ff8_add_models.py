"""add models

Revision ID: 2a21c03b0ff8
Revises: 
Create Date: 2023-02-19 14:55:51.527202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a21c03b0ff8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poster', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('media_type', sa.String(), nullable=False),
    sa.Column('vote_average', sa.Float(), nullable=False),
    sa.Column('genre_ids', sa.ARRAY(sa.Integer()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('viewer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('content_genre',
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.PrimaryKeyConstraint('content_id', 'genre_id')
    )
    op.create_table('watchlist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('viewer_id', sa.Integer(), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('viewer_rate', sa.Float(), nullable=True),
    sa.Column('viewer_comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.ForeignKeyConstraint(['viewer_id'], ['viewer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watchlist')
    op.drop_table('content_genre')
    op.drop_table('viewer')
    op.drop_table('genre')
    op.drop_table('content')
    # ### end Alembic commands ###