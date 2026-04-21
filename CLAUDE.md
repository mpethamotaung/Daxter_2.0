# Daxter 2.0

Full-stack accountant dashboard with agent-based data ingestion.

## Structure
- `backend/` — Python FastAPI server with 5 data agents and AI query engine
- `frontend/` — React/Vite dashboard with TailwindCSS and Recharts

## Running
- Backend: `cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Frontend: `cd frontend && npm run dev`
- Docker: `docker compose up --build`
- Custom backend port: pass `--port` to uvicorn, then set `VITE_BACKEND_URL=http://localhost:<port>` when running the frontend
- Environments are managed individually by contributors (venv or conda). Do not commit envs, node_modules, or .db files.
- Detailed setup: see `docs/` folder

## Key conventions
- Async-first backend (async SQLAlchemy, FastAPI)
- Agents are in `backend/app/agents/`, each extends `BaseAgent`
- Routes in `backend/app/routes/`, organized by domain
- Frontend components in `frontend/src/components/`
- WebSocket at `/ws` for real-time agent updates
