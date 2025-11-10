from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import time

app = FastAPI(
    title="Green Coding Advisor API",
    description="AI-enhanced platform for sustainable coding",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Green Coding Advisor API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": time.time()
    }

# Simple auth endpoints
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    username: str
    password: str

@app.post("/auth/login")
async def login(request: LoginRequest):
    # Simple mock authentication
    if request.email == "jayvasani@gmail.com" and request.password == "Jay@2543":
        return {
            "access_token": "mock_token_12345",
            "refresh_token": "mock_refresh_12345",
            "token_type": "bearer"
        }
    return {"detail": "Incorrect email or password"}

@app.post("/auth/signup")
async def signup(request: SignupRequest):
    # Simple mock signup
    return {
        "message": "User created successfully",
        "user": {
            "email": request.email,
            "username": request.username
        }
    }

@app.get("/auth/me")
async def get_current_user():
    return {
        "id": 1,
        "email": "jayvasani@gmail.com",
        "username": "jayvasani",
        "role": "developer"
    }

# Simple submissions endpoint
class CodeSubmission(BaseModel):
    code: str
    language: str
    filename: str

@app.post("/submissions/analyze")
async def analyze_code(submission: CodeSubmission):
    # Mock analysis results
    return {
        "id": "mock_123",
        "greenScore": 78,
        "energyConsumption": 15.6,
        "co2Emissions": 0.024,
        "memoryUsage": 45.2,
        "cpuTime": 12.3,
        "suggestions": [
            "Consider using list comprehension instead of for loops",
            "Optimize data structure access patterns",
            "Reduce nested function calls"
        ],
        "language": submission.language,
        "filename": submission.filename
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
