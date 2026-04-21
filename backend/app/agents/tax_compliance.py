import random
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.agents.base import BaseAgent
from app.models import TaxCompliance, Alert

FILINGS = [
    ("Form 1040", "Federal", "Individual income tax return"),
    ("Form 1120", "Federal", "Corporate income tax return"),
    ("Form 941", "Federal", "Quarterly employment tax"),
    ("Form 940", "Federal", "Annual FUTA tax return"),
    ("State Income Tax", "California", "CA state income tax filing"),
    ("State Income Tax", "New York", "NY state income tax filing"),
    ("Sales Tax Return", "Texas", "TX quarterly sales tax"),
    ("Form 1099-NEC", "Federal", "Non-employee compensation reporting"),
    ("Property Tax", "Los Angeles County", "Annual property tax assessment"),
    ("Payroll Tax", "Federal", "Quarterly payroll tax deposit"),
]


class TaxComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Tax Compliance Agent")

    async def collect_data(self, session: AsyncSession) -> int:
        now = datetime.datetime.utcnow()
        count = 0

        for filing_type, jurisdiction, notes in random.sample(FILINGS, k=random.randint(2, 5)):
            days_until = random.randint(-5, 60)
            deadline = now + datetime.timedelta(days=days_until)

            if days_until < 0:
                status = random.choice(["compliant", "non_compliant"])
            elif days_until < 14:
                status = "warning"
            else:
                status = random.choice(["compliant", "pending"])

            record = TaxCompliance(
                filing_type=filing_type,
                jurisdiction=jurisdiction,
                deadline=deadline,
                status=status,
                amount_due=round(random.uniform(500, 50000), 2),
                notes=notes,
                last_updated=now,
            )
            session.add(record)
            count += 1

            if status in ("warning", "non_compliant"):
                severity = "critical" if status == "non_compliant" else "warning"
                alert = Alert(
                    severity=severity,
                    title=f"Tax Filing: {filing_type} ({jurisdiction})",
                    message=f"{'OVERDUE' if days_until < 0 else 'Due in ' + str(days_until) + ' days'}. Amount: ${record.amount_due:,.2f}",
                    source_agent=self.name,
                    created_at=now,
                )
                session.add(alert)

        await session.flush()
        return count
