import asyncio
import logging
from app.database import async_session
from app.agents.financial_data import FinancialDataAgent
from app.agents.tax_compliance import TaxComplianceAgent
from app.agents.accounts_receivable import AccountsReceivableAgent
from app.agents.accounts_payable import AccountsPayableAgent
from app.agents.audit import AuditAgent
from app.config import AGENT_POLL_INTERVAL

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self):
        self.agents = [
            FinancialDataAgent(),
            TaxComplianceAgent(),
            AccountsReceivableAgent(),
            AccountsPayableAgent(),
            AuditAgent(),
        ]
        self._task: asyncio.Task | None = None
        self._ws_subscribers: list = []

    def subscribe(self, queue: asyncio.Queue):
        self._ws_subscribers.append(queue)

    def unsubscribe(self, queue: asyncio.Queue):
        self._ws_subscribers.remove(queue)

    async def _broadcast(self, event: dict):
        for q in self._ws_subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                pass

    async def _run_loop(self):
        logger.info("Orchestrator started")
        while True:
            for agent in self.agents:
                try:
                    async with async_session() as session:
                        count = await agent.run_cycle(session)
                        await self._broadcast({
                            "type": "agent_update",
                            "agent": agent.name,
                            "state": agent.state,
                            "records": count,
                        })
                except Exception as e:
                    logger.error(f"Orchestrator error for {agent.name}: {e}")

            await self._broadcast({"type": "cycle_complete"})
            await asyncio.sleep(AGENT_POLL_INTERVAL)

    def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._run_loop())
            logger.info("Orchestrator task created")

    def stop(self):
        if self._task and not self._task.done():
            self._task.cancel()
            logger.info("Orchestrator stopped")

    def agent_statuses(self) -> list[dict]:
        return [a.status() for a in self.agents]


orchestrator = Orchestrator()
