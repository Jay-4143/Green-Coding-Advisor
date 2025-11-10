from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base


class UserRole(str, enum.Enum):
    STUDENT = "student"
    DEVELOPER = "developer"
    ADMIN = "admin"


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.DEVELOPER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    submissions = relationship("Submission", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    members = relationship("TeamMember", back_populates="team")
    projects = relationship("Project", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(50), default="member")  # member, admin
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    team_id = Column(Integer, ForeignKey("teams.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="projects")
    submissions = relationship("Submission", back_populates="project")


class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Code information
    code_content = Column(Text, nullable=False)
    language = Column(String(20), nullable=False)  # python, java, javascript, cpp
    filename = Column(String(255))
    
    # Analysis results
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING)
    green_score = Column(Float)  # 0-100
    energy_consumption_wh = Column(Float)  # Energy in watt-hours
    co2_emissions_g = Column(Float)  # CO2 emissions in grams
    cpu_time_ms = Column(Float)  # CPU time in milliseconds
    memory_usage_mb = Column(Float)  # Memory usage in MB
    complexity_score = Column(Float)  # Code complexity score
    
    # Analysis metadata
    analysis_results = Column(JSON)  # Store detailed analysis results
    suggestions = Column(JSON)  # Store optimization suggestions
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    analyzed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    project = relationship("Project", back_populates="submissions")


class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(255))  # Icon URL or emoji
    criteria = Column(JSON)  # Criteria for earning the badge
    points = Column(Integer, default=0)  # Points awarded
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge")


class CodeAnalysis(Base):
    __tablename__ = "code_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    
    # Analysis details
    cyclomatic_complexity = Column(Float)
    cognitive_complexity = Column(Float)
    maintainability_index = Column(Float)
    lines_of_code = Column(Integer)
    comment_ratio = Column(Float)
    
    # Performance metrics
    estimated_memory_usage = Column(Float)
    estimated_cpu_time = Column(Float)
    algorithm_complexity = Column(String(20))  # O(n), O(log n), etc.
    
    # Code smells detected
    code_smells = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
