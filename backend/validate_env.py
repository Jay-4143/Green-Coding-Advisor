#!/usr/bin/env python3
"""
Environment Configuration Validator
Validates that all required environment variables are set correctly.
Run this script before deploying to production.
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.config import settings


def validate_environment():
    """Validate environment configuration"""
    print("=" * 60)
    print("Green Coding Advisor - Environment Configuration Validator")
    print("=" * 60)
    print()
    
    # Basic checks
    print(f"Environment: {settings.environment}")
    print(f"Debug Mode: {settings.debug}")
    print(f"MongoDB Database: {settings.mongodb_db}")
    print()
    
    # Production validation
    if settings.is_production():
        print("Running production validation checks...")
        print()
        
        errors = settings.validate_production()
        
        if errors:
            print("❌ PRODUCTION CONFIGURATION ERRORS FOUND:")
            print()
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
            print()
            print("Please fix these issues before deploying to production.")
            return False
        else:
            print("✅ All production configuration checks passed!")
            print()
            
            # Additional production recommendations
            print("Production Configuration Summary:")
            print(f"  ✓ MongoDB URI: {'Set' if settings.mongodb_uri and settings.mongodb_uri != 'mongodb://localhost:27017' else '⚠ Not configured'}")
            print(f"  ✓ Secret Key: {'Set' if settings.secret_key and len(settings.secret_key) >= 32 else '⚠ Too short'}")
            print(f"  ✓ CORS Origins: {len(settings.allowed_origins_list)} origin(s) configured")
            print(f"  ✓ Debug Mode: {'Disabled' if not settings.debug else '⚠ Enabled (should be False)'}")
            print()
            
            # Optional services
            print("Optional Services:")
            print(f"  - Email: {'Configured' if settings.mail_username and settings.mail_password else 'Not configured'}")
            print(f"  - Redis: {'Configured' if settings.redis_url and settings.redis_url != 'redis://localhost:6379/0' else 'Not configured'}")
            print(f"  - Sentry: {'Configured' if settings.sentry_dsn else 'Not configured'}")
            print(f"  - Electricity Maps: {'Configured' if settings.electricity_maps_api_key else 'Not configured'}")
            print()
            
            return True
    else:
        print("Running development validation checks...")
        print()
        
        # Development checks
        warnings = []
        
        if settings.secret_key == "dev-key-change-in-production":
            warnings.append("Using default SECRET_KEY (acceptable for development)")
        
        if not settings.mongodb_uri or settings.mongodb_uri == "mongodb://localhost:27017":
            warnings.append("Using default MongoDB URI (ensure MongoDB is running locally)")
        
        if warnings:
            print("⚠ Development Warnings:")
            for warning in warnings:
                print(f"  - {warning}")
            print()
        
        print("✅ Development configuration looks good!")
        print()
        return True


def check_env_file():
    """Check if .env file exists"""
    env_file = backend_dir / ".env"
    env_example = backend_dir / "env.example"
    
    if not env_file.exists():
        print("⚠ Warning: .env file not found!")
        print(f"   Please copy {env_example} to .env and configure it.")
        print()
        return False
    
    print(f"✓ Found .env file at {env_file}")
    print()
    return True


if __name__ == "__main__":
    print()
    
    # Check for .env file
    env_exists = check_env_file()
    
    # Validate configuration
    is_valid = validate_environment()
    
    print("=" * 60)
    
    if is_valid:
        print("✅ Environment validation completed successfully!")
        sys.exit(0)
    else:
        print("❌ Environment validation failed. Please fix the errors above.")
        sys.exit(1)

