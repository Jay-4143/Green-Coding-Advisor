# Green Coding Advisor - AI‑Enhanced Web Platform

## Overview
Web-based, AI-enhanced platform to analyze code sustainability, provide optimization suggestions, track carbon footprint, and gamify progress.

## Backend (FastAPI)

### Setup
1) Create venv
```
python -m venv .venv
.venv\\Scripts\\activate
```
2) Install deps
```
pip install -r backend/requirements.txt
```
3) Run API
```
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
4) Test
```
GET http://localhost:8000/health
```

Next: integrate DB, queue, and analysis pipeline.

## Frontend (React + Vite + Tailwind)

### Setup
```
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

