# Green Coding Advisor API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Getting Tokens

1. **Sign Up** - Create a new account
2. **Login** - Get access and refresh tokens
3. **Refresh Token** - Get a new access token using refresh token

## Endpoints

### Authentication

#### POST /auth/signup
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "Password123!",
  "role": "developer"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "role": "developer",
  "is_verified": false
}
```

#### POST /auth/login
Authenticate user and get tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### POST /auth/verify-email
Verify user email with token.

**Request Body (Form Data):**
```
token: <verification_token>
```

#### POST /auth/forgot-password
Request password reset.

**Request Body (Form Data):**
```
email: user@example.com
```

#### POST /auth/reset-password
Reset password with token.

**Request Body (Form Data):**
```
token: <reset_token>
new_password: NewPassword123!
```

### Code Analysis

#### POST /submissions/analyze
Analyze code without saving (public endpoint).

**Request Body:**
```json
{
  "code": "def hello():\n    print('Hello')",
  "language": "python",
  "region": "usa"
}
```

**Response:**
```json
{
  "green_score": 85.5,
  "energy_consumption_wh": 0.05,
  "co2_emissions_g": 12.5,
  "cpu_time_ms": 2.5,
  "memory_usage_mb": 10.2,
  "complexity_score": 5.0,
  "suggestions": [
    {
      "finding": "Optimization opportunity",
      "before_code": "...",
      "after_code": "...",
      "explanation": "...",
      "predicted_improvement": {
        "green_score": 10,
        "energy_wh": -0.01
      },
      "severity": "medium"
    }
  ],
  "analysis_details": {...},
  "real_world_impact": {
    "light_bulb_hours": 0.83,
    "tree_planting_days": 0.57,
    "car_miles": 0.031,
    "description": "Running this code 1M times = powering a light bulb for 0.8 hours"
  }
}
```

#### POST /submissions
Submit code for analysis (requires authentication).

**Request Body:**
```json
{
  "code_content": "def hello():\n    print('Hello')",
  "language": "python",
  "filename": "hello.py",
  "project_id": 1
}
```

### Metrics

#### GET /metrics/summary
Get aggregate metrics.

**Query Parameters:**
- `user_id` (optional): Filter by user ID

**Response:**
```json
{
  "average_green_score": 82.5,
  "total_submissions": 50,
  "total_co2_saved": 125.5,
  "total_energy_saved": 2.5,
  "badges_earned": 5,
  "current_streak": 7
}
```

#### GET /metrics/history
Get submission history.

**Query Parameters:**
- `user_id` (optional): Filter by user ID
- `limit` (optional): Number of results (default: 50)

#### GET /metrics/language-stats
Get statistics per programming language.

**Query Parameters:**
- `user_id` (optional): Filter by user ID

#### GET /metrics/carbon-timeline
Get carbon emissions timeline.

**Query Parameters:**
- `user_id` (optional): Filter by user ID
- `days` (optional): Number of days (default: 30)

#### GET /metrics/leaderboard
Get leaderboard.

**Query Parameters:**
- `timeframe`: "week", "month", or "all" (default: "month")
- `limit`: Number of entries (default: 10)

### Badges

#### GET /badges/me
Get current user's badges.

#### GET /badges/all
Get all available badges.

#### POST /badges/check/{user_id}
Manually check and award badges.

### Teams

#### POST /teams
Create a new team.

#### GET /teams
Get all teams for current user.

#### GET /teams/{team_id}
Get team details.

#### GET /teams/{team_id}/dashboard
Get team dashboard with metrics.

#### GET /teams/{team_id}/leaderboard
Get team leaderboard.

#### POST /teams/{team_id}/members
Add member to team.

#### GET /teams/{team_id}/members
Get team members.

### Projects

#### POST /projects
Create a new project.

#### GET /projects
Get user's projects.

#### GET /projects/{project_id}
Get project details.

#### GET /projects/{project_id}/summary
Get project summary with metrics.

### Reports

#### GET /reports/submission/{submission_id}/pdf
Download PDF report for a submission.

#### GET /reports/submissions/csv
Download CSV report for submissions.

#### GET /reports/metrics/csv
Download CSV report for metrics.

### Streaks

#### GET /streaks/me
Get current user's streak information.

#### GET /streaks/me/calendar
Get submission calendar.

### Chatbot

#### POST /chat/answer
Ask a question about green coding.

**Request Body:**
```json
{
  "message": "How to optimize loops?",
  "context": null
}
```

**Response:**
```json
{
  "answer": "Use list comprehensions...",
  "suggestions": ["...", "..."],
  "related_topics": ["loop_optimization"]
}
```

## Error Responses

All error responses follow this format:

```json
{
  "error": true,
  "message": "Error message",
  "status_code": 400,
  "error_type": "validation_error",
  "details": {
    "field": "email",
    "message": "Invalid email format"
  }
}
```

## Rate Limiting

API requests are rate-limited to 60 requests per minute per IP address.

## Supported Languages

- Python
- JavaScript/TypeScript
- Java
- C/C++

## Region Codes

- `usa`: United States
- `europe`: Europe
- `asia`: Asia
- `world`: World average

