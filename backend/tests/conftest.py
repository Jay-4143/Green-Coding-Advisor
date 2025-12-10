"""
Pytest configuration and fixtures for Green Coding Advisor tests
Updated for MongoDB/Motor async support
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
import sys
from pathlib import Path
from datetime import datetime

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.main import create_app
from app.mongo import get_mongo_db, get_next_sequence
from app.auth import get_password_hash
from app.config import settings
from app.schemas import UserRole


# Test MongoDB database name
TEST_DB_NAME = "green_coding_test"


@pytest_asyncio.fixture(scope="function")
async def test_db():
    """Create a test MongoDB database for each test"""
    # Use test database
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[TEST_DB_NAME]
    
    # Clean up before test
    collections = await db.list_collection_names()
    for collection_name in collections:
        await db[collection_name].delete_many({})
    
    try:
        yield db
    finally:
        # Clean up after test
        collections = await db.list_collection_names()
        for collection_name in collections:
            await db[collection_name].delete_many({})
        client.close()


@pytest_asyncio.fixture(scope="function")
async def client(test_db):
    """Create a test client with MongoDB database override"""
    app = create_app()
    
    async def override_get_mongo_db():
        return test_db
    
    app.dependency_overrides[get_mongo_db] = override_get_mongo_db
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(test_db):
    """Create a test user in MongoDB"""
    user_id = await get_next_sequence(test_db, "users")
    hashed_password = get_password_hash("Test@1234")
    
    user_doc = {
        "id": user_id,
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": hashed_password,
        "role": UserRole.DEVELOPER.value,
        "is_active": True,
        "is_verified": True,
        "created_at": datetime.utcnow(),
        "current_streak": 0,
        "longest_streak": 0,
    }
    
    await test_db["users"].insert_one(user_doc)
    
    # Return user document
    return user_doc


@pytest_asyncio.fixture
async def test_admin(test_db):
    """Create a test admin user in MongoDB"""
    user_id = await get_next_sequence(test_db, "users")
    hashed_password = get_password_hash("Admin@1234")
    
    admin_doc = {
        "id": user_id,
        "email": "admin@example.com",
        "username": "admin",
        "hashed_password": hashed_password,
        "role": UserRole.ADMIN.value,
        "is_active": True,
        "is_verified": True,
        "created_at": datetime.utcnow(),
        "current_streak": 0,
        "longest_streak": 0,
    }
    
    await test_db["users"].insert_one(admin_doc)
    
    return admin_doc


@pytest_asyncio.fixture
async def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = await client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": "Test@1234"
        }
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
