from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os
import re


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8-sig",  # tolerate UTF-8 BOM in .env
        case_sensitive=False,
    )
    # Database Configuration
    database_url: str = "sqlite:///./green.db"
    database_url_async: str = "sqlite+aiosqlite:///./green.db"
    
    # MongoDB Configuration (Atlas or local)
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "green_coding"
    
    # JWT Configuration
    secret_key: str = "dev-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email Configuration
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = ""
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_tls: bool = True
    mail_ssl: bool = False
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # AI/ML Configuration
    huggingface_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # Carbon Tracking
    electricity_maps_api_key: Optional[str] = None
    codecarbon_region: str = "usa"  # usa, europe, asia, world
    codecarbon_offline: bool = True  # Use offline mode for CodeCarbon
    codecarbon_log_level: str = "warning"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000,http://127.0.0.1:8000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed_origins string into list"""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # File Upload
    max_file_size_mb: int = 10
    allowed_file_types: str = "py,java,js,ts,cpp,c,h"
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Parse allowed_file_types string into list"""
        return [ftype.strip() for ftype in self.allowed_file_types.split(",") if ftype.strip()]
    
    # Monitoring
    sentry_dsn: Optional[str] = None
    
    def validate_production(self) -> List[str]:
        """
        Validate required settings for production environment.
        Returns a list of validation errors (empty if all valid).
        """
        errors = []
        
        if self.environment == "production":
            # Required MongoDB configuration
            if not self.mongodb_uri or self.mongodb_uri == "mongodb://localhost:27017":
                errors.append("MONGODB_URI must be set to a production MongoDB Atlas connection string")
            
            if not self.mongodb_db:
                errors.append("MONGODB_DB must be set")
            
            # Required JWT secret key
            if not self.secret_key or self.secret_key == "dev-key-change-in-production":
                errors.append("SECRET_KEY must be changed from default value in production")
            
            if len(self.secret_key) < 32:
                errors.append("SECRET_KEY must be at least 32 characters long")
            
            # Required CORS configuration
            if not self.allowed_origins or "localhost" in self.allowed_origins.lower():
                errors.append("ALLOWED_ORIGINS must be set to production domain(s), not localhost")
            
            # Debug must be False in production
            if self.debug:
                errors.append("DEBUG must be False in production environment")
            
            # Validate MongoDB URI format
            if self.mongodb_uri and not (
                self.mongodb_uri.startswith("mongodb://") or 
                self.mongodb_uri.startswith("mongodb+srv://")
            ):
                errors.append("MONGODB_URI must be a valid MongoDB connection string")
        
        return errors
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"


settings = Settings()

# Validate production settings on import (only warn, don't fail)
if settings.is_production():
    validation_errors = settings.validate_production()
    if validation_errors:
        import warnings
        warnings.warn(
            f"Production configuration issues detected:\n" + "\n".join(f"  - {err}" for err in validation_errors),
            UserWarning
        )
