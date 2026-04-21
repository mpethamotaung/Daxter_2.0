from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FinancialRecordOut(BaseModel):
    id: int
    date: datetime
    category: str
    description: str
    amount: float
    transaction_type: str
    source_agent: str
    client_name: Optional[str] = None

    class Config:
        from_attributes = True


class TaxComplianceOut(BaseModel):
    id: int
    filing_type: str
    jurisdiction: str
    deadline: datetime
    status: str
    amount_due: float
    notes: Optional[str] = None
    last_updated: datetime

    class Config:
        from_attributes = True


class AROut(BaseModel):
    id: int
    client_name: str
    invoice_number: str
    amount: float
    issued_date: datetime
    due_date: datetime
    paid: bool
    days_overdue: int

    class Config:
        from_attributes = True


class APOut(BaseModel):
    id: int
    vendor_name: str
    bill_number: str
    amount: float
    received_date: datetime
    due_date: datetime
    paid: bool
    category: str

    class Config:
        from_attributes = True


class AgentLogOut(BaseModel):
    id: int
    agent_name: str
    state: str
    message: str
    records_processed: int
    timestamp: datetime

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    severity: str
    title: str
    message: str
    source_agent: str
    acknowledged: bool
    created_at: datetime

    class Config:
        from_attributes = True


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    timestamp: datetime


class DashboardSummary(BaseModel):
    total_revenue: float
    total_expenses: float
    net_income: float
    outstanding_receivables: float
    outstanding_payables: float
    upcoming_tax_deadlines: int
    compliance_warnings: int
    active_agents: int
    total_alerts: int
    revenue_trend: list[dict]
    expense_by_category: list[dict]


class AgentStatusOut(BaseModel):
    name: str
    state: str
    last_run: Optional[datetime] = None
    records_processed: int
    error_count: int
