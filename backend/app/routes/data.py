from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import FinancialRecord, TaxCompliance, AccountsReceivable, AccountsPayable
from app.schemas import FinancialRecordOut, TaxComplianceOut, AROut, APOut

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/financial", response_model=list[FinancialRecordOut])
async def get_financial_records(
    limit: int = Query(50, le=200),
    tx_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(FinancialRecord).order_by(FinancialRecord.date.desc())
    if tx_type:
        stmt = stmt.where(FinancialRecord.transaction_type == tx_type)
    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/tax-compliance", response_model=list[TaxComplianceOut])
async def get_tax_compliance(
    limit: int = Query(50, le=200),
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(TaxCompliance).order_by(TaxCompliance.deadline.asc())
    if status:
        stmt = stmt.where(TaxCompliance.status == status)
    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/receivables", response_model=list[AROut])
async def get_receivables(
    limit: int = Query(50, le=200),
    overdue_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(AccountsReceivable).order_by(AccountsReceivable.due_date.asc())
    if overdue_only:
        stmt = stmt.where(AccountsReceivable.paid == False, AccountsReceivable.days_overdue > 0)
    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/payables", response_model=list[APOut])
async def get_payables(
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(AccountsPayable).order_by(AccountsPayable.due_date.asc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
