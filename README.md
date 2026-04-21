# Daxter 2.0

## Accountant Data Aggregation and Insights Dashboard

A unified dashboard for accountants that consolidates real-time financial and tax compliance data from multiple agent-based sources. The platform integrates intelligent AI workflows, agent orchestration, and real-time data processing.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  KPI Cards │ Charts │ Tax Tracker │ AI Chat │ Alerts    │
│                    ↕ WebSocket + REST                    │
├─────────────────────────────────────────────────────────┤
│                   FastAPI Backend                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Agent Orchestrator                   │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │    │
│  │  │Financial │ │   Tax    │ │    Accounts      │ │    │
│  │  │  Data    │ │Compliance│ │ Receivable / AP  │ │    │
│  │  └──────────┘ └──────────┘ └──────────────────┘ │    │
│  │  ┌──────────┐                                    │    │
│  │  │  Audit   │    AI Query Engine                 │    │
│  │  └──────────┘                                    │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                  SQLite Database                          │
│  financial_records │ tax_compliance │ accounts_*          │
│  agent_logs │ alerts │ query_history                      │
└─────────────────────────────────────────────────────────┘
```

## Features

### Agent System (5 Autonomous Agents)
- **Financial Data Agent** — Ingests revenue and expense transactions across categories
- **Tax Compliance Agent** — Tracks filing deadlines, compliance status, generates alerts
- **Accounts Receivable Agent** — Monitors invoices, aging, overdue payments
- **Accounts Payable Agent** — Tracks vendor bills and payment schedules
- **Audit Agent** — Detects anomalies (large transactions, duplicates, ratio checks)

### Dashboard
- **KPI Cards** — Revenue, expenses, net income, AR/AP, tax deadlines, compliance warnings
- **Revenue Trend Chart** — 30-day revenue with area visualization
- **Expense Breakdown** — Horizontal bar chart by category
- **Tax Compliance Tracker** — Filing status, deadlines, jurisdiction tracking
- **Agent Orchestration Monitor** — Real-time agent state, activity logs
- **Alerts Panel** — Severity-based alerts with acknowledge workflow

### AI Assistant
- Natural language queries about financial data
- Keyword-matched routing to specialized handlers
- Full financial summary on demand
- Query history persistence

### Real-Time Updates
- WebSocket connection for live agent status broadcasts
- Auto-reconnect on disconnect
- Dashboard auto-refreshes on each agent cycle

### Observability
- Structured logging with configurable levels
- Health check endpoint (`/api/health`)
- Agent activity logs with error tracking
- Per-agent metrics (records processed, error count, last run)

## Tech Stack

| Layer     | Technology                              |
|-----------|----------------------------------------|
| Frontend  | React 18, Vite, TailwindCSS, Recharts |
| Backend   | Python 3.12, FastAPI, SQLAlchemy 2.0   |
| Database  | SQLite (async via aiosqlite)           |
| Real-time | WebSocket                              |
| Icons     | Lucide React                           |

## Quick Start

### Prerequisites
- Python 3.12+ (via [venv](https://docs.python.org/3/library/venv.html) or [conda/miniconda](https://docs.conda.io/en/latest/miniconda.html))
- Node.js 18+

### Backend

Set up a Python environment using **either** venv or conda:

```bash
# Option A — venv
python -m venv .venv && source .venv/bin/activate

# Option B — conda
conda create -n daxter python=3.12 -y && conda activate daxter
```

Then install and run:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and proxies API requests to the backend at `http://localhost:8000`.

### Docker

```bash
docker compose up --build
```

## Documentation

Detailed guides for setup, port configuration, and troubleshooting are in the [`docs/`](docs/) folder:

| Document | Covers |
|----------|--------|
| [Environment Setup](docs/environment-setup.md) | Python (venv & conda) and Node.js installation |
| [Development Guide](docs/development.md) | Running locally, custom hosts/ports, how the frontend proxy connects to the backend |
| [Docker Setup](docs/docker-setup.md) | Docker Compose, custom port mapping, volumes, logs |

## API Endpoints

| Method | Path                              | Description                  |
|--------|-----------------------------------|------------------------------|
| GET    | `/api/health`                     | Health check + agent status  |
| GET    | `/api/dashboard/summary`          | Aggregated KPI summary       |
| GET    | `/api/agents/status`              | All agent states             |
| GET    | `/api/agents/logs`                | Agent activity logs          |
| GET    | `/api/agents/alerts`              | All alerts                   |
| POST   | `/api/agents/alerts/{id}/acknowledge` | Acknowledge an alert    |
| POST   | `/api/query/`                     | Ask AI assistant             |
| GET    | `/api/query/history`              | Past queries                 |
| GET    | `/api/data/financial`             | Financial records            |
| GET    | `/api/data/tax-compliance`        | Tax compliance filings       |
| GET    | `/api/data/receivables`           | Accounts receivable          |
| GET    | `/api/data/payables`              | Accounts payable             |
| WS     | `/ws`                             | Real-time event stream       |
