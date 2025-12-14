"""
Admin-only endpoints for system management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db
from ..schemas import User
from ..auth import get_current_active_user, require_role
from ..models import UserRole
from datetime import datetime

router = APIRouter()


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Dependency to require admin role"""
    role_value = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_value != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/stats")
async def get_system_stats(
    current_user: User = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get system-wide statistics (admin only)"""
    try:
        # Count users
        total_users = await db["users"].count_documents({})
        active_users = await db["users"].count_documents({"is_active": True})
        verified_users = await db["users"].count_documents({"is_verified": True})
        
        # Count by role
        admin_count = await db["users"].count_documents({"role": "admin"})
        developer_count = await db["users"].count_documents({"role": "developer"})
        
        # Count submissions
        total_submissions = await db["submissions"].count_documents({})
        completed_submissions = await db["submissions"].count_documents({"status": "completed"})
        
        # Calculate average green score
        pipeline = [
            {"$match": {"status": "completed", "green_score": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$green_score"}}}
        ]
        avg_result = await db["submissions"].aggregate(pipeline).to_list(length=1)
        average_green_score = avg_result[0]["avg_score"] if avg_result and avg_result[0].get("avg_score") else 0
        
        # Count teams and projects
        total_teams = await db["teams"].count_documents({})
        total_projects = await db["projects"].count_documents({})
        
        # Count badges
        total_badges = await db["badges"].count_documents({})
        
        # Recent activity (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_users = await db["users"].count_documents({"created_at": {"$gte": yesterday}})
        recent_submissions = await db["submissions"].count_documents({"created_at": {"$gte": yesterday}})
        
        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "verified": verified_users,
                "by_role": {
                    "admin": admin_count,
                    "developer": developer_count
                },
                "recent": recent_users
            },
            "submissions": {
                "total": total_submissions,
                "completed": completed_submissions,
                "average_green_score": round(average_green_score, 2) if average_green_score else 0,
                "recent": recent_submissions
            },
            "teams": {
                "total": total_teams
            },
            "projects": {
                "total": total_projects
            },
            "badges": {
                "total": total_badges
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching system stats: {str(e)}")


@router.get("/users")
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all users with pagination (admin only)"""
    try:
        # Build query
        query = {}
        if search:
            query["$or"] = [
                {"email": {"$regex": search, "$options": "i"}},
                {"username": {"$regex": search, "$options": "i"}}
            ]
        if role:
            query["role"] = role
        
        # Get total count
        total = await db["users"].count_documents(query)
        
        # Get users
        cursor = db["users"].find(query).sort("created_at", -1).skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        
        # Get submission counts for each user
        for user in users:
            user_id = user.get("id")
            if user_id:
                submission_count = await db["submissions"].count_documents({"user_id": user_id})
                user["submission_count"] = submission_count
            # Remove sensitive data
            user.pop("_id", None)
            user.pop("hashed_password", None)
            user.pop("email_verification_token", None)
            user.pop("password_reset_token", None)
        
        return {
            "users": users,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: str,
    current_user: User = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Update user role (admin only)"""
    if new_role not in ["admin", "developer"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be admin or developer")
    
    user = await db["users"].find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent changing your own role
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")
    
    await db["users"].update_one(
        {"id": user_id},
        {"$set": {"role": new_role, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": f"User role updated to {new_role}", "user_id": user_id, "new_role": new_role}


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    is_active: bool,
    current_user: User = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Activate or deactivate user (admin only)"""
    user = await db["users"].find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deactivating yourself
    if user_id == current_user.id and not is_active:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    await db["users"].update_one(
        {"id": user_id},
        {"$set": {"is_active": is_active, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": f"User {'activated' if is_active else 'deactivated'}", "user_id": user_id, "is_active": is_active}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Delete a user (admin only)"""
    user = await db["users"].find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting yourself
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    # Delete user and related data
    await db["users"].delete_one({"id": user_id})
    await db["submissions"].delete_many({"user_id": user_id})
    await db["team_members"].delete_many({"user_id": user_id})
    
    return {"message": "User deleted successfully", "user_id": user_id}


@router.get("/submissions")
async def get_all_submissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all submissions (admin only)"""
    try:
        query = {}
        if user_id:
            query["user_id"] = user_id
        if status:
            query["status"] = status
        
        total = await db["submissions"].count_documents(query)
        cursor = db["submissions"].find(query).sort("created_at", -1).skip(skip).limit(limit)
        submissions = await cursor.to_list(length=limit)
        
        for sub in submissions:
            sub.pop("_id", None)
        
        return {
            "submissions": submissions,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching submissions: {str(e)}")


@router.get("/teams")
async def get_all_teams(
    current_user: User = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all teams (admin only)"""
    try:
        teams = await db["teams"].find({}).sort("created_at", -1).to_list(length=None)
        
        for team in teams:
            team_id = team.get("id")
            if team_id:
                # Get member count
                member_count = await db["team_members"].count_documents({"team_id": team_id})
                team["member_count"] = member_count
                
                # Get project count
                project_count = await db["projects"].count_documents({"team_id": team_id})
                team["project_count"] = project_count
            
            team.pop("_id", None)
        
        return {"teams": teams, "total": len(teams)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching teams: {str(e)}")

