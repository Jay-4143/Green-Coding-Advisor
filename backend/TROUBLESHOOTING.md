# Backend Server Troubleshooting Guide

## Common Issues and Solutions

### 1. Port 8000 Already in Use

**Error:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): only one usage of each socket address is normally permitted
```

**Solution:**
```powershell
# Find and kill the process using port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Or use a different port
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

### 2. ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'reportlab'
ModuleNotFoundError: No module named 'aiosqlite'
```

**Solution:**
```powershell
# Install missing dependencies
pip install -r requirements.txt

# Or install specific packages
pip install reportlab openpyxl aiosqlite
```

### 3. Database Errors

**Error:**
```
sqlalchemy.exc.OperationalError: unable to open database file
```

**Solution:**
```powershell
# Check if database file exists
Test-Path green.db

# If it doesn't exist, create it
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

### 4. Import Errors

**Error:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solution:**
1. Check if all files are in the correct locations
2. Verify Python path:
   ```powershell
   python -c "import sys; print(sys.path)"
   ```
3. Run the import check script:
   ```powershell
   python check_imports.py
   ```

### 5. Rate Limiter Warnings

**Warning:**
```
Rate limiter initialization failed: ...
```

**Solution:**
This is not critical - the server will continue without rate limiting. If you want to fix it:
- Check if `slowapi` is installed: `pip install slowapi`
- The app will work fine without rate limiting in development

### 6. Server Starts but Doesn't Respond

**Symptoms:**
- Server starts successfully
- But HTTP requests fail or timeout

**Solution:**
1. Check if the server is actually running:
   ```powershell
   netstat -an | findstr :8000
   ```
2. Try accessing the health endpoint:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
   ```
3. Check firewall settings
4. Verify the host is correct (127.0.0.1 or 0.0.0.0)

### 7. Database Locked Error

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
- Close any other applications using the database
- Restart the server
- Check if multiple server instances are running

### 8. CORS Errors in Browser

**Error:**
```
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Solution:**
- Check CORS settings in `app/config.py`
- Ensure `allowed_origins` includes `http://localhost:5173`
- Restart the server after changing config

## Diagnostic Commands

### Check if app can be imported
```powershell
python -c "from app.main import app; print('OK')"
```

### Check all imports
```powershell
python check_imports.py
```

### Check database
```powershell
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine); print('Database OK')"
```

### Check if port is available
```powershell
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
```

### View server logs
Run the server without `--reload` to see all logs:
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level debug
```

## Getting Help

If you're still experiencing issues:

1. **Check the error message** - Read it carefully for specific error details
2. **Run diagnostic scripts** - Use `check_imports.py` to verify all imports
3. **Check logs** - Look at the console output for warnings or errors
4. **Verify dependencies** - Ensure all packages in `requirements.txt` are installed
5. **Check Python version** - Ensure you're using Python 3.8 or higher:
   ```powershell
   python --version
   ```

## Quick Fix Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Port 8000 is available
- [ ] Database file exists or can be created
- [ ] No syntax errors in code
- [ ] All imports work (`python check_imports.py`)
- [ ] Server can be created (`python -c "from app.main import create_app; app = create_app()"`)

## Still Having Issues?

If none of the above solutions work:

1. **Create a fresh database:**
   ```powershell
   Remove-Item green.db -ErrorAction SilentlyContinue
   python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
   ```

2. **Reinstall dependencies:**
   ```powershell
   pip install --upgrade -r requirements.txt
   ```

3. **Check for Python path issues:**
   ```powershell
   cd backend
   $env:PYTHONPATH = "."
   python start_server.py
   ```

