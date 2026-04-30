#!/usr/bin/env python
"""Test script to diagnose backend startup issues"""
import sys
import traceback

print("Testing backend imports and startup...")
print("=" * 50)

try:
    print("1. Importing config...")
    from app.config import settings
    print(f"   [OK] Config loaded. Database URL: {settings.database_url}")
except Exception as e:
    print(f"   [FAIL] Config import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("2. Importing MongoDB...")
    from app.mongo import get_mongo_db
    print("   [OK] MongoDB module imported")
except Exception as e:
    print(f"   [FAIL] MongoDB import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("3. Importing logger...")
    from app.logger import green_logger
    print("   [OK] Logger imported")
except Exception as e:
    print(f"   [FAIL] Logger import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Importing routers...")
    from app.routers import auth, submissions, metrics, advisor, chatbot, projects, teams, badges, reports, streaks
    print("   [OK] All routers imported")
except Exception as e:
    print(f"   [FAIL] Router import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("5. Creating app...")
    from app.main import create_app
    app = create_app()
    print("   [OK] App created successfully")
except Exception as e:
    print(f"   [FAIL] App creation failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("6. Testing MongoDB connection...")
    import asyncio
    from motor.motor_asyncio import AsyncIOMotorClient
    
    async def test_mongo():
        client = AsyncIOMotorClient(settings.mongodb_uri)
        # Ping the server
        await client.admin.command('ping')
        return True

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_mongo())
    print("   [OK] MongoDB connection works")
except Exception as e:
    print(f"   [FAIL] MongoDB connection failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("=" * 50)
print("All checks passed! Backend should start successfully.")
print("Try running: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")

