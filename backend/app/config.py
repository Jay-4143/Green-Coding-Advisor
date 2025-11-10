from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "sqlite:///./green.db"
    database_url_async: str = "sqlite+aiosqlite:///./green.db"
    
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
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # File Upload
    max_file_size_mb: int = 10
    allowed_file_types: List[str] = ["py", "java", "js", "ts", "cpp", "c", "h"]
    
    # Monitoring
    sentry_dsn: Optional[str] = None
    
    class Config:
        env_file = None
        case_sensitive = False


settings = Settings()
