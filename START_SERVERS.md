# How to Start Backend and Frontend

## Backend (Port 8000)
```powershell
cd backend
python start_server.py
```

The backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## Frontend (Port 5173)
```powershell
cd frontend
npm run dev
```

The frontend will be available at: http://localhost:5173

## Verify Backend is Running
Open a new terminal and run:
```powershell
python -c "import requests; r=requests.get('http://localhost:8000/health'); print('Backend Status:', r.status_code, r.json())"
```

If you see `Backend Status: 200`, the backend is running correctly.

## Troubleshooting

### If login/signup doesn't work:
1. **Hard refresh your browser**: Press `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
2. **Check browser console**: Press F12, go to Console tab, look for errors
3. **Check Network tab**: Press F12, go to Network tab, try login, see if requests are being made
4. **Verify both servers are running**: 
   - Backend: http://localhost:8000/health should return 200
   - Frontend: http://localhost:5173 should show the website

### Test Credentials
- Email: `teamuser@example.com`
- Password: `Test@1234`
