# Environment Setup

This project requires a Python environment for the backend and Node.js for the frontend. Choose whichever Python environment manager fits your workflow — both `venv` and `conda` instructions are provided below. If you prefer Docker instead, see [docker-setup.md](docker-setup.md).

---

## Prerequisites

| Tool       | Minimum version | Check with             |
|------------|-----------------|------------------------|
| Python     | 3.12+           | `python --version`     |
| Node.js    | 18+             | `node --version`       |
| npm        | 9+              | `npm --version`        |

---

## Python Environment

Pick **one** of the following options.

### Option A — venv (standard library)

```bash
# Create the environment (run from the repo root, not inside backend/)
python -m venv .venv

# Activate
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows (cmd)
.venv\Scripts\Activate.ps1      # Windows (PowerShell)

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### Option B — conda / miniconda

```bash
# Create a named environment
conda create -n daxter python=3.12 -y

# Activate
conda activate daxter

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

> **Note:** The environment directory (`.venv/`, `envs/`, etc.) is git-ignored. Each contributor creates and manages their own environment locally — never commit environment folders to the repo.

---

## Node.js / Frontend

```bash
cd frontend
npm install
```

This installs all frontend dependencies into `frontend/node_modules/`, which is also git-ignored.

---

## Verifying the Setup

After completing the steps above, confirm everything is installed:

```bash
# Backend — should print the FastAPI version
python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"

# Frontend — should list the project name
cd frontend && npm ls --depth=0
```

---

## Deactivating

```bash
# venv
deactivate

# conda
conda deactivate
```
