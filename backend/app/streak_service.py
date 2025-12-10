from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, date, timedelta
from typing import Optional
from .mongo import get_next_sequence


class StreakService:
    """Service for tracking user submission streaks"""
    
    @staticmethod
    async def update_streak(user_id: int, db: AsyncIOMotorDatabase) -> dict:
        """Update user's streak based on submission date"""
        user = await db["users"].find_one({"id": user_id})
        if not user:
            return {"current_streak": 0, "longest_streak": 0}
        
        today = date.today()
        last_submission_date = None
        if user.get("last_submission_date"):
            if isinstance(user["last_submission_date"], str):
                last_submission_date = datetime.fromisoformat(user["last_submission_date"]).date()
            elif isinstance(user["last_submission_date"], datetime):
                last_submission_date = user["last_submission_date"].date()
        
        # If no previous submission, start streak at 1
        if last_submission_date is None:
            current_streak = 1
            longest_streak = max(user.get("longest_streak", 0), 1)
            await db["users"].update_one(
                {"id": user_id},
                {
                    "$set": {
                        "current_streak": current_streak,
                        "longest_streak": longest_streak,
                        "last_submission_date": datetime.utcnow()
                    }
                }
            )
        else:
            days_diff = (today - last_submission_date).days
            
            if days_diff == 0:
                # Same day submission - streak continues
                current_streak = user.get("current_streak", 0) or 1
                longest_streak = user.get("longest_streak", 0)
            elif days_diff == 1:
                # Consecutive day - increment streak
                current_streak = (user.get("current_streak", 0) or 0) + 1
                longest_streak = max(user.get("longest_streak", 0), current_streak)
                await db["users"].update_one(
                    {"id": user_id},
                    {
                        "$set": {
                            "current_streak": current_streak,
                            "longest_streak": longest_streak,
                            "last_submission_date": datetime.utcnow()
                        }
                    }
                )
            else:
                # Streak broken - reset to 1
                current_streak = 1
                await db["users"].update_one(
                    {"id": user_id},
                    {
                        "$set": {
                            "current_streak": current_streak,
                            "last_submission_date": datetime.utcnow()
                        }
                    }
                )
                longest_streak = user.get("longest_streak", 0)
        
        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_submission_date": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    async def get_streak_info(user_id: int, db: AsyncIOMotorDatabase) -> dict:
        """Get user's streak information"""
        user = await db["users"].find_one({"id": user_id})
        if not user:
            return {"current_streak": 0, "longest_streak": 0, "days_until_next": 0}
        
        today = date.today()
        last_submission_date = None
        if user.get("last_submission_date"):
            if isinstance(user["last_submission_date"], str):
                last_submission_date = datetime.fromisoformat(user["last_submission_date"]).date()
            elif isinstance(user["last_submission_date"], datetime):
                last_submission_date = user["last_submission_date"].date()
        
        if last_submission_date is None:
            days_until_next = 0
            days_diff = None
        else:
            days_diff = (today - last_submission_date).days
            if days_diff == 0:
                days_until_next = 1  # Can submit tomorrow to continue streak
            else:
                days_until_next = max(0, 1 - days_diff)  # Days until streak would continue
        
        return {
            "current_streak": user.get("current_streak", 0) or 0,
            "longest_streak": user.get("longest_streak", 0) or 0,
            "last_submission_date": user.get("last_submission_date").isoformat() if user.get("last_submission_date") else None,
            "days_until_next": days_until_next,
            "is_streak_active": days_diff == 0 or days_diff == 1 if last_submission_date else False
        }
    
    @staticmethod
    async def get_submission_calendar(user_id: int, db: AsyncIOMotorDatabase, days: int = 30) -> dict:
        """Get submission calendar for the last N days"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        cursor = db["submissions"].find({
            "user_id": user_id,
            "status": "completed",
            "created_at": {"$gte": start_datetime, "$lte": end_datetime}
        })
        
        submissions = await cursor.to_list(length=None)
        
        # Create calendar data
        calendar_data = {}
        for submission in submissions:
            sub_date = None
            if submission.get("created_at"):
                if isinstance(submission["created_at"], str):
                    sub_date = datetime.fromisoformat(submission["created_at"]).date()
                elif isinstance(submission["created_at"], datetime):
                    sub_date = submission["created_at"].date()
            
            if sub_date:
                date_str = sub_date.isoformat()
                if date_str not in calendar_data:
                    calendar_data[date_str] = 0
                calendar_data[date_str] += 1
        
        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "submissions": calendar_data,
            "total_days": days,
            "days_with_submissions": len(calendar_data)
        }


streak_service = StreakService()
