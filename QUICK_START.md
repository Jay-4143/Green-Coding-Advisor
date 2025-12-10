# Quick Start Guide - Green Coding Advisor

## ✅ Fixed Issues

1. **Missing `aiosqlite` dependency** - ✅ FIXED and installed
2. **Backend startup errors** - ✅ All imports verified working
3. **Port conflicts** - Commands provided to resolve

## 🚀 Start the Application

### Step 1: Start Backend (Terminal 1)

```powershell
# Navigate to backend
cd backend

# Free port 8000 if needed
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Start server
python start_server.py
```

**Expected output:**
```
Starting Green Coding Advisor Backend Server...
============================================================
Server will be available at: http://127.0.0.1:8000
API Documentation: http://127.0.0.1:8000/docs
============================================================

INFO:     Started server process [...]
INFO:     Waiting for application startup.
Database tables created successfully
Default badges initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!**

### Step 2: Start Frontend (Terminal 2)

Open a **NEW** terminal window:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies if needed (first time only)
npm install

# Start frontend
npm run dev
```

**Expected output:**
```
  VITE v5.4.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

### Step 3: Access the Application

1. **Frontend:** Open http://localhost:5173 in your browser
2. **Backend API Docs:** Open http://127.0.0.1:8000/docs
3. **Health Check:** http://127.0.0.1:8000/health

## 🧪 Verify Everything Works

### Test Backend:
```powershell
# In a new terminal
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -Method GET
```

Should return: `{"status":"healthy","version":"1.0.0",...}`

### Test Frontend:
- Open http://localhost:5173
- You should see the login/signup page
- Try creating an account or logging in

## 🐛 Troubleshooting

### Backend won't start:

1. **Check if port is free:**
   ```powershell
   Get-NetTCPConnection -LocalPort 8000
   ```

2. **Test imports:**
   ```powershell
   cd backend
   python test_startup.py
   ```
   All checks should pass ✓

3. **Install missing dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### Frontend won't start:

1. **Install dependencies:**
   ```powershell
   cd frontend
   npm install
   ```

2. **Check for errors in terminal output**

3. **Clear cache and reinstall:**
   ```powershell
   Remove-Item -Recurse -Force node_modules
   npm install
   ```

### API Connection Issues:

1. **Verify backend is running:**
   - Check Terminal 1 shows "Uvicorn running"
   - Test http://127.0.0.1:8000/health

2. **Check CORS settings:**
   - Backend allows `http://localhost:5173` by default
   - See `backend/app/config.py` for CORS settings

3. **Check browser console:**
   - Open Developer Tools (F12)
   - Look for CORS or network errors

## 📝 Notes

- **Backend** must be running before frontend can make API calls
- Keep **both terminals open** while using the application
- Use `Ctrl+C` to stop servers
- Database file: `backend/green.db` (created automatically)

