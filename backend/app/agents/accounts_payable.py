import random
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.base import BaseAgent
from app.models import AccountsPayable

VENDORS = [
    ("Intuit", "Software Licenses"),
    ("WeWork", "Office Space"),
    ("AWS", "Cloud Services"),
    ("Google Workspace", "Software Licenses"),
    ("Office Depot", "Office Supplies"),
    ("ADP", "Payroll Services"),
    ("Travelers Insurance", "Insurance"),
    ("Verizon", "Telecommunications"),
    ("Thomson Reuters", "Research & Data"),
    ("Staples", "Office Supplies"),
]


class AccountsPayableAgent(BaseAgent):
    def __init__(self):
        super().__init__("Accounts Payable Agent")
        self._bill_counter = 5000

    async def collect_data(self, session: AsyncSession) -> int:
        now = datetime.datetime.utcnow()
        count = 0

        for _ in range(random.randint(2, 5)):
            self._bill_counter += 1
            vendor, category = random.choice(VENDORS)
            days_ago = random.randint(1, 45)
            received = now - datetime.timedelta(days=days_ago)
            due = received + datetime.timedelta(days=random.choice([15, 30, 45, 60]))
            paid = random.random() < 0.5

            record = AccountsPayable(
                vendor_name=vendor,
                bill_number=f"BILL-{self._bill_counter}",
                amount=round(random.uniform(100, 15000), 2),
                received_date=received,
                due_date=due,
                paid=paid,
                category=category,
            )
            session.add(record)
            count += 1

        await session.flush()
        return count
