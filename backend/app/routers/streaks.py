from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db
from ..schemas import User
from ..auth import get_current_active_user
from ..streak_service import streak_service

router = APIRouter()


@router.get("/me")
async def get_my_streak(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get current user's streak information"""
    streak_info = await streak_service.get_streak_info(current_user.id, db)
    return streak_info


@router.get("/user/{user_id}")
async def get_user_streak(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get streak information for a specific user"""
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    streak_info = await streak_service.get_streak_info(user_id, db)
    return streak_info


@router.get("/me/calendar")
async def get_my_submission_calendar(
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get submission calendar for current user"""
    calendar = await streak_service.get_submission_calendar(current_user.id, db, days)
    return calendar
