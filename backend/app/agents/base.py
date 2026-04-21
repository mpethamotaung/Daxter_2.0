import asyncio
import logging
import datetime
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AgentLog

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.state = "idle"
        self.records_processed = 0
        self.error_count = 0
        self.last_run: datetime.datetime | None = None
        self._running = False

    @abstractmethod
    async def collect_data(self, session: AsyncSession) -> int:
        """Collect and ingest data. Returns number of records processed."""
        ...

    async def run_cycle(self, session: AsyncSession):
        self.state = "running"
        self._running = True
        try:
            count = await self.collect_data(session)
            self.records_processed += count
            self.last_run = datetime.datetime.utcnow()
            self.state = "idle"
            log = AgentLog(
                agent_name=self.name,
                state="idle",
                message=f"Cycle complete. Ingested {count} records.",
                records_processed=count,
                timestamp=self.last_run,
            )
            session.add(log)
            await session.commit()
            logger.info(f"[{self.name}] Ingested {count} records")
            return count
        except Exception as e:
            self.state = "error"
            self.error_count += 1
            logger.error(f"[{self.name}] Error: {e}")
            log = AgentLog(
                agent_name=self.name,
                state="error",
                message=str(e),
                records_processed=0,
                timestamp=datetime.datetime.utcnow(),
            )
            session.add(log)
            await session.commit()
            return 0
        finally:
            self._running = False

    def status(self) -> dict:
        return {
            "name": self.name,
            "state": self.state,
            "last_run": self.last_run,
            "records_processed": self.records_processed,
            "error_count": self.error_count,
        }
