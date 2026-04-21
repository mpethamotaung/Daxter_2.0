"""
Simple rule-based AI engine that answers financial queries by inspecting database state.
Simulates what a real LLM integration would do, but is fully self-contained.
"""
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import (
    FinancialRecord, TaxCompliance, AccountsReceivable, AccountsPayable, Alert,
)


async def _revenue_summary(session: AsyncSession) -> str:
    stmt = select(func.sum(FinancialRecord.amount)).where(
        FinancialRecord.transaction_type == "revenue"
    )
    result = await session.execute(stmt)
    total = result.scalar() or 0
    return f"Total recorded revenue: ${total:,.2f}."


async def _expense_summary(session: AsyncSession) -> str:
    stmt = select(func.sum(FinancialRecord.amount)).where(
        FinancialRecord.transaction_type == "expense"
    )
    result = await session.execute(stmt)
    total = result.scalar() or 0
    return f"Total recorded expenses: ${total:,.2f}."


async def _ar_summary(session: AsyncSession) -> str:
    stmt = select(func.sum(AccountsReceivable.amount)).where(
        AccountsReceivable.paid == False
    )
    result = await session.execute(stmt)
    total = result.scalar() or 0

    stmt2 = select(func.count()).select_from(AccountsReceivable).where(
        AccountsReceivable.paid == False, AccountsReceivable.days_overdue > 30
    )
    result2 = await session.execute(stmt2)
    overdue_count = result2.scalar() or 0

    return f"Outstanding receivables: ${total:,.2f}. {overdue_count} invoices are overdue by more than 30 days."


async def _ap_summary(session: AsyncSession) -> str:
    stmt = select(func.sum(AccountsPayable.amount)).where(
        AccountsPayable.paid == False
    )
    result = await session.execute(stmt)
    total = result.scalar() or 0
    return f"Outstanding payables: ${total:,.2f}."


async def _tax_summary(session: AsyncSession) -> str:
    now = datetime.datetime.utcnow()
    upcoming = now + datetime.timedelta(days=30)
    stmt = select(func.count()).select_from(TaxCompliance).where(
        TaxCompliance.deadline <= upcoming,
        TaxCompliance.status != "compliant",
    )
    result = await session.execute(stmt)
    count = result.scalar() or 0

    stmt2 = select(func.count()).select_from(TaxCompliance).where(
        TaxCompliance.status == "non_compliant"
    )
    result2 = await session.execute(stmt2)
    nc = result2.scalar() or 0

    return f"{count} tax filings due within 30 days need attention. {nc} filings are non-compliant."


async def _alert_summary(session: AsyncSession) -> str:
    stmt = select(func.count()).select_from(Alert).where(Alert.acknowledged == False)
    result = await session.execute(stmt)
    total = result.scalar() or 0

    stmt2 = select(func.count()).select_from(Alert).where(
        Alert.acknowledged == False, Alert.severity == "critical"
    )
    result2 = await session.execute(stmt2)
    critical = result2.scalar() or 0

    return f"{total} unacknowledged alerts ({critical} critical)."


async def _top_clients(session: AsyncSession) -> str:
    stmt = (
        select(
            FinancialRecord.client_name,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .where(
            FinancialRecord.transaction_type == "revenue",
            FinancialRecord.client_name.isnot(None),
        )
        .group_by(FinancialRecord.client_name)
        .order_by(func.sum(FinancialRecord.amount).desc())
        .limit(5)
    )
    result = await session.execute(stmt)
    rows = result.all()
    if not rows:
        return "No client revenue data available yet."
    lines = [f"  {i+1}. {name}: ${total:,.2f}" for i, (name, total) in enumerate(rows)]
    return "Top clients by revenue:\n" + "\n".join(lines)


KEYWORD_HANDLERS = {
    "revenue": _revenue_summary,
    "income": _revenue_summary,
    "expense": _expense_summary,
    "cost": _expense_summary,
    "spending": _expense_summary,
    "receivable": _ar_summary,
    "owed to us": _ar_summary,
    "invoice": _ar_summary,
    "payable": _ap_summary,
    "bills": _ap_summary,
    "we owe": _ap_summary,
    "tax": _tax_summary,
    "compliance": _tax_summary,
    "filing": _tax_summary,
    "deadline": _tax_summary,
    "alert": _alert_summary,
    "warning": _alert_summary,
    "risk": _alert_summary,
    "client": _top_clients,
    "customer": _top_clients,
}


async def answer_query(question: str, session: AsyncSession) -> str:
    q = question.lower()

    if any(w in q for w in ("summary", "overview", "dashboard", "everything", "status")):
        parts = [
            await _revenue_summary(session),
            await _expense_summary(session),
            await _ar_summary(session),
            await _ap_summary(session),
            await _tax_summary(session),
            await _alert_summary(session),
        ]
        return "Here's your financial overview:\n\n" + "\n\n".join(parts)

    for keyword, handler in KEYWORD_HANDLERS.items():
        if keyword in q:
            return await handler(session)

    return (
        "I can help with questions about revenue, expenses, receivables, payables, "
        "tax compliance, alerts, and client data. Try asking for a 'summary' to see everything."
    )
