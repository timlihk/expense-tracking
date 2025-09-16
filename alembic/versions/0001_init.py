from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    op.execute("CREATE EXTENSION IF NOT EXISTS uuid-ossp;")

    op.create_table('users',
        sa.Column('id', sa.Uuid(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('email', sa.Text(), nullable=False, unique=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

    op.create_table('oauth_credentials',
        sa.Column('id', sa.Uuid(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('user_id', sa.Uuid(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('provider', sa.Text(), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('refresh_token', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('scope', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

    op.create_table('vendors',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('name', sa.Text(), unique=True)
    )

    op.create_table('categories',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('name', sa.Text(), unique=True)
    )

    op.create_table('expense_reports',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('zoho_report_id', sa.Text(), unique=True),
        sa.Column('title', sa.Text()),
        sa.Column('report_number', sa.Text()),
        sa.Column('start_date', sa.Date()),
        sa.Column('end_date', sa.Date()),
        sa.Column('status', sa.Text()),
        sa.Column('total_amount', sa.Numeric(18,2)),
        sa.Column('currency', sa.Text()),
        sa.Column('submitted_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('approved_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

    op.create_table('expenses',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('zoho_expense_id', sa.Text(), unique=True),
        sa.Column('report_id', sa.BigInteger(), sa.ForeignKey('expense_reports.id', ondelete='SET NULL')),
        sa.Column('txn_date', sa.Date(), nullable=False),
        sa.Column('merchant', sa.Text()),
        sa.Column('vendor_id', sa.BigInteger(), sa.ForeignKey('vendors.id')),
        sa.Column('category_id', sa.BigInteger(), sa.ForeignKey('categories.id')),
        sa.Column('description', sa.Text()),
        sa.Column('amount', sa.Numeric(18,2), nullable=False),
        sa.Column('currency', sa.Text(), nullable=False),
        sa.Column('exchange_rate', sa.Numeric(18,6)),
        sa.Column('amount_home', sa.Numeric(18,2)),
        sa.Column('payment_mode', sa.Text()),
        sa.Column('reimbursable', sa.Boolean(), server_default=sa.text('true')),
        sa.Column('company_report_status', sa.Text(), server_default='Pending'),
        sa.Column('reimbursement_status', sa.Text(), server_default='Not Reimbursed'),
        sa.Column('reimbursed_amount', sa.Numeric(18,2), server_default='0'),
        sa.Column('reimbursed_date', sa.Date()),
        sa.Column('external_ref', sa.Text()),
        sa.Column('kirkland_te_report', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

    op.create_table('attachments',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('expense_id', sa.BigInteger(), sa.ForeignKey('expenses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('zoho_file_id', sa.Text()),
        sa.Column('filename', sa.Text()),
        sa.Column('mime_type', sa.Text()),
        sa.Column('size_bytes', sa.BigInteger()),
        sa.Column('url', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

    op.create_table('sync_state',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('provider', sa.Text(), nullable=False),
        sa.Column('cursor', sa.Text()),
        sa.Column('last_run_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('status', sa.Text()),
        sa.Column('message', sa.Text())
    )

    op.create_index('idx_expenses_txn_date', 'expenses', ['txn_date'])
    op.create_index('idx_expenses_report_id', 'expenses', ['report_id'])
    op.create_index('idx_expenses_status', 'expenses', ['reimbursement_status'])
    op.create_index('idx_expenses_kirkland_te_report', 'expenses', ['kirkland_te_report'])

def downgrade():
    op.drop_index('idx_expenses_kirkland_te_report', table_name='expenses')
    op.drop_index('idx_expenses_status', table_name='expenses')
    op.drop_index('idx_expenses_report_id', table_name='expenses')
    op.drop_index('idx_expenses_txn_date', table_name='expenses')
    op.drop_table('sync_state')
    op.drop_table('attachments')
    op.drop_table('expenses')
    op.drop_table('expense_reports')
    op.drop_table('categories')
    op.drop_table('vendors')
    op.drop_table('oauth_credentials')
    op.drop_table('users')
