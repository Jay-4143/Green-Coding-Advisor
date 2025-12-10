"""
Quick script to test MongoDB connection and diagnose issues
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.config import settings
from app.mongo import get_mongo_client, get_mongo_db


async def test_connection():
    """Test MongoDB connection"""
    print("Testing MongoDB connection...")
    print(f"MongoDB URI: {settings.mongodb_uri[:50]}..." if len(settings.mongodb_uri) > 50 else f"MongoDB URI: {settings.mongodb_uri}")
    print(f"MongoDB DB: {settings.mongodb_db}")
    print()
    
    try:
        # Test client connection
        print("1. Testing client connection...")
        client = get_mongo_client()
        
        # Try to get server info (this will fail if connection is bad)
        print("2. Getting server info...")
        server_info = await client.admin.command('ping')
        print(f"   ✓ Server ping successful: {server_info}")
        
        # Test database access
        print("3. Testing database access...")
        db = await get_mongo_db().__anext__()
        print(f"   ✓ Database '{settings.mongodb_db}' accessible")
        
        # Test collection access
        print("4. Testing users collection...")
        users_count = await db["users"].count_documents({})
        print(f"   ✓ Users collection accessible (found {users_count} users)")
        
        # List all collections
        print("5. Listing collections...")
        collections = await db.list_collection_names()
        print(f"   ✓ Collections: {', '.join(collections) if collections else 'None'}")
        
        print("\n✅ MongoDB connection test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ MongoDB connection test FAILED!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your MONGODB_URI in backend/.env")
        print("2. Verify your MongoDB Atlas IP whitelist includes your current IP")
        print("3. Check your MongoDB username and password")
        print("4. Ensure the database name in MONGODB_DB exists")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)

