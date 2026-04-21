import random
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.base import BaseAgent
from app.models import FinancialRecord

REVENUE_CATEGORIES = [
    ("Tax Preparation Services", "Individual tax return filing"),
    ("Bookkeeping Services", "Monthly bookkeeping for client"),
    ("Audit Services", "Financial audit engagement"),
    ("Consulting", "Financial advisory consultation"),
    ("Payroll Services", "Payroll processing for client"),
]

EXPENSE_CATEGORIES = [
    ("Software Licenses", "Accounting software subscription"),
    ("Office Rent", "Monthly office lease payment"),
    ("Staff Salaries", "Employee compensation"),
    ("Professional Development", "CPA continuing education"),
    ("Marketing", "Digital advertising campaign"),
    ("Insurance", "Professional liability insurance"),
    ("Utilities", "Office utilities and internet"),
]

CLIENTS = [
    "Meridian Corp", "Atlas Manufacturing", "Pinnacle Retail", "Vertex Solutions",
    "Horizon Healthcare", "Summit Logistics", "Cascade Financial", "Ironwood Construction",
    "Sterling Enterprises", "BlueWave Technologies",
]


class FinancialDataAgent(BaseAgent):
    def __init__(self):
        super().__init__("Financial Data Agent")

    async def collect_data(self, session: AsyncSession) -> int:
        now = datetime.datetime.utcnow()
        records = []

        for _ in range(random.randint(3, 8)):
            if random.random() < 0.6:
                cat, desc = random.choice(REVENUE_CATEGORIES)
                amount = round(random.uniform(1500, 25000), 2)
                tx_type = "revenue"
            else:
                cat, desc = random.choice(EXPENSE_CATEGORIES)
                amount = round(random.uniform(200, 8000), 2)
                tx_type = "expense"

            record = FinancialRecord(
                date=now - datetime.timedelta(days=random.randint(0, 30)),
                category=cat,
                description=desc,
                amount=amount,
                transaction_type=tx_type,
                source_agent=self.name,
                client_name=random.choice(CLIENTS) if tx_type == "revenue" else None,
            )
            records.append(record)

        session.add_all(records)
        await session.flush()
        return len(records)
