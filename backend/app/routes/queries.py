import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import QueryHistory
from app.schemas import QueryRequest, QueryResponse
from app.ai_engine import answer_query

router = APIRouter(prefix="/api/query", tags=["query"])


@router.post("/", response_model=QueryResponse)
async def ask_question(req: QueryRequest, db: AsyncSession = Depends(get_db)):
    answer = await answer_query(req.question, db)
    now = datetime.datetime.utcnow()
    entry = QueryHistory(question=req.question, answer=answer, timestamp=now)
    db.add(entry)
    await db.commit()
    return QueryResponse(question=req.question, answer=answer, timestamp=now)


@router.get("/history", response_model=list[QueryResponse])
async def get_query_history(limit: int = 20, db: AsyncSession = Depends(get_db)):
    stmt = select(QueryHistory).order_by(QueryHistory.timestamp.desc()).limit(limit)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [
        QueryResponse(question=r.question, answer=r.answer, timestamp=r.timestamp)
        for r in rows
    ]
