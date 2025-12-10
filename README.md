# Green Coding Advisor - AI‑Enhanced Web Platform

## Overview
Web-based, AI-enhanced platform to analyze code sustainability, provide optimization suggestions, track carbon footprint, and gamify progress.

## Backend (FastAPI)

### Quick Start

**Option 1: Using the startup script (Recommended)**
```powershell
cd backend
python start_server.py
```

**Option 2: Using the batch file (Windows)**
```powershell
cd backend
.\start_backend.bat
```

**Option 3: Using uvicorn directly**
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Setup (First Time Only)

1. **Install dependencies:**
```powershell
cd backend
pip install -r requirements.txt
```

2. **Verify installation:**
```powershell
python test_startup.py
```

### Verify Backend is Running

Once started, you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Test the health endpoint:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health"
```

Or open in browser: http://127.0.0.1:8000/docs (API documentation)

### Troubleshooting

**Port 8000 already in use?**
```powershell
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

## Frontend (React + Vite + Tailwind)

### Setup
```
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## Dockerized Setup

### Requirements
- Docker Desktop (or Docker Engine + Docker Compose v2)
- Copy `backend/env.example` to `backend/.env` and update secrets before building

### Build images
```powershell
docker compose build
```

### Run the full stack
```powershell
docker compose up
```

Services:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:5173

To stop containers:
```powershell
docker compose down
```

