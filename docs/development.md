# Development Guide

How to run the backend and frontend locally, how they connect to each other, and how to change the default ports.

---

## Default Ports

| Service   | Default host | Default port | Config location                     |
|-----------|-------------|--------------|-------------------------------------|
| Backend   | `127.0.0.1` | `8000`       | uvicorn CLI args                    |
| Frontend  | `localhost`  | `5173`       | `frontend/vite.config.js` / env vars |

The frontend dev server proxies all `/api/*` and `/ws` requests to the backend. This proxy is configured in `frontend/vite.config.js` and defaults to `http://localhost:8000`. When both services use their defaults, they connect automatically with no extra configuration.

---

## Running the Backend

Open a terminal, activate your Python environment (see [environment-setup.md](environment-setup.md)), then:

```bash
cd backend
uvicorn app.main:app --reload
```

This starts the API at `http://127.0.0.1:8000`.

### Custom host and port

Pass `--host` and `--port` to uvicorn to override the defaults:

```bash
# Bind to all interfaces on port 9000
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000
```

> **If you change the backend port**, you must also tell the frontend where to find it (see below).

### Backend environment variables

| Variable              | Default                                | Description                        |
|-----------------------|----------------------------------------|------------------------------------|
| `DATABASE_URL`        | `sqlite+aiosqlite:///./daxter.db`      | SQLAlchemy async database URL      |
| `AGENT_POLL_INTERVAL` | `10`                                   | Seconds between agent run cycles   |
| `LOG_LEVEL`           | `INFO`                                 | Python logging level               |

---

## Running the Frontend

Open a **second** terminal:

```bash
cd frontend
npm run dev
```

This starts the Vite dev server at `http://localhost:5173`.

### Custom host and port

Use environment variables:

```bash
VITE_PORT=3000 VITE_HOST=0.0.0.0 npm run dev
```

Or on Windows (cmd):

```cmd
set VITE_PORT=3000 && set VITE_HOST=0.0.0.0 && npm run dev
```

### Pointing the frontend to a different backend port

If you started the backend on a non-default port, set `VITE_BACKEND_URL` when starting the frontend:

```bash
# Backend is running on port 9000
VITE_BACKEND_URL=http://localhost:9000 npm run dev
```

This tells the Vite proxy where to forward `/api/*` and `/ws` requests.

---

## How the Frontend Connects to the Backend

```
Browser (localhost:5173)
  │
  ├── GET /api/dashboard/summary ──► Vite dev server proxy ──► Backend (localhost:8000)
  ├── GET /api/agents/status     ──► Vite dev server proxy ──► Backend (localhost:8000)
  ├── POST /api/query/           ──► Vite dev server proxy ──► Backend (localhost:8000)
  └── WS  /ws                    ──► Vite dev server proxy ──► Backend (localhost:8000)
```

The frontend never calls the backend port directly. All requests go to the Vite dev server on the frontend port, which proxies them to the backend. This is configured in `frontend/vite.config.js`:

```js
const BACKEND_URL = process.env.VITE_BACKEND_URL || 'http://localhost:8000'

proxy: {
  '/api': BACKEND_URL,
  '/ws':  { target: WS_BACKEND_URL, ws: true },
}
```

**If the proxy is misconfigured** (wrong port, backend not running), the frontend will load but all data panels will show loading spinners and the connection indicator in the sidebar will read "Reconnecting...".

---

## Quick Reference — Common Scenarios

### Both on defaults (most common)

```bash
# Terminal 1
cd backend && uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm run dev
```

Open `http://localhost:5173`.

### Backend on custom port

```bash
# Terminal 1
cd backend && uvicorn app.main:app --reload --port 9000

# Terminal 2 — tell the frontend where the backend is
cd frontend && VITE_BACKEND_URL=http://localhost:9000 npm run dev
```

### Multiple instances side by side

If you're running another app on 8000/5173 already:

```bash
# Terminal 1
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8500

# Terminal 2
cd frontend && VITE_BACKEND_URL=http://localhost:8500 VITE_PORT=5200 npm run dev
```

Open `http://localhost:5200`.

---

## API Docs

Once the backend is running, interactive Swagger docs are available at:

```
http://localhost:8000/docs
```

The health check endpoint is a fast way to verify the backend is up:

```bash
curl http://localhost:8000/api/health
```
