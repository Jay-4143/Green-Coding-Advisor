import asyncio, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    c = AsyncIOMotorClient(settings.mongodb_uri)
    db = c[settings.mongodb_db]
    print(f"Connected to: {settings.mongodb_db}")
    print("users:", await db["users"].count_documents({}))
    print("submissions:", await db["submissions"].count_documents({}))
    print("user_badges:", await db["user_badges"].count_documents({}))
    print("badges:", await db["badges"].count_documents({}))
    print("teams:", await db["teams"].count_documents({}))
    
    # List all users
    users = await db["users"].find({}).sort("id", 1).to_list(length=None)
    print(f"\nUser list:")
    for u in users:
        sub_count = await db["submissions"].count_documents({"user_id": u.get("id"), "status": "completed"})
        print(f"  id={u.get('id'):3d}  username={u.get('username', '?'):20s}  subs={sub_count}")
    
    c.close()

asyncio.run(check())
