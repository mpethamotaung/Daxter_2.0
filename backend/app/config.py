import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./daxter.db")
AGENT_POLL_INTERVAL = int(os.getenv("AGENT_POLL_INTERVAL", "10"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
