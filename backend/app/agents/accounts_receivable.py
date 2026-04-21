import random
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.base import BaseAgent
from app.models import AccountsReceivable, Alert

CLIENTS = [
    "Meridian Corp", "Atlas Manufacturing", "Pinnacle Retail", "Vertex Solutions",
    "Horizon Healthcare", "Summit Logistics", "Cascade Financial", "Ironwood Construction",
    "Sterling Enterprises", "BlueWave Technologies",
]


class AccountsReceivableAgent(BaseAgent):
    def __init__(self):
        super().__init__("Accounts Receivable Agent")
        self._invoice_counter = 1000

    async def collect_data(self, session: AsyncSession) -> int:
        now = datetime.datetime.utcnow()
        count = 0

        for _ in range(random.randint(2, 6)):
            self._invoice_counter += 1
            days_ago = random.randint(5, 90)
            issued = now - datetime.timedelta(days=days_ago)
            due = issued + datetime.timedelta(days=30)
            paid = random.random() < 0.4
            overdue = max(0, (now - due).days) if not paid else 0

            record = AccountsReceivable(
                client_name=random.choice(CLIENTS),
                invoice_number=f"INV-{self._invoice_counter}",
                amount=round(random.uniform(2000, 50000), 2),
                issued_date=issued,
                due_date=due,
                paid=paid,
                days_overdue=overdue,
            )
            session.add(record)
            count += 1

            if overdue > 60:
                alert = Alert(
                    severity="critical",
                    title=f"Severely overdue invoice: {record.invoice_number}",
                    message=f"{record.client_name} owes ${record.amount:,.2f}, {overdue} days overdue.",
                    source_agent=self.name,
                    created_at=now,
                )
                session.add(alert)
            elif overdue > 30:
                alert = Alert(
                    severity="warning",
                    title=f"Overdue invoice: {record.invoice_number}",
                    message=f"{record.client_name} owes ${record.amount:,.2f}, {overdue} days overdue.",
                    source_agent=self.name,
                    created_at=now,
                )
                session.add(alert)

        await session.flush()
        return count
