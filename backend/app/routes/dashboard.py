import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import (
    FinancialRecord, TaxCompliance, AccountsReceivable, AccountsPayable, Alert,
)
from app.schemas import DashboardSummary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_summary(db: AsyncSession = Depends(get_db)):
    # Revenue
    r = await db.execute(
        select(func.coalesce(func.sum(FinancialRecord.amount), 0)).where(
            FinancialRecord.transaction_type == "revenue"
        )
    )
    total_revenue = r.scalar()

    # Expenses
    r = await db.execute(
        select(func.coalesce(func.sum(FinancialRecord.amount), 0)).where(
            FinancialRecord.transaction_type == "expense"
        )
    )
    total_expenses = r.scalar()

    # Outstanding AR
    r = await db.execute(
        select(func.coalesce(func.sum(AccountsReceivable.amount), 0)).where(
            AccountsReceivable.paid == False
        )
    )
    outstanding_ar = r.scalar()

    # Outstanding AP
    r = await db.execute(
        select(func.coalesce(func.sum(AccountsPayable.amount), 0)).where(
            AccountsPayable.paid == False
        )
    )
    outstanding_ap = r.scalar()

    # Upcoming tax deadlines
    now = datetime.datetime.utcnow()
    r = await db.execute(
        select(func.count()).select_from(TaxCompliance).where(
            TaxCompliance.deadline >= now,
            TaxCompliance.deadline <= now + datetime.timedelta(days=30),
        )
    )
    upcoming_tax = r.scalar()

    # Compliance warnings
    r = await db.execute(
        select(func.count()).select_from(TaxCompliance).where(
            TaxCompliance.status.in_(["warning", "non_compliant"])
        )
    )
    compliance_warnings = r.scalar()

    # Active agents (from orchestrator)
    from app.orchestrator import orchestrator
    active = sum(1 for a in orchestrator.agents if a.state != "stopped")

    # Alerts
    r = await db.execute(
        select(func.count()).select_from(Alert).where(Alert.acknowledged == False)
    )
    total_alerts = r.scalar()

    # Revenue trend (last 30 days, grouped by date)
    thirty_days_ago = now - datetime.timedelta(days=30)
    r = await db.execute(
        select(
            func.date(FinancialRecord.date).label("day"),
            func.sum(FinancialRecord.amount).label("total"),
        )
        .where(
            FinancialRecord.transaction_type == "revenue",
            FinancialRecord.date >= thirty_days_ago,
        )
        .group_by(func.date(FinancialRecord.date))
        .order_by(func.date(FinancialRecord.date))
    )
    revenue_trend = [{"date": str(row.day), "amount": round(row.total, 2)} for row in r.all()]

    # Expense by category
    r = await db.execute(
        select(
            FinancialRecord.category,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .where(FinancialRecord.transaction_type == "expense")
        .group_by(FinancialRecord.category)
        .order_by(func.sum(FinancialRecord.amount).desc())
    )
    expense_by_cat = [{"category": row.category, "amount": round(row.total, 2)} for row in r.all()]

    return DashboardSummary(
        total_revenue=round(total_revenue, 2),
        total_expenses=round(total_expenses, 2),
        net_income=round(total_revenue - total_expenses, 2),
        outstanding_receivables=round(outstanding_ar, 2),
        outstanding_payables=round(outstanding_ap, 2),
        upcoming_tax_deadlines=upcoming_tax,
        compliance_warnings=compliance_warnings,
        active_agents=active,
        total_alerts=total_alerts,
        revenue_trend=revenue_trend,
        expense_by_category=expense_by_cat,
    )
