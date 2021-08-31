"""First Migration

Revision ID: 7a17989aa1e3
Revises: 
Create Date: 2021-08-31 19:23:49.227719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a17989aa1e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'external_id', name='unique_cre_fields')
    )
    op.create_table('standard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('section', sa.String(), nullable=False),
    sa.Column('subsection', sa.String(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'section', 'subsection', name='standard_section')
    )
    op.create_table('crelinks',
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('group', sa.Integer(), nullable=False),
    sa.Column('cre', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cre'], ['cre.id'], ),
    sa.ForeignKeyConstraint(['group'], ['cre.id'], ),
    sa.PrimaryKeyConstraint('group', 'cre')
    )
    op.create_table('links',
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('cre', sa.Integer(), nullable=False),
    sa.Column('standard', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cre'], ['cre.id'], ),
    sa.ForeignKeyConstraint(['standard'], ['standard.id'], ),
    sa.PrimaryKeyConstraint('cre', 'standard')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('links')
    op.drop_table('crelinks')
    op.drop_table('standard')
    op.drop_table('cre')
    # ### end Alembic commands ###


