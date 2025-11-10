from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI(title="Green Coding Advisor API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Green Coding Advisor API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/login")
async def login(request: LoginRequest):
    if request.email == "jayvasani@gmail.com" and request.password == "Jay@2543":
        return {
            "access_token": "mock_token_12345",
            "refresh_token": "mock_refresh_12345",
            "token_type": "bearer"
        }
    return {"detail": "Incorrect email or password"}

class SignupRequest(BaseModel):
    email: str
    username: str
    password: str

@app.post("/auth/signup")
async def signup(request: SignupRequest):
    return {
        "message": "User created successfully",
        "user": {"email": request.email, "username": request.username}
    }

@app.get("/auth/me")
async def get_current_user():
    return {
        "id": 1,
        "email": "jayvasani@gmail.com",
        "username": "jayvasani",
        "role": "developer"
    }

class CodeSubmission(BaseModel):
    code: str
    language: str

@app.post("/submissions/")
async def analyze_code(submission: CodeSubmission):
    return {
        "id": "mock_123",
        "greenScore": 78,
        "energyConsumption": 15.6,
        "co2Emissions": 0.024,
        "memoryUsage": 45.2,
        "cpuTime": 12.3,
        "suggestions": [
            "Consider using list comprehension instead of for loops",
            "Optimize data structure access patterns"
        ],
        "language": submission.language
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
