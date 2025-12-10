@echo off
echo Starting Green Coding Advisor Backend Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if uvicorn is installed
python -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo ERROR: uvicorn is not installed. Installing...
    pip install uvicorn
)

REM Check if app can be imported
echo Checking imports...
python -c "from app.main import app" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to import app. Check the error above.
    pause
    exit /b 1
)

echo.
echo Starting server on http://127.0.0.1:8000
echo Press CTRL+C to stop the server
echo.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause

