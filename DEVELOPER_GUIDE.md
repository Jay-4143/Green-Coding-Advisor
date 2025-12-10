# Green Coding Advisor - Developer Guide

This guide is for developers who want to contribute to or integrate with the Green Coding Advisor platform.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Backend Development](#backend-development)
5. [Frontend Development](#frontend-development)
6. [Database Schema](#database-schema)
7. [API Integration](#api-integration)
8. [Testing](#testing)
9. [Contributing](#contributing)

## Architecture Overview

### Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- MongoDB Atlas (NoSQL database)
- Motor (async MongoDB driver)
- Pydantic (data validation)
- JWT (authentication)

**Frontend:**
- React 18
- TypeScript
- Vite (build tool)
- Tailwind CSS
- Axios (HTTP client)

**Infrastructure:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- MongoDB Atlas (cloud database)

### System Architecture

```
┌─────────────┐
│   Frontend  │ (React + Vite)
│  (Port 5173)│
└──────┬──────┘
       │ HTTP/REST
       │
┌──────▼──────┐
│   Backend   │ (FastAPI)
│  (Port 8000)│
└──────┬──────┘
       │
┌──────▼──────┐
│  MongoDB    │ (Atlas)
│  Database   │
└─────────────┘
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Git

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/green-coding-advisor.git
   cd green-coding-advisor
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp env.example .env
   # Edit .env with your MongoDB URI
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **Run Development Servers:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python -m uvicorn app.main:app --reload

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

## Project Structure

```
green-coding-advisor/
├── backend/
│   ├── app/
│   │   ├── routers/        # API route handlers
│   │   ├── schemas.py      # Pydantic models
│   │   ├── auth.py         # Authentication logic
│   │   ├── mongo.py        # Database connection
│   │   ├── security.py     # Security utilities
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api/            # API client
│   │   └── App.tsx         # Main app component
│   ├── tests/              # Frontend tests
│   ├── package.json
│   └── Dockerfile
└── .github/
    └── workflows/          # CI/CD pipelines
```

## Backend Development

### Adding a New Endpoint

1. **Create router function:**
   ```python
   # app/routers/example.py
   from fastapi import APIRouter, Depends
   from ..auth import get_current_active_user
   from ..rate_limiter import limiter
   from fastapi import Request

   router = APIRouter()

   @router.get("/example")
   @limiter.limit("60/minute")
   async def example_endpoint(
       request: Request,
       current_user=Depends(get_current_active_user)
   ):
       return {"message": "Hello"}
   ```

2. **Register router in main.py:**
   ```python
   from .routers import example
   app.include_router(example.router, prefix="/example", tags=["Example"])
   ```

### Database Operations

```python
from ..mongo import get_mongo_db

async def example_function(db=Depends(get_mongo_db)):
    # Insert
    await db["collection"].insert_one({"key": "value"})
    
    # Find
    doc = await db["collection"].find_one({"key": "value"})
    
    # Update
    await db["collection"].update_one(
        {"key": "value"},
        {"$set": {"new_key": "new_value"}}
    )
    
    # Delete
    await db["collection"].delete_one({"key": "value"})
```

### Input Validation

```python
from ..security import sanitize_string, validate_email

# In your endpoint
email = sanitize_string(user_input.email.lower().strip())
if not validate_email(email):
    raise HTTPException(status_code=400, detail="Invalid email")
```

### Rate Limiting

```python
from ..rate_limiter import limiter
from fastapi import Request

@router.post("/endpoint")
@limiter.limit("10/minute")  # Stricter for sensitive endpoints
async def endpoint(request: Request, ...):
    ...
```

## Frontend Development

### Adding a New Component

```typescript
// src/components/Example.tsx
import React from 'react';

interface ExampleProps {
  title: string;
}

const Example: React.FC<ExampleProps> = ({ title }) => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">{title}</h1>
    </div>
  );
};

export default Example;
```

### API Calls

```typescript
import { apiClient } from '../api/client';

// GET request
const response = await apiClient.get('/endpoint');
const data = response.data;

// POST request
const response = await apiClient.post('/endpoint', {
  key: 'value'
});

// With authentication (automatic via interceptor)
const response = await apiClient.get('/protected-endpoint');
```

### State Management

Currently using React hooks. For complex state, consider:
- Context API for global state
- React Query for server state
- Zustand for simple global state

## Database Schema

### Collections

**users:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "hashed_password": "...",
  "role": "developer",
  "is_active": true,
  "is_verified": true,
  "current_streak": 5,
  "longest_streak": 10,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**submissions:**
```json
{
  "id": 1,
  "user_id": 1,
  "code_content": "...",
  "language": "python",
  "green_score": 85.5,
  "energy_consumption_wh": 0.05,
  "co2_emissions_g": 12.5,
  "status": "completed",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**badges:**
```json
{
  "id": 1,
  "name": "First Steps",
  "description": "Submit your first code analysis",
  "icon": "🌱",
  "criteria": {...}
}
```

**user_badges:**
```json
{
  "user_id": 1,
  "badge_id": 1,
  "earned_at": "2024-01-01T00:00:00Z"
}
```

## API Integration

### Authentication Flow

1. **Sign Up:**
   ```bash
   POST /auth/signup
   {
     "email": "user@example.com",
     "username": "user",
     "password": "Password123!"
   }
   ```

2. **Login:**
   ```bash
   POST /auth/login
   {
     "email": "user@example.com",
     "password": "Password123!"
   }
   # Returns: { "access_token": "...", "refresh_token": "..." }
   ```

3. **Use Token:**
   ```bash
   GET /auth/me
   Authorization: Bearer <access_token>
   ```

### Example: Submit Code

```python
import requests

# Login
response = requests.post("http://localhost:8000/auth/login", json={
    "email": "user@example.com",
    "password": "password"
})
token = response.json()["access_token"]

# Submit code
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8000/submissions",
    json={
        "code_content": "def hello(): print('world')",
        "language": "python",
        "filename": "hello.py"
    },
    headers=headers
)
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:e2e  # E2E tests with Playwright
```

### Running All Tests

```bash
# From project root
pytest backend/tests/
cd frontend && npm test
```

## Contributing

### Development Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and test
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/my-feature`
5. Create Pull Request

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Maximum line length: 120
- Run `pylint` before committing

**TypeScript:**
- Use ESLint rules
- Prefer functional components
- Use TypeScript strict mode
- Follow React best practices

### Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `chore:` Maintenance

Example: `feat: Add pagination to leaderboard`

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Request review from maintainers
4. Address review comments
5. Merge after approval

## Environment Variables

See `backend/env.example` and `backend/PRODUCTION_ENV_SETUP.md` for details.

## Troubleshooting

### Common Issues

**Import Errors:**
- Ensure you're in the correct directory
- Check Python path: `python -c "import sys; print(sys.path)"`

**Database Connection:**
- Verify MongoDB URI in `.env`
- Check network access in MongoDB Atlas
- Test connection: `python -c "from app.mongo import get_mongo_client; print(get_mongo_client())"`

**Port Conflicts:**
- Backend: Change port in `uvicorn` command
- Frontend: Change port in `vite.config.ts`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [API Documentation](./API_DOCUMENTATION.md)

---

Happy Coding! 🚀

