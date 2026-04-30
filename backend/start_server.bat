@echo off
echo Starting Green Coding Advisor Backend Server...
echo.

REM Check if Python is available
if exist "venv\Scripts\python.exe" (
    set PYTHON_EXE=venv\Scripts\python.exe
) else (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python is not installed or not in PATH and venv was not found.
        pause
        exit /b 1
    )
    set PYTHON_EXE=python
)

REM Check if uvicorn is installed
%PYTHON_EXE% -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo ERROR: uvicorn is not installed in the chosen environment. Installing...
    %PYTHON_EXE% -m pip install uvicorn
)

REM Check if app can be imported
echo Checking imports...
%PYTHON_EXE% -c "from app.main import app" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to import app. Check the error above.
    pause
    exit /b 1
)

echo.
echo Starting server on http://127.0.0.1:8000
echo Press CTRL+C to stop the server
echo.

%PYTHON_EXE% -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause

