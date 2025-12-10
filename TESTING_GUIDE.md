# Green Coding Advisor - Testing Guide

## Project Status

✅ **Frontend**: Ready to run on http://localhost:5173
✅ **Backend Dependencies**: Installed (including reportlab, openpyxl, aiosqlite)
✅ **Database**: SQLite database exists and tables are created
✅ **All Components**: Code is complete and ready for testing

## ⚠️ IMPORTANT: Fixed Issues

1. **Missing aiosqlite dependency** - ✅ FIXED: Added to requirements.txt and installed
2. **Port conflicts** - Use the provided commands to kill processes on port 8000
3. **Server startup** - Use the startup scripts provided for reliable server launch

## Starting the Servers

### Backend Server

**Option 1: Using the startup script (Recommended)**
1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **First, ensure port 8000 is free:**
   ```powershell
   Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
   ```

3. **Run the startup script:**
   ```powershell
   python start_server.py
   ```
   Or on Windows, you can double-click `backend/start_backend.bat`
   
   **Note:** Keep this terminal window open. The server runs in the foreground.

**Option 2: Using uvicorn directly**
1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Start the server:**
   ```powershell
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

**Expected output:**
   - Database tables created
   - Default badges initialized
   - Server running on http://127.0.0.1:8000

**If you get a port conflict error:**
   - Port 8000 is already in use
   - Kill the process using port 8000:
     ```powershell
     Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
     ```
   - Or use a different port:
     ```powershell
     python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
     ```

3. **Test the backend:**
   - Open browser: http://localhost:8000/docs (API documentation)
   - Health check: http://localhost:8000/health
   - Root endpoint: http://localhost:8000/

### Frontend Server

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Start the development server:**
   ```powershell
   npm run dev
   ```

   The server should start on http://localhost:5173

3. **Access the application:**
   - Open browser: http://localhost:5173
   - The application should load with the login page

## Testing the Application

### 1. User Registration & Authentication

- **Sign Up**: Create a new account
- **Login**: Log in with your credentials
- **Email Verification**: Check email for verification link (if email is configured)
- **Password Reset**: Test forgot password functionality

### 2. Code Analysis

- **Submit Code**: Paste or upload code in Python, JavaScript, Java, or C++
- **View Results**: Check Green Score, energy consumption, CO2 emissions
- **Optimization Suggestions**: Review AI-generated suggestions
- **Code Comparison**: View before/after code comparisons

### 3. Dashboard Features

- **Metrics Overview**: View total submissions, average green score, carbon savings
- **Charts**: Check Green Score history, language efficiency, carbon timeline
- **Badges**: View earned badges and achievements
- **Streaks**: Check daily submission streaks
- **Download Reports**: Download CSV reports of metrics

### 4. Additional Features

- **Badges**: View all available badges and earned badges
- **Teams**: Create teams, invite members, view team metrics
- **Chatbot**: Ask questions about green coding practices
- **Leaderboard**: View top users by green score
- **Settings**: Manage user profile and preferences

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `POST /auth/verify-email` - Verify email
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password

### Code Submissions
- `POST /submissions/analyze` - Analyze code
- `GET /submissions/` - Get user submissions
- `GET /submissions/{id}` - Get submission details

### Metrics
- `GET /metrics/summary` - Get user metrics summary
- `GET /metrics/history` - Get submission history
- `GET /metrics/leaderboard` - Get leaderboard
- `GET /metrics/language-stats` - Get language statistics
- `GET /metrics/carbon-timeline` - Get carbon emissions timeline

### Badges
- `GET /badges/me` - Get user's badges
- `GET /badges/all` - Get all available badges

### Teams
- `POST /teams` - Create team
- `GET /teams/{id}` - Get team details
- `POST /teams/{id}/join` - Join team
- `GET /teams/{id}/metrics` - Get team metrics

### Reports
- `GET /reports/metrics/csv` - Download metrics CSV
- `GET /reports/submissions/csv` - Download submissions CSV
- `GET /reports/submission/{id}/pdf` - Download submission PDF

### Chatbot
- `POST /chat/answer` - Ask chatbot a question
- `GET /chat/suggestions` - Get suggested questions

### Streaks
- `GET /streaks/me` - Get user's streak information

## Troubleshooting

### Backend won't start

1. **Check dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Check for port conflicts:**
   ```powershell
   netstat -an | findstr :8000
   ```

3. **Check database:**
   ```powershell
   python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
   ```

### Frontend won't start

1. **Install dependencies:**
   ```powershell
   cd frontend
   npm install
   ```

2. **Check for port conflicts:**
   ```powershell
   netstat -an | findstr :5173
   ```

### Database issues

1. **Reset database:**
   ```powershell
   Remove-Item green.db
   python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
   ```

## Expected Behavior

### Successful Backend Start
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
Database tables created successfully
Default badges initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Successful Frontend Start
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Next Steps

1. Start both servers (backend and frontend)
2. Open http://localhost:5173 in your browser
3. Create an account and start testing features
4. Submit code samples for analysis
5. Explore all features: badges, teams, chatbot, reports

## Notes

- Email functionality requires SMTP configuration in `.env` file
- CodeCarbon integration works in offline mode by default
- All features are functional and ready for testing
- The application uses SQLite for development (can be switched to PostgreSQL for production)

