# 🌱 Green Coding Advisor  
### AI-Enhanced Sustainable Code Optimization Platform

---

## 🚀 Overview

Green Coding Advisor is an AI-enhanced web platform designed to analyze source code sustainability, detect inefficient patterns, suggest optimized alternatives, calculate a Green Score (0–100), estimate carbon footprint impact, and gamify eco-friendly development practices.

The platform promotes sustainable software engineering by helping developers reduce computational waste, CPU usage, memory overhead, and inefficient algorithmic patterns.

---
## 🎯 Problem Statement

Modern software development often prioritizes functionality over efficiency, leading to:

- High CPU consumption
- Excessive memory usage
- Poor asynchronous handling
- Redundant iterations
- Increased energy consumption

Green Coding Advisor provides intelligent insights to help developers write optimized and environmentally responsible code.

---

## 🧠 Core Features

### 🔍 Static Code Analysis
- Detects inefficient patterns using:
  - Regex-based pattern detection
  - AST (Abstract Syntax Tree) parsing
- Multi-language support:
  - Python
  - JavaScript
  - Java
  - C++

---

### ⚡ Intelligent Code Optimization
- Deterministic “Detect & Replace” strategy
- Predefined verified transformation templates
- Avoids AI hallucination
- Guarantees syntactically correct optimized output

**Example Optimizations:**
- `for i in range(len(list))` → Direct iteration
- `await` inside loop → `Promise.all()` (parallel execution)
- `String +=` in loops → `StringBuilder`
- `innerHTML +=` → DOM-efficient approach

---

### 🌿 Green Score (0–100)

Dynamic sustainability metric calculated using:

**Penalties:**
- Severe inefficiencies
- Code complexity
- File size impact

**Bonuses:**
- Efficient built-in functions
- Functional programming constructs
- High-performance patterns
- Clean structure (functions/classes)

This provides immediate gamified feedback on code sustainability.

---

### 🌍 Carbon Footprint Estimation
- Estimates computational overhead
- Displays sustainability improvement after optimization
- Encourages eco-friendly coding habits

---

### 🎮 Gamification System
- Real-time score updates
- Optimization comparison view
- Improvement tracking

---

### 📊 Diff Visualization
- Side-by-side:
  - Original Code
  - Optimized Code
- Highlights replaced sections
- Displays Green Score improvement

---

## 🏗️ System Architecture

### Hybrid Optimization Engine

1. Pattern Recognition Layer (Regex + AST)
2. Deterministic Transformation Engine
3. Heuristic-Based Green Scoring System
4. AI-Assisted Sustainability Analysis

This ensures reliability, explainability, and syntactically correct optimizations.

---

## 🛠️ Technology Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Custom Regex Engine
- AST Parsing

### Frontend
- React
- Vite
- Tailwind CSS

### DevOps
- Docker
- Docker Compose

---
---

# 📸 Application Screenshots

## 🏠 Home Page
![screenshots/home.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/Home.png)

---

## 📞 Contact Us
![screenshots/contact.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/Contact%20Us.png)

---

## 🔐 Login Page
![Images/Screenshots/Login.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/Login.png)

---

## 👤 User Dashboard
![screenshots/user-dashboard.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/User%20dashboard.png)

---

## 📊 Dashboard Analytics
![screenshots/dashboard-2.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/dashboard%202.png)

---

## 📤 Code Submission Page
![screenshots/submission.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/Submission%20page.png)

---

## 🔎 Code Analysis Result
![screenshots/analysis.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/Analysis.png)

---

## 🏆 Leaderboard
![screenshots/leaderboard.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/Leaderboard.png)

---

## 🛠️ Admin Dashboard
![screenshots/admin-dashboard.png](https://github.com/Jay-4143/Green-Coding-Advisor/blob/3ac2279ea05cf9e33950b28bac89fc8d51de610f/Images/Screenshots/Admin%20dashboard.png)

---

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

