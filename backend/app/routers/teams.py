from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db, get_next_sequence
from ..schemas import User
from ..schemas import TeamBase, TeamCreate, TeamResponse, TeamMemberAdd
from ..auth import get_current_active_user
from ..logger import green_logger

router = APIRouter()


@router.post("", response_model=TeamResponse)
async def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Create a new team"""
    # Create team
    team_id = await get_next_sequence(db, "teams")
    team_doc = {
        "id": team_id,
        "name": team_data.name,
        "description": team_data.description,
        "created_by": current_user.id,
        "created_at": datetime.utcnow()
    }
    
    await db["teams"].insert_one(team_doc)
    
    # Add creator as team admin
    member_id = await get_next_sequence(db, "team_members")
    team_member_doc = {
        "id": member_id,
        "team_id": team_id,
        "user_id": current_user.id,
        "role": "admin",
        "joined_at": datetime.utcnow()
    }
    await db["team_members"].insert_one(team_member_doc)
    
    green_logger.log_user_action(
        user_id=current_user.id,
        action="team_created",
        details={"team_id": team_id, "team_name": team_data.name}
    )
    
    return TeamResponse(**team_doc)


@router.get("", response_model=List[TeamResponse])
async def get_my_teams(
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all teams the current user is a member of"""
    team_memberships = await db["team_members"].find({"user_id": current_user.id}).to_list(length=None)
    team_ids = [tm["team_id"] for tm in team_memberships]
    
    if not team_ids:
        return []
    
    cursor = db["teams"].find({"id": {"$in": team_ids}})
    teams = await cursor.to_list(length=None)
    
    return [TeamResponse(**{k: v for k, v in t.items() if k != "_id"}) for t in teams]


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get team details"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is a member
    membership = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": current_user.id
    })
    
    if not membership and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not a team member")
    
    return TeamResponse(**{k: v for k, v in team.items() if k != "_id"})


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_data: TeamBase,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Update team details (admin only)"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is team admin
    membership = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": current_user.id,
        "role": "admin"
    })
    
    if not membership and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not a team admin")
    
    await db["teams"].update_one(
        {"id": team_id},
        {
            "$set": {
                "name": team_data.name,
                "description": team_data.description
            }
        }
    )
    
    updated_team = await db["teams"].find_one({"id": team_id})
    return TeamResponse(**{k: v for k, v in updated_team.items() if k != "_id"})


@router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Delete a team (admin only)"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is team admin or creator
    if team.get("created_by") != current_user.id and current_user.role.value != "admin":
        membership = await db["team_members"].find_one({
            "team_id": team_id,
            "user_id": current_user.id,
            "role": "admin"
        })
        if not membership:
            raise HTTPException(status_code=403, detail="Not authorized to delete team")
    
    await db["teams"].delete_one({"id": team_id})
    await db["team_members"].delete_many({"team_id": team_id})
    
    return {"message": "Team deleted successfully"}


@router.post("/{team_id}/members")
async def add_team_member(
    team_id: int,
    member_data: TeamMemberAdd,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Add a member to a team (admin only)"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if current user is team admin
    membership = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": current_user.id,
        "role": "admin"
    })
    
    if not membership and team.get("created_by") != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not a team admin")
    
    # Check if user exists
    user = await db["users"].find_one({"email": member_data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User with this email not found")
    
    # Check if already a member
    existing = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": user["id"]
    })
    if existing:
        raise HTTPException(status_code=400, detail="User is already a team member")
    
    # Add member
    member_id = await get_next_sequence(db, "team_members")
    team_member_doc = {
        "id": member_id,
        "team_id": team_id,
        "user_id": user["id"],
        "role": member_data.role,
        "joined_at": datetime.utcnow()
    }
    await db["team_members"].insert_one(team_member_doc)
    
    green_logger.log_user_action(
        user_id=current_user.id,
        action="team_member_added",
        details={"team_id": team_id, "added_user_id": user["id"]}
    )
    
    return {"message": "Member added successfully"}


@router.delete("/{team_id}/members/{user_id}")
async def remove_team_member(
    team_id: int,
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Remove a member from a team (admin only)"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if current user is team admin
    membership = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": current_user.id,
        "role": "admin"
    })
    
    if not membership and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not a team admin")
    
    # Remove member
    result = await db["team_members"].delete_one({
        "team_id": team_id,
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return {"message": "Member removed successfully"}


@router.get("/{team_id}/members")
async def get_team_members(
    team_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all members of a team"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is a member
    membership = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": current_user.id
    })
    
    if not membership and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not a team member")
    
    members_cursor = db["team_members"].find({"team_id": team_id})
    members = await members_cursor.to_list(length=None)
    
    result = []
    for m in members:
        user = await db["users"].find_one({"id": m["user_id"]})
        if user:
            result.append({
                "id": user["id"],
                "username": user.get("username"),
                "email": user.get("email"),
                "role": m.get("role"),
                "joined_at": m.get("joined_at").isoformat() if m.get("joined_at") else None
            })
    
    return result


@router.get("/{team_id}/dashboard")
async def get_team_dashboard(
    team_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get team dashboard with metrics and leaderboard"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is a member
    membership = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": current_user.id
    })
    
    if not membership and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not a team member")
    
    # Get team members
    team_members_cursor = db["team_members"].find({"team_id": team_id})
    team_members = await team_members_cursor.to_list(length=None)
    member_ids = [tm["user_id"] for tm in team_members]
    
    # Get all submissions from team members
    submissions_cursor = db["submissions"].find({
        "user_id": {"$in": member_ids},
        "status": "completed"
    })
    submissions = await submissions_cursor.to_list(length=None)
    
    # Calculate team metrics
    total_submissions = len(submissions)
    if total_submissions > 0:
        avg_green_score = sum(s.get("green_score", 0) or 0 for s in submissions) / total_submissions
        total_co2_saved = sum(s.get("co2_emissions_g", 0) or 0 for s in submissions)
        total_energy_saved = sum(s.get("energy_consumption_wh", 0) or 0 for s in submissions)
    else:
        avg_green_score = 0
        total_co2_saved = 0
        total_energy_saved = 0
    
    # Get team projects
    projects_cursor = db["projects"].find({"team_id": team_id})
    projects = await projects_cursor.to_list(length=None)
    
    # Team leaderboard (members sorted by average green score)
    member_stats = []
    for member in team_members:
        user_submissions = [s for s in submissions if s.get("user_id") == member["user_id"]]
        user = await db["users"].find_one({"id": member["user_id"]})
        
        if user_submissions:
            avg_score = sum(s.get("green_score", 0) or 0 for s in user_submissions) / len(user_submissions)
            co2_saved = sum(s.get("co2_emissions_g", 0) or 0 for s in user_submissions)
            submission_count = len(user_submissions)
        else:
            avg_score = 0
            co2_saved = 0
            submission_count = 0
        
        member_stats.append({
            "user_id": member["user_id"],
            "username": user.get("username") if user else "Unknown",
            "average_green_score": round(avg_score, 2),
            "total_submissions": submission_count,
            "total_co2_saved": round(co2_saved, 3),
            "role": member.get("role")
        })
    
    # Sort by average green score
    member_stats.sort(key=lambda x: x["average_green_score"], reverse=True)
    
    return {
        "team": {
            "id": team["id"],
            "name": team["name"],
            "description": team.get("description"),
            "created_by": team.get("created_by"),
            "created_at": team.get("created_at").isoformat() if team.get("created_at") else None
        },
        "metrics": {
            "total_members": len(team_members),
            "total_projects": len(projects),
            "total_submissions": total_submissions,
            "average_green_score": round(avg_green_score, 2),
            "total_co2_saved": round(total_co2_saved, 3),
            "total_energy_saved": round(total_energy_saved, 3)
        },
        "leaderboard": member_stats,
        "projects": [
            {
                "id": p["id"],
                "name": p.get("name"),
                "description": p.get("description"),
                "created_at": p.get("created_at").isoformat() if p.get("created_at") else None
            }
            for p in projects
        ]
    }


@router.get("/{team_id}/leaderboard")
async def get_team_leaderboard(
    team_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get team leaderboard"""
    team = await db["teams"].find_one({"id": team_id})
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is a member
    membership = await db["team_members"].find_one({
        "team_id": team_id,
        "user_id": current_user.id
    })
    
    if not membership and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not a team member")
    
    # Get team members
    team_members_cursor = db["team_members"].find({"team_id": team_id})
    team_members = await team_members_cursor.to_list(length=None)
    member_ids = [tm["user_id"] for tm in team_members]
    
    # Get all submissions from team members
    submissions_cursor = db["submissions"].find({
        "user_id": {"$in": member_ids},
        "status": "completed"
    })
    submissions = await submissions_cursor.to_list(length=None)
    
    # Calculate member statistics
    member_stats = []
    for member in team_members:
        user_submissions = [s for s in submissions if s.get("user_id") == member["user_id"]]
        user = await db["users"].find_one({"id": member["user_id"]})
        
        if user_submissions:
            avg_score = sum(s.get("green_score", 0) or 0 for s in user_submissions) / len(user_submissions)
            co2_saved = sum(s.get("co2_emissions_g", 0) or 0 for s in user_submissions)
            submission_count = len(user_submissions)
        else:
            avg_score = 0
            co2_saved = 0
            submission_count = 0
        
        member_stats.append({
            "user_id": member["user_id"],
            "username": user.get("username") if user else "Unknown",
            "average_green_score": round(avg_score, 2),
            "total_submissions": submission_count,
            "total_co2_saved": round(co2_saved, 3),
            "role": member.get("role")
        })
    
    # Sort by average green score
    member_stats.sort(key=lambda x: x["average_green_score"], reverse=True)
    
    # Add rank
    for idx, stat in enumerate(member_stats, start=1):
        stat["rank"] = idx
    
    return {"entries": member_stats}
