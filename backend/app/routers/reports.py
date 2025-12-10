from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db
from ..schemas import User
from ..auth import get_current_active_user
from ..report_generator import report_generator
from ..logger import green_logger

router = APIRouter()


@router.get("/submission/{submission_id}/pdf")
async def download_submission_pdf(
    submission_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Download PDF report for a specific submission"""
    submission = await db["submissions"].find_one({
        "id": submission_id,
        "user_id": current_user.id
    })
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    if submission.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Submission analysis not completed")
    
    # Prepare submission data
    created_at = submission.get("created_at")
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    elif not isinstance(created_at, datetime):
        created_at = datetime.utcnow()
    
    submission_data = {
        "id": submission["id"],
        "filename": submission.get("filename") or "code.py",
        "language": submission.get("language"),
        "green_score": submission.get("green_score", 0) or 0,
        "energy_consumption_wh": submission.get("energy_consumption_wh", 0) or 0,
        "co2_emissions_g": submission.get("co2_emissions_g", 0) or 0,
        "cpu_time_ms": submission.get("cpu_time_ms", 0) or 0,
        "memory_usage_mb": submission.get("memory_usage_mb", 0) or 0,
        "complexity_score": submission.get("complexity_score", 0) or 0,
        "suggestions": submission.get("suggestions", []) or [],
        "real_world_impact": submission.get("analysis_results", {}).get("real_world_impact", {}) if submission.get("analysis_results") else {},
        "created_at": created_at.isoformat()
    }
    
    # Generate PDF
    user_data = {
        "username": current_user.username,
        "email": current_user.email
    }
    pdf_buffer = report_generator.generate_pdf_report(submission_data, user_data)
    
    # Log report generation
    green_logger.log_user_action(
        user_id=current_user.id,
        action="pdf_report_generated",
        details={"submission_id": submission_id}
    )
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=green-coding-report-{submission_id}.pdf"
        }
    )


@router.get("/submissions/csv")
async def download_submissions_csv(
    user_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Download CSV report for user submissions"""
    # Check authorization
    if user_id and user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    target_user_id = user_id or current_user.id
    
    # Get submissions
    cursor = db["submissions"].find({
        "user_id": target_user_id,
        "status": "completed"
    }).sort("created_at", -1)
    submissions = await cursor.to_list(length=None)
    
    # Prepare submission data
    submissions_data = []
    for submission in submissions:
        created_at = submission.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.utcnow()
        
        submissions_data.append({
            "id": submission["id"],
            "filename": submission.get("filename") or "code.py",
            "language": submission.get("language"),
            "green_score": submission.get("green_score", 0) or 0,
            "energy_consumption_wh": submission.get("energy_consumption_wh", 0) or 0,
            "co2_emissions_g": submission.get("co2_emissions_g", 0) or 0,
            "cpu_time_ms": submission.get("cpu_time_ms", 0) or 0,
            "memory_usage_mb": submission.get("memory_usage_mb", 0) or 0,
            "complexity_score": submission.get("complexity_score", 0) or 0,
            "created_at": created_at.isoformat()
        })
    
    # Generate CSV
    csv_buffer = report_generator.generate_csv_report(submissions_data)
    
    # Log report generation
    green_logger.log_user_action(
        user_id=current_user.id,
        action="csv_report_generated",
        details={"submissions_count": len(submissions_data)}
    )
    
    return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=green-coding-submissions-{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )


@router.get("/metrics/csv")
async def download_metrics_csv(
    user_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Download CSV report for user metrics"""
    # Check authorization
    if user_id and user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    target_user_id = user_id or current_user.id
    
    # Get metrics directly from database
    query_filter = {"status": "completed"}
    if target_user_id is not None:
        query_filter["user_id"] = target_user_id
    
    cursor = db["submissions"].find(query_filter)
    submissions = await cursor.to_list(length=None)
    
    # Calculate metrics
    total_submissions = len(submissions)
    green_scores = [s.get("green_score", 0) or 0 for s in submissions]
    avg_score = sum(green_scores) / total_submissions if total_submissions else 0
    total_co2 = sum(s.get("co2_emissions_g", 0) or 0 for s in submissions)
    total_energy = sum(s.get("energy_consumption_wh", 0) or 0 for s in submissions)
    
    # Get badge count
    badge_cursor = db["user_badges"].find({"user_id": target_user_id})
    badges = await badge_cursor.to_list(length=None)
    badge_count = len(badges) if target_user_id else 0
    
    metrics_data = {
        "average_green_score": round(avg_score, 2),
        "total_submissions": total_submissions,
        "total_co2_saved": round(total_co2, 3),
        "total_energy_saved": round(total_energy, 3),
        "badges_earned": badge_count,
    }
    
    # Generate CSV
    csv_buffer = report_generator.generate_user_metrics_csv(metrics_data)
    
    # Log report generation
    green_logger.log_user_action(
        user_id=current_user.id,
        action="metrics_csv_generated",
        details={"user_id": target_user_id}
    )
    
    return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=green-coding-metrics-{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )
