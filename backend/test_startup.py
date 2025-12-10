#!/usr/bin/env python
"""Test script to diagnose backend startup issues"""
import sys
import traceback

print("Testing backend imports and startup...")
print("=" * 50)

try:
    print("1. Importing config...")
    from app.config import settings
    print(f"   ✓ Config loaded. Database URL: {settings.database_url}")
except Exception as e:
    print(f"   ✗ Config import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("2. Importing database...")
    from app.database import engine, Base
    print("   ✓ Database imported")
except Exception as e:
    print(f"   ✗ Database import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("3. Importing logger...")
    from app.logger import green_logger
    print("   ✓ Logger imported")
except Exception as e:
    print(f"   ✗ Logger import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Importing routers...")
    from app.routers import auth, submissions, metrics, advisor, chatbot, projects, teams, badges, reports, streaks
    print("   ✓ All routers imported")
except Exception as e:
    print(f"   ✗ Router import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("5. Creating app...")
    from app.main import create_app
    app = create_app()
    print("   ✓ App created successfully")
except Exception as e:
    print(f"   ✗ App creation failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("6. Testing database connection...")
    from app.database import SessionLocal
    from sqlalchemy import text
    db = SessionLocal()
    db.execute(text("SELECT 1"))
    db.close()
    print("   ✓ Database connection works")
except Exception as e:
    print(f"   ✗ Database connection failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("=" * 50)
print("All checks passed! Backend should start successfully.")
print("Try running: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")

