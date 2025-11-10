from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import asyncio
from datetime import datetime

from ..database import get_db
from ..models import Submission, SubmissionStatus, User
from ..schemas import (
    SubmissionCreate, 
    SubmissionResponse, 
    AnalysisResponse,
    OptimizationSuggestion,
    CodeAnalysisRequest
)
from ..auth import get_current_active_user
from ..ml_predictor import green_predictor
from ..logger import green_logger

router = APIRouter()


@router.post("", response_model=SubmissionResponse)
async def create_submission(
    submission_data: SubmissionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit code for analysis"""
    
    # Create submission record
    db_submission = Submission(
        user_id=current_user.id,
        project_id=submission_data.project_id,
        code_content=submission_data.code_content,
        language=submission_data.language,
        filename=submission_data.filename,
        status=SubmissionStatus.PENDING
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    # Log submission
    green_logger.log_user_action(
        user_id=current_user.id,
        action="code_submitted",
        details={
            "submission_id": db_submission.id,
            "language": submission_data.language,
            "code_length": len(submission_data.code_content)
        }
    )
    
    # Start background analysis
    background_tasks.add_task(
        analyze_code_background,
        db_submission.id,
        submission_data.code_content,
        submission_data.language
    )
    
    return db_submission


@router.get("/{submission_id}", response_model=SubmissionResponse)
def get_submission(
    submission_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get submission analysis results"""
    
    submission = db.query(Submission).filter(
        Submission.id == submission_id,
        Submission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return submission


@router.post("/{submission_id}/analyze", response_model=AnalysisResponse)
async def analyze_submission(
    submission_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Manually trigger analysis for a submission"""
    
    submission = db.query(Submission).filter(
        Submission.id == submission_id,
        Submission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Perform analysis
    analysis_result = green_predictor.analyze_code(
        submission.code_content,
        submission.language
    )
    
    # Update submission with results
    submission.green_score = analysis_result["metrics"]["green_score"]
    submission.energy_consumption_wh = analysis_result["metrics"]["energy_consumption_wh"]
    submission.co2_emissions_g = analysis_result["metrics"]["co2_emissions_g"]
    submission.cpu_time_ms = analysis_result["metrics"]["cpu_time_ms"]
    submission.memory_usage_mb = analysis_result["metrics"]["memory_usage_mb"]
    submission.complexity_score = analysis_result["metrics"]["complexity_score"]
    submission.analysis_results = analysis_result["analysis_details"]
    submission.suggestions = analysis_result["suggestions"]
    submission.status = SubmissionStatus.COMPLETED
    submission.analyzed_at = datetime.utcnow()
    
    db.commit()
    
    # Log analysis completion
    green_logger.log_code_analysis(
        submission_id=submission.id,
        language=submission.language,
        metrics=analysis_result["metrics"]
    )
    
    return AnalysisResponse(
        green_score=analysis_result["metrics"]["green_score"],
        energy_consumption_wh=analysis_result["metrics"]["energy_consumption_wh"],
        co2_emissions_g=analysis_result["metrics"]["co2_emissions_g"],
        cpu_time_ms=analysis_result["metrics"]["cpu_time_ms"],
        memory_usage_mb=analysis_result["metrics"]["memory_usage_mb"],
        complexity_score=analysis_result["metrics"]["complexity_score"],
        suggestions=[
            OptimizationSuggestion(**suggestion) 
            for suggestion in analysis_result["suggestions"]
        ],
        analysis_details=analysis_result["analysis_details"]
    )


@router.post("/quick-analyze", response_model=AnalysisResponse)
async def quick_analyze(
    request: CodeAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Quick analysis without saving to database"""
    
    # Perform analysis
    analysis_result = green_predictor.analyze_code(
        request.code,
        request.language
    )
    
    # Log quick analysis
    green_logger.log_user_action(
        user_id=current_user.id,
        action="quick_analysis",
        details={
            "language": request.language,
            "code_length": len(request.code),
            "green_score": analysis_result["metrics"]["green_score"]
        }
    )
    
    return AnalysisResponse(
        green_score=analysis_result["metrics"]["green_score"],
        energy_consumption_wh=analysis_result["metrics"]["energy_consumption_wh"],
        co2_emissions_g=analysis_result["metrics"]["co2_emissions_g"],
        cpu_time_ms=analysis_result["metrics"]["cpu_time_ms"],
        memory_usage_mb=analysis_result["metrics"]["memory_usage_mb"],
        complexity_score=analysis_result["metrics"]["complexity_score"],
        suggestions=[
            OptimizationSuggestion(**suggestion) 
            for suggestion in analysis_result["suggestions"]
        ],
        analysis_details=analysis_result["analysis_details"]
    )


@router.get("/user/{user_id}/history")
def get_user_submission_history(
    user_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's submission history"""
    
    # Check if user can access this data
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    submissions = db.query(Submission).filter(
        Submission.user_id == user_id,
        Submission.status == SubmissionStatus.COMPLETED
    ).order_by(Submission.created_at.desc()).limit(limit).all()
    
    return submissions


@router.get("/user/{user_id}/stats")
def get_user_stats(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's coding statistics"""
    
    # Check if user can access this data
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    submissions = db.query(Submission).filter(
        Submission.user_id == user_id,
        Submission.status == SubmissionStatus.COMPLETED
    ).all()
    
    if not submissions:
        return {
            "total_submissions": 0,
            "average_green_score": 0,
            "total_co2_saved": 0,
            "total_energy_saved": 0,
            "best_score": 0,
            "improvement_trend": "No data"
        }
    
    # Calculate statistics
    total_submissions = len(submissions)
    average_green_score = sum(s.green_score for s in submissions) / total_submissions
    total_co2_saved = sum(s.co2_emissions_g for s in submissions)
    total_energy_saved = sum(s.energy_consumption_wh for s in submissions)
    best_score = max(s.green_score for s in submissions)
    
    # Calculate improvement trend
    recent_scores = [s.green_score for s in submissions[-10:]]
    if len(recent_scores) >= 2:
        trend = "improving" if recent_scores[-1] > recent_scores[0] else "declining"
    else:
        trend = "stable"
    
    return {
        "total_submissions": total_submissions,
        "average_green_score": round(average_green_score, 2),
        "total_co2_saved": round(total_co2_saved, 2),
        "total_energy_saved": round(total_energy_saved, 2),
        "best_score": best_score,
        "improvement_trend": trend
    }


@router.post("/analyze", response_model=AnalysisResponse)
async def public_analyze_code(request: CodeAnalysisRequest):
    """Public endpoint to analyze code without saving or authentication.
    Matches the frontend's /submissions/analyze usage.
    """
    analysis_result = green_predictor.analyze_code(request.code, request.language)
    return AnalysisResponse(
        green_score=analysis_result["metrics"]["green_score"],
        energy_consumption_wh=analysis_result["metrics"]["energy_consumption_wh"],
        co2_emissions_g=analysis_result["metrics"]["co2_emissions_g"],
        cpu_time_ms=analysis_result["metrics"]["cpu_time_ms"],
        memory_usage_mb=analysis_result["metrics"]["memory_usage_mb"],
        complexity_score=analysis_result["metrics"]["complexity_score"],
        suggestions=[
            OptimizationSuggestion(**suggestion)
            for suggestion in analysis_result["suggestions"]
        ],
        analysis_details=analysis_result["analysis_details"],
    )


async def analyze_code_background(submission_id: int, code: str, language: str):
    """Background task for code analysis"""
    
    try:
        # Perform analysis
        analysis_result = green_predictor.analyze_code(code, language)
        
        # Update database (this would need a separate database session)
        # For now, we'll just log the completion
        green_logger.logger.info(
            "background_analysis_completed",
            submission_id=submission_id,
            green_score=analysis_result["metrics"]["green_score"]
        )
        
    except Exception as e:
        green_logger.log_error(e, {"submission_id": submission_id})