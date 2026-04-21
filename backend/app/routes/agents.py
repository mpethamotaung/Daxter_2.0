from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import AgentLog, Alert
from app.schemas import AgentStatusOut, AgentLogOut, AlertOut
from app.orchestrator import orchestrator

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("/status", response_model=list[AgentStatusOut])
async def get_agent_statuses():
    return orchestrator.agent_statuses()


@router.get("/logs", response_model=list[AgentLogOut])
async def get_agent_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    stmt = select(AgentLog).order_by(AgentLog.timestamp.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/alerts", response_model=list[AlertOut])
async def get_alerts(limit: int = 50, db: AsyncSession = Depends(get_db)):
    stmt = select(Alert).order_by(Alert.created_at.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Alert).where(Alert.id == alert_id)
    result = await db.execute(stmt)
    alert = result.scalar_one_or_none()
    if not alert:
        return {"error": "Alert not found"}
    alert.acknowledged = True
    await db.commit()
    return {"status": "acknowledged"}
