from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from .models import UserRole, SubmissionStatus


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRole = UserRole.DEVELOPER


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        import re
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
        if not re.match(pattern, v):
            raise ValueError('Password must be at least 8 characters, include 1 uppercase, 1 digit, and 1 special character')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    otp: Optional[str] = None
    otp_expiry: Optional[datetime] = None
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# User type for type hints (matches MongoDB user document structure)
class User(UserBase):
    id: int
    is_active: bool = True
    is_verified: bool = False
    created_at: Optional[datetime] = None
    otp: Optional[str] = None
    otp_expiry: Optional[datetime] = None
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Submission Schemas
class SubmissionBase(BaseModel):
    code_content: str
    language: str
    filename: Optional[str] = None
    project_id: Optional[int] = None


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionResponse(SubmissionBase):
    id: int
    user_id: int
    status: SubmissionStatus
    green_score: Optional[float] = None
    energy_consumption_wh: Optional[float] = None
    co2_emissions_g: Optional[float] = None
    cpu_time_ms: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    complexity_score: Optional[float] = None
    analysis_results: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    analyzed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Team Schemas
class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamResponse(TeamBase):
    id: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Badge Schemas
class BadgeBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    points: int = 0


class BadgeCreate(BadgeBase):
    criteria: Dict[str, Any]


class BadgeResponse(BadgeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Analysis Schemas
class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    region: Optional[str] = "usa"  # Region for CO2 calculation
    filename: Optional[str] = None


class OptimizationSuggestion(BaseModel):
    finding: str
    before_code: str
    after_code: str
    explanation: str
    predicted_improvement: Dict[str, float]
    severity: str  # low, medium, high


class AnalysisResponse(BaseModel):
    green_score: float
    energy_consumption_wh: float
    co2_emissions_g: float
    cpu_time_ms: float
    memory_usage_mb: float
    complexity_score: float
    suggestions: List[OptimizationSuggestion]
    analysis_details: Dict[str, Any]


# Metrics Schemas
class MetricsHistory(BaseModel):
    date: datetime
    green_score: float
    energy_wh: float
    co2_g: float


class UserMetrics(BaseModel):
    average_green_score: float
    total_submissions: int
    total_co2_saved: float
    badges_earned: int
    current_streak: int
    history: List[MetricsHistory]


# Chat Schemas
class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    answer: str
    suggestions: Optional[List[str]] = None
    related_topics: Optional[List[str]] = None
