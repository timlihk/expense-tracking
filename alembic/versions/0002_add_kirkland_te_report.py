"""Add Kirkland T&E report reference field

Revision ID: 0002
Revises: 0001
Create Date: 2024-09-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    # Add kirkland_te_report column to expenses table
    op.add_column('expenses', sa.Column('kirkland_te_report', sa.Text(), nullable=True))

    # Create index for efficient queries
    op.create_index('idx_expenses_kirkland_te_report', 'expenses', ['kirkland_te_report'])


def downgrade():
    # Remove index and column
    op.drop_index('idx_expenses_kirkland_te_report', table_name='expenses')
    op.drop_column('expenses', 'kirkland_te_report')