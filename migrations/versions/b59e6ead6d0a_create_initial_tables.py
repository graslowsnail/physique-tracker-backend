"""Create initial tables

Revision ID: b59e6ead6d0a
Revises: d3c759b4b369
Create Date: 2025-03-15 23:23:26.137266

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b59e6ead6d0a'
down_revision = 'd3c759b4b369'
branch_labels = None
depends_on = None


def upgrade():
    # First drop foreign key constraints
    op.drop_constraint('pdf_page_project_id_fkey', 'pdf_page', type_='foreignkey')
    op.drop_constraint('project_user_id_fkey', 'project', type_='foreignkey')
    
    # Then drop tables in correct order (dependent tables first)
    op.drop_table('pdf_page')
    op.drop_table('project')
    op.drop_table('user')
    
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('folder_id', sa.String(length=255), nullable=False),
    sa.Column('image_path', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pdf_pages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('page_number', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('project_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('folder_id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='project_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='project_pkey'),
    sa.UniqueConstraint('folder_id', name='project_folder_id_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('pdf_page',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('page_number', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('image_path', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], name='pdf_page_project_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='pdf_page_pkey')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    op.drop_table('pdf_pages')
    op.drop_table('projects')
    op.drop_table('users')
    # ### end Alembic commands ###
