from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db, get_next_sequence
from ..schemas import User
from ..schemas import ProjectBase, ProjectCreate, ProjectResponse
from ..auth import get_current_active_user
from ..logger import green_logger

router = APIRouter()


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Create a new project"""
    # If team_id provided, verify user is team member
    if project_data.team_id:
        team = await db["teams"].find_one({"id": project_data.team_id})
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        # Check if user is team member
        membership = await db["team_members"].find_one({
            "team_id": project_data.team_id,
            "user_id": current_user.id
        })
        
        if not membership and current_user.role.value != "admin":
            raise HTTPException(status_code=403, detail="Not a team member")
    
    # Create project
    project_id = await get_next_sequence(db, "projects")
    project_doc = {
        "id": project_id,
        "name": project_data.name,
        "description": project_data.description,
        "team_id": project_data.team_id,
        "created_by": current_user.id,
        "created_at": datetime.utcnow()
    }
    
    await db["projects"].insert_one(project_doc)
    
    green_logger.log_user_action(
        user_id=current_user.id,
        action="project_created",
        details={"project_id": project_id, "project_name": project_data.name}
    )
    
    return ProjectResponse(**project_doc)


@router.get("", response_model=List[ProjectResponse])
async def get_my_projects(
    team_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all projects for the current user"""
    
    # Filter by team if team_id provided
    if team_id:
        # Check if user is team member
        membership = await db["team_members"].find_one({
            "team_id": team_id,
            "user_id": current_user.id
        })
        
        if not membership and current_user.role.value != "admin":
            raise HTTPException(status_code=403, detail="Not a team member")
        
        cursor = db["projects"].find({"team_id": team_id})
    else:
        # Get user's projects (created by user or in user's teams)
        team_memberships = await db["team_members"].find({"user_id": current_user.id}).to_list(length=None)
        team_ids = [tm["team_id"] for tm in team_memberships]
        
        cursor = db["projects"].find({
            "$or": [
                {"created_by": current_user.id},
                {"team_id": {"$in": team_ids}}
            ]
        })
    
    projects = await cursor.to_list(length=None)
    return [ProjectResponse(**{k: v for k, v in p.items() if k != "_id"}) for p in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get project details"""
    project = await db["projects"].find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check access
    if project.get("team_id"):
        membership = await db["team_members"].find_one({
            "team_id": project["team_id"],
            "user_id": current_user.id
        })
        if not membership and project.get("created_by") != current_user.id and current_user.role.value != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
    elif project.get("created_by") != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return ProjectResponse(**{k: v for k, v in project.items() if k != "_id"})


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectBase,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Update project details"""
    project = await db["projects"].find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if user is creator or team admin
    if project.get("created_by") != current_user.id:
        if project.get("team_id"):
            membership = await db["team_members"].find_one({
                "team_id": project["team_id"],
                "user_id": current_user.id,
                "role": "admin"
            })
            if not membership and current_user.role.value != "admin":
                raise HTTPException(status_code=403, detail="Not authorized")
        else:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    await db["projects"].update_one(
        {"id": project_id},
        {
            "$set": {
                "name": project_data.name,
                "description": project_data.description
            }
        }
    )
    
    updated_project = await db["projects"].find_one({"id": project_id})
    return ProjectResponse(**{k: v for k, v in updated_project.items() if k != "_id"})


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Delete a project"""
    project = await db["projects"].find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if user is creator or team admin
    if project.get("created_by") != current_user.id:
        if project.get("team_id"):
            membership = await db["team_members"].find_one({
                "team_id": project["team_id"],
                "user_id": current_user.id,
                "role": "admin"
            })
            if not membership and current_user.role.value != "admin":
                raise HTTPException(status_code=403, detail="Not authorized")
        else:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    await db["projects"].delete_one({"id": project_id})
    
    return {"message": "Project deleted successfully"}


@router.get("/{project_id}/summary")
async def get_project_summary(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get project summary with metrics"""
    project = await db["projects"].find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check access
    if project.get("team_id"):
        membership = await db["team_members"].find_one({
            "team_id": project["team_id"],
            "user_id": current_user.id
        })
        if not membership and project.get("created_by") != current_user.id and current_user.role.value != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
    elif project.get("created_by") != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get project submissions
    cursor = db["submissions"].find({
        "project_id": project_id,
        "status": "completed"
    })
    submissions = await cursor.to_list(length=None)
    
    # Calculate metrics
    total_submissions = len(submissions)
    if total_submissions > 0:
        avg_green_score = sum(s.get("green_score", 0) or 0 for s in submissions) / total_submissions
        total_co2_saved = sum(s.get("co2_emissions_g", 0) or 0 for s in submissions)
        total_energy_saved = sum(s.get("energy_consumption_wh", 0) or 0 for s in submissions)
        best_score = max((s.get("green_score", 0) or 0 for s in submissions), default=0)
    else:
        avg_green_score = 0
        total_co2_saved = 0
        total_energy_saved = 0
        best_score = 0
    
    # Get language breakdown
    language_stats = {}
    for submission in submissions:
        lang = submission.get("language", "unknown")
        if lang not in language_stats:
            language_stats[lang] = {
                "count": 0,
                "avg_score": 0,
                "scores": []
            }
        language_stats[lang]["count"] += 1
        if submission.get("green_score"):
            language_stats[lang]["scores"].append(submission["green_score"])
    
    # Calculate averages
    for lang in language_stats:
        scores = language_stats[lang]["scores"]
        language_stats[lang]["avg_score"] = sum(scores) / len(scores) if scores else 0
        del language_stats[lang]["scores"]
    
    # Sort submissions by created_at
    submissions_sorted = sorted(
        submissions,
        key=lambda x: x.get("created_at", datetime.min) if isinstance(x.get("created_at"), datetime) else datetime.min,
        reverse=True
    )[:10]
    
    return {
        "project": {
            "id": project["id"],
            "name": project["name"],
            "description": project.get("description"),
            "team_id": project.get("team_id"),
            "created_by": project.get("created_by"),
            "created_at": project.get("created_at").isoformat() if project.get("created_at") else None
        },
        "metrics": {
            "total_submissions": total_submissions,
            "average_green_score": round(avg_green_score, 2),
            "best_score": round(best_score, 2),
            "total_co2_saved": round(total_co2_saved, 3),
            "total_energy_saved": round(total_energy_saved, 3),
            "language_stats": language_stats
        },
        "recent_submissions": [
            {
                "id": s["id"],
                "filename": s.get("filename"),
                "language": s.get("language"),
                "green_score": s.get("green_score"),
                "created_at": s.get("created_at").isoformat() if s.get("created_at") else None
            }
            for s in submissions_sorted
        ]
    }


@router.get("/{project_id}/submissions")
async def get_project_submissions(
    project_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Get all submissions for a project"""
    project = await db["projects"].find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check access
    if project.get("team_id"):
        membership = await db["team_members"].find_one({
            "team_id": project["team_id"],
            "user_id": current_user.id
        })
        if not membership and project.get("created_by") != current_user.id and current_user.role.value != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
    elif project.get("created_by") != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    cursor = db["submissions"].find({"project_id": project_id}).sort("created_at", -1).limit(limit)
    submissions = await cursor.to_list(length=None)
    
    return [{k: v for k, v in s.items() if k != "_id"} for s in submissions]
