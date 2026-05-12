"""Remove dummy test users from the REAL database."""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

DUMMY_PATTERNS = ["User1", "User2", "User3", "TeamUser", "TestUser"]

async def cleanup():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]
    
    for name in DUMMY_PATTERNS:
        user = await db["users"].find_one({"username": name})
        if not user:
            print(f"  [SKIP] '{name}' not found")
            continue
        
        uid = user.get("id")
        sub_del = await db["submissions"].delete_many({"user_id": uid})
        badge_del = await db["user_badges"].delete_many({"user_id": uid})
        tm_del = await db["team_members"].delete_many({"user_id": uid})
        await db["users"].delete_one({"id": uid})
        print(f"  [OK] Deleted '{name}' (id={uid}): {sub_del.deleted_count} subs, {badge_del.deleted_count} badges, {tm_del.deleted_count} memberships")
    
    # Verify
    remaining = await db["users"].count_documents({})
    print(f"\nRemaining users: {remaining}")
    client.close()

if __name__ == "__main__":
    asyncio.run(cleanup())
