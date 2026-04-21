import datetime
from sqlalchemy import String, Float, Integer, DateTime, Text, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum


class TransactionType(str, enum.Enum):
    REVENUE = "revenue"
    EXPENSE = "expense"
    TAX_PAYMENT = "tax_payment"
    INVOICE = "invoice"
    BILL = "bill"


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    WARNING = "warning"
    NON_COMPLIANT = "non_compliant"
    PENDING = "pending"


class AgentState(str, enum.Enum):
    RUNNING = "running"
    IDLE = "idle"
    ERROR = "error"
    STOPPED = "stopped"


class AlertSeverity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    category: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    amount: Mapped[float] = mapped_column(Float)
    transaction_type: Mapped[str] = mapped_column(String(50))
    source_agent: Mapped[str] = mapped_column(String(100))
    client_name: Mapped[str] = mapped_column(String(200), nullable=True)


class TaxCompliance(Base):
    __tablename__ = "tax_compliance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filing_type: Mapped[str] = mapped_column(String(100))
    jurisdiction: Mapped[str] = mapped_column(String(100))
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(50))
    amount_due: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)


class AccountsReceivable(Base):
    __tablename__ = "accounts_receivable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_name: Mapped[str] = mapped_column(String(200))
    invoice_number: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Float)
    issued_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    due_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    paid: Mapped[bool] = mapped_column(Boolean, default=False)
    days_overdue: Mapped[int] = mapped_column(Integer, default=0)


class AccountsPayable(Base):
    __tablename__ = "accounts_payable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vendor_name: Mapped[str] = mapped_column(String(200))
    bill_number: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Float)
    received_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    due_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    paid: Mapped[bool] = mapped_column(Boolean, default=False)
    category: Mapped[str] = mapped_column(String(100))


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    severity: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    source_agent: Mapped[str] = mapped_column(String(100))
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)


class QueryHistory(Base):
    __tablename__ = "query_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
