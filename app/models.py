from sqlalchemy import Column, BigInteger, Text, Date, Boolean, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(Text, unique=True, nullable=False)

class OAuthCredentials(Base):
    __tablename__ = "oauth_credentials"
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = Column(Text, nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    scope = Column(Text)
    user = relationship("User")

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, unique=True)

class Category(Base):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, unique=True)

class ExpenseReport(Base):
    __tablename__ = "expense_reports"
    id = Column(BigInteger, primary_key=True)
    zoho_report_id = Column(Text, unique=True)
    title = Column(Text)
    report_number = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Text)
    total_amount = Column(Numeric(18,2))
    currency = Column(Text)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(BigInteger, primary_key=True)
    zoho_expense_id = Column(Text, unique=True)
    report_id = Column(BigInteger, ForeignKey("expense_reports.id", ondelete="SET NULL"))
    txn_date = Column(Date, nullable=False)
    merchant = Column(Text)
    vendor_id = Column(BigInteger, ForeignKey("vendors.id"))
    category_id = Column(BigInteger, ForeignKey("categories.id"))
    description = Column(Text)
    amount = Column(Numeric(18,2), nullable=False)
    currency = Column(Text, nullable=False)
    exchange_rate = Column(Numeric(18,6))
    amount_home = Column(Numeric(18,2))
    payment_mode = Column(Text)
    reimbursable = Column(Boolean, default=True)
    company_report_status = Column(Text, default="Pending")
    reimbursement_status = Column(Text, default="Not Reimbursed")
    reimbursed_amount = Column(Numeric(18,2), default=0)
    reimbursed_date = Column(Date)
    external_ref = Column(Text)

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(BigInteger, primary_key=True)
    expense_id = Column(BigInteger, ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False)
    zoho_file_id = Column(Text)
    filename = Column(Text)
    mime_type = Column(Text)
    size_bytes = Column(BigInteger)
    url = Column(Text)

class SyncState(Base):
    __tablename__ = "sync_state"
    id = Column(BigInteger, primary_key=True)
    provider = Column(Text, nullable=False)
    cursor = Column(Text)
    last_run_at = Column(TIMESTAMP(timezone=True))
    status = Column(Text)
    message = Column(Text)
