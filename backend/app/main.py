import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.orchestrator import orchestrator
from app.routes import dashboard, agents, queries, data, websocket
from app.config import LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Daxter 2.0 — initializing database")
    await init_db()
    logger.info("Starting agent orchestrator")
    orchestrator.start()
    yield
    logger.info("Shutting down orchestrator")
    orchestrator.stop()


app = FastAPI(
    title="Daxter 2.0",
    description="Accountant Data Aggregation and Insights Dashboard",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(agents.router)
app.include_router(queries.router)
app.include_router(data.router)
app.include_router(websocket.router)


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "agents": orchestrator.agent_statuses(),
    }
