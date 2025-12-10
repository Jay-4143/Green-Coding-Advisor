from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from .config import settings


_mongo_client: Optional[AsyncIOMotorClient] = None


def get_mongo_client() -> AsyncIOMotorClient:
    """
    Get a singleton Motor client.
    This connects to MongoDB Atlas (or local Mongo) using settings.mongodb_uri.
    """
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(settings.mongodb_uri)
    return _mongo_client


async def get_mongo_db():
    """
    FastAPI dependency that returns the configured MongoDB database.
    Usage:
        db = Depends(get_mongo_db)
    """
    client = get_mongo_client()
    db = client[settings.mongodb_db]
    return db


async def get_next_sequence(db, name: str) -> int:
    """
    Generate an auto-incrementing integer id for a given collection name.
    Uses a 'counters' collection internally. This lets us keep integer ids
    (user_id, project_id, etc.) while storing data in MongoDB.
    """
    result = await db["counters"].find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(result["seq"])



