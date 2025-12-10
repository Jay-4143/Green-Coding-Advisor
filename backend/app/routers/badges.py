from fastapi import APIRouter, Depends, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db
from ..schemas import User
from ..auth import get_current_active_user
from ..badge_service import badge_service

router = APIRouter()


@router.get("/me")
async def get_my_badges(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get current user's badges"""
    # Ensure defaults exist
    await badge_service.get_all_badges(db)
    badges = await badge_service.get_user_badges(current_user.id, db)
    return {"badges": badges}


@router.get("/user/{user_id}")
async def get_user_badges(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get badges for a specific user"""
    # Users can view their own badges or admins can view any user's badges
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await badge_service.get_all_badges(db)
    badges = await badge_service.get_user_badges(user_id, db)
    return {"badges": badges}


@router.get("/all")
async def get_all_badges(
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all available badges"""
    badges = await badge_service.get_all_badges(db)
    return {"badges": badges}


@router.post("/check/{user_id}")
async def check_and_award_badges(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Manually check and award badges for a user"""
    # Users can check their own badges or admins can check any user's badges
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    newly_awarded = await badge_service.check_and_award_badges(user_id, db)
    return {
        "newly_awarded": newly_awarded,
        "count": len(newly_awarded)
    }


@router.post("/initialize")
async def initialize_badges(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Initialize default badges (admin only)"""
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    await badge_service.initialize_default_badges(db)
    return {"message": "Default badges initialized successfully"}
