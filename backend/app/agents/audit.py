import random
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.agents.base import BaseAgent
from app.models import FinancialRecord, Alert


class AuditAgent(BaseAgent):
    def __init__(self):
        super().__init__("Audit Agent")

    async def collect_data(self, session: AsyncSession) -> int:
        now = datetime.datetime.utcnow()
        alerts_created = 0

        # Check for unusually large transactions
        stmt = select(FinancialRecord).where(FinancialRecord.amount > 20000)
        result = await session.execute(stmt)
        large_txns = result.scalars().all()
        for txn in large_txns[-3:]:
            if random.random() < 0.3:
                alert = Alert(
                    severity="warning",
                    title=f"Large transaction flagged: ${txn.amount:,.2f}",
                    message=f"Category: {txn.category}. {txn.description}. Review recommended.",
                    source_agent=self.name,
                    created_at=now,
                )
                session.add(alert)
                alerts_created += 1

        # Check for duplicate-looking entries
        stmt = (
            select(
                FinancialRecord.category,
                FinancialRecord.amount,
                func.count().label("cnt"),
            )
            .group_by(FinancialRecord.category, FinancialRecord.amount)
            .having(func.count() > 2)
        )
        result = await session.execute(stmt)
        duplicates = result.all()
        for cat, amount, cnt in duplicates[:2]:
            if random.random() < 0.4:
                alert = Alert(
                    severity="info",
                    title=f"Potential duplicate entries detected",
                    message=f"{cnt} entries in '{cat}' with identical amount ${amount:,.2f}.",
                    source_agent=self.name,
                    created_at=now,
                )
                session.add(alert)
                alerts_created += 1

        # Simulated ratio check
        if random.random() < 0.2:
            alert = Alert(
                severity="info",
                title="Expense ratio review",
                message="Monthly expense-to-revenue ratio exceeds 70% threshold. Management review suggested.",
                source_agent=self.name,
                created_at=now,
            )
            session.add(alert)
            alerts_created += 1

        await session.flush()
        return alerts_created
