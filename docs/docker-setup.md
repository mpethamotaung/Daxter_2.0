# Docker Setup

Run the full stack (backend + frontend) in containers with Docker Compose. No local Python or Node.js installation required.

---

## Prerequisites

| Tool            | Minimum version | Check with               |
|-----------------|-----------------|--------------------------|
| Docker Engine   | 20+             | `docker --version`       |
| Docker Compose  | v2+             | `docker compose version` |

---

## Quick Start

From the repo root:

```bash
docker compose up --build
```

This builds both images and starts:

| Service   | URL                           |
|-----------|-------------------------------|
| Backend   | `http://localhost:8000`        |
| Frontend  | `http://localhost:5173`        |
| API Docs  | `http://localhost:8000/docs`   |

To stop:

```bash
docker compose down
```

---

## Custom Ports

If the default ports conflict with other services on your machine, override them with environment variables:

```bash
BACKEND_PORT=9000 FRONTEND_PORT=3000 docker compose up --build
```

This maps:
- Backend → `http://localhost:9000`
- Frontend → `http://localhost:3000`

You can also set these in a `.env` file in the repo root (git-ignored):

```env
BACKEND_PORT=9000
FRONTEND_PORT=3000
```

> **Note:** Inside the Docker network the frontend container proxies to the backend container by service name (`http://backend:8000`), so you only need to change the *host-side* port mapping. The internal wiring is handled automatically.

---

## How It Works

```
Host machine
  │
  ├── localhost:5173  ─► frontend container (Vite :5173)
  │                         │
  │                         └── /api/*, /ws proxy ──► backend container (uvicorn :8000)
  │
  └── localhost:8000  ─► backend container (uvicorn :8000)
                              │
                              └── SQLite database (persisted in Docker volume db-data)
```

The `docker-compose.yml` sets `VITE_BACKEND_URL=http://backend:8000` on the frontend container, which tells the Vite proxy to route API requests to the backend container. You don't need to set this yourself.

---

## Persistent Data

The backend's SQLite database is stored in a Docker volume called `db-data`. Data persists across `docker compose down` / `up` cycles.

To start fresh (delete all data):

```bash
docker compose down -v
```

---

## Rebuilding

If you change backend dependencies (`requirements.txt`) or frontend packages (`package.json`):

```bash
docker compose up --build
```

For code-only changes (no dependency changes), the existing images will pick up changes if you're using volume mounts, or you can rebuild with the command above.

---

## Running Individual Services

```bash
# Backend only
docker compose up backend

# Frontend only (requires backend to be running)
docker compose up frontend
```

---

## Logs

```bash
# Follow all logs
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend
```
