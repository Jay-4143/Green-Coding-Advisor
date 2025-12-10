"""
MongoDB index creation for optimized queries.
Run this on application startup to ensure indexes exist.
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, TEXT
from typing import List, Tuple


async def create_indexes(db: AsyncIOMotorDatabase):
    """
    Create all necessary indexes for MongoDB collections.
    This should be called during application startup.
    """
    indexes_created = []
    
    try:
        # Users collection indexes
        users_collection = db["users"]
        
        # Email index (unique)
        await users_collection.create_index([("email", ASCENDING)], unique=True, background=True)
        indexes_created.append("users.email (unique)")
        
        # Username index (unique)
        await users_collection.create_index([("username", ASCENDING)], unique=True, background=True)
        indexes_created.append("users.username (unique)")
        
        # User ID index
        await users_collection.create_index([("id", ASCENDING)], unique=True, background=True)
        indexes_created.append("users.id (unique)")
        
        # Active users index
        await users_collection.create_index([("is_active", ASCENDING), ("is_verified", ASCENDING)], background=True)
        indexes_created.append("users.is_active, is_verified")
        
        # Submissions collection indexes
        submissions_collection = db["submissions"]
        
        # User ID + created_at for user submissions query
        await submissions_collection.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)], background=True)
        indexes_created.append("submissions.user_id, created_at")
        
        # Submission ID index
        await submissions_collection.create_index([("id", ASCENDING)], unique=True, background=True)
        indexes_created.append("submissions.id (unique)")
        
        # Status index for filtering
        await submissions_collection.create_index([("status", ASCENDING)], background=True)
        indexes_created.append("submissions.status")
        
        # Language index
        await submissions_collection.create_index([("language", ASCENDING)], background=True)
        indexes_created.append("submissions.language")
        
        # Green score index for leaderboard queries
        await submissions_collection.create_index([("green_score", DESCENDING)], background=True)
        indexes_created.append("submissions.green_score")
        
        # Project ID index
        await submissions_collection.create_index([("project_id", ASCENDING)], background=True)
        indexes_created.append("submissions.project_id")
        
        # Created at index for time-based queries
        await submissions_collection.create_index([("created_at", DESCENDING)], background=True)
        indexes_created.append("submissions.created_at")
        
        # Compound index for user submissions with status
        await submissions_collection.create_index(
            [("user_id", ASCENDING), ("status", ASCENDING), ("created_at", DESCENDING)],
            background=True
        )
        indexes_created.append("submissions.user_id, status, created_at")
        
        # Badges collection indexes
        badges_collection = db["badges"]
        
        # Badge ID index
        await badges_collection.create_index([("id", ASCENDING)], unique=True, background=True)
        indexes_created.append("badges.id (unique)")
        
        # Badge name index
        await badges_collection.create_index([("name", ASCENDING)], unique=True, background=True)
        indexes_created.append("badges.name (unique)")
        
        # User badges collection indexes
        user_badges_collection = db["user_badges"]
        
        # User ID + badge ID (unique combination)
        await user_badges_collection.create_index(
            [("user_id", ASCENDING), ("badge_id", ASCENDING)],
            unique=True,
            background=True
        )
        indexes_created.append("user_badges.user_id, badge_id (unique)")
        
        # User ID + earned_at for user badges query
        await user_badges_collection.create_index(
            [("user_id", ASCENDING), ("earned_at", DESCENDING)],
            background=True
        )
        indexes_created.append("user_badges.user_id, earned_at")
        
        # Projects collection indexes
        projects_collection = db.get_collection("projects")
        if projects_collection is not None:
            await projects_collection.create_index([("id", ASCENDING)], unique=True, background=True)
            indexes_created.append("projects.id (unique)")
            
            await projects_collection.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)], background=True)
            indexes_created.append("projects.user_id, created_at")
        
        # Teams collection indexes
        teams_collection = db.get_collection("teams")
        if teams_collection is not None:
            await teams_collection.create_index([("id", ASCENDING)], unique=True, background=True)
            indexes_created.append("teams.id (unique)")
            
            await teams_collection.create_index([("name", ASCENDING)], unique=True, background=True)
            indexes_created.append("teams.name (unique)")
        
        # Counters collection index (for sequence generation)
        counters_collection = db["counters"]
        await counters_collection.create_index([("_id", ASCENDING)], unique=True, background=True)
        indexes_created.append("counters._id (unique)")
        
        return indexes_created
        
    except Exception as e:
        # Log error but don't fail startup
        import logging
        logging.error(f"Error creating MongoDB indexes: {e}")
        return indexes_created

