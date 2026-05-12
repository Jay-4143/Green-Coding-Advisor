"""List all users in the database."""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def list_users():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["green_coding"]
    
    users = await db["users"].find({}).sort("id", 1).to_list(length=None)
    print(f"Total users: {len(users)}\n")
    for u in users:
        # Count submissions
        sub_count = await db["submissions"].count_documents({"user_id": u.get("id"), "status": "completed"})
        # Count badges
        badge_count = await db["user_badges"].count_documents({"user_id": u.get("id")})
        print(f"  id={u.get('id'):3d}  username={u.get('username', '?'):20s}  email={u.get('email', '?'):35s}  subs={sub_count}  badges={badge_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(list_users())
