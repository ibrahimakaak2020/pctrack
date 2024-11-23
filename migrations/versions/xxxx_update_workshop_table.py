"""update workshop table

Revision ID: xxxx
Revises: previous_revision
Create Date: 2024-xx-xx

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add location foreign key
    op.add_column('workshop', sa.Column('locid', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_workshop_location', 'workshop', 'location',
                         ['locid'], ['locid'])
    
    # Remove description column
    op.drop_column('workshop', 'description')
    
    # Make locid not nullable after data migration
    op.alter_column('workshop', 'locid', nullable=False)

def downgrade():
    # Remove foreign key and location column
    op.drop_constraint('fk_workshop_location', 'workshop', type_='foreignkey')
    op.drop_column('workshop', 'locid')
    
    # Add back description column
    op.add_column('workshop', sa.Column('description', sa.String(length=200))) 