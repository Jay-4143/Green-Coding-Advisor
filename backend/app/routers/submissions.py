from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Query
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime
from celery.result import AsyncResult

from ..mongo import get_mongo_db, get_next_sequence
from ..schemas import (
    SubmissionCreate, 
    SubmissionResponse, 
    AnalysisResponse,
    OptimizationSuggestion,
    CodeAnalysisRequest
)
from ..auth import get_current_active_user, get_optional_user
from ..schemas import User
from ..ml_predictor import green_predictor
from ..logger import green_logger
from ..badge_service import badge_service
from ..streak_service import streak_service
from ..security import (
    sanitize_code_content, validate_language, sanitize_filename,
    validate_pagination_params
)
from ..config import settings
from ..task_queue import analyze_submission_task, celery_app
from ..cache import (
    delete_cache,
    cache_key_user_metrics,
    cache_key_leaderboard,
    cache_key_user_badges,
)

router = APIRouter()

# Import shared rate limiter
from ..rate_limiter import limiter


@router.post("", response_model=SubmissionResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def create_submission(
    request: Request,
    submission_data: SubmissionCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_active_user),
    db=Depends(get_mongo_db),
):
    """Submit code for analysis (MongoDB)."""
    
    # Validate and sanitize input
    try:
        submission_data.code_content = sanitize_code_content(
            submission_data.code_content,
            max_length=1000000  # 1MB max
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not validate_language(submission_data.language):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid language. Allowed: python, java, javascript, typescript, cpp, c"
        )
    
    if submission_data.filename:
        try:
            submission_data.filename = sanitize_filename(submission_data.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    submission_id = await get_next_sequence(db, "submissions")
    now = datetime.utcnow()

    submission_doc: Dict[str, Any] = {
        "id": submission_id,
        "user_id": current_user.id,
        "project_id": submission_data.project_id,
        "code_content": submission_data.code_content,
        "language": submission_data.language,
        "filename": submission_data.filename,
        "status": "pending",
        "green_score": None,
        "energy_consumption_wh": None,
        "co2_emissions_g": None,
        "cpu_time_ms": None,
        "memory_usage_mb": None,
        "complexity_score": None,
        "analysis_results": None,
        "suggestions": None,
        "created_at": now,
        "analyzed_at": None,
    }

    await db["submissions"].insert_one(submission_doc)

    green_logger.log_user_action(
        user_id=current_user.id,
        action="code_submitted",
        details={
            "submission_id": submission_id,
            "language": submission_data.language,
            "code_length": len(submission_data.code_content),
        },
    )
    
    background_tasks.add_task(
        analyze_code_background,
        submission_id,
        submission_data.code_content,
        submission_data.language,
    )
    
    submission_doc.pop("_id", None)
    return SubmissionResponse.model_validate(submission_doc)


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: int,
    current_user=Depends(get_current_active_user),
    db=Depends(get_mongo_db),
):
    """Get submission analysis results"""
    
    submission = await db["submissions"].find_one(
        {"id": submission_id, "user_id": current_user.id}
    )
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    submission.pop("_id", None)
    return SubmissionResponse.model_validate(submission)


@router.post("/{submission_id}/analyze", response_model=AnalysisResponse)
async def analyze_submission(
    submission_id: int,
    current_user=Depends(get_current_active_user),
    db=Depends(get_mongo_db),
):
    """Manually trigger analysis for a submission"""
    
    submission = await db["submissions"].find_one(
        {"id": submission_id, "user_id": current_user.id}
    )
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    from ..config import settings

    analysis_result = green_predictor.analyze_code(
        submission["code_content"],
        submission["language"],
        region=getattr(settings, "codecarbon_region", "usa"),
    )
    
    metrics = analysis_result["metrics"]
    update_fields = {
        "green_score": metrics["green_score"],
        "energy_consumption_wh": metrics["energy_consumption_wh"],
        "co2_emissions_g": metrics["co2_emissions_g"],
        "cpu_time_ms": metrics["cpu_time_ms"],
        "memory_usage_mb": metrics["memory_usage_mb"],
        "complexity_score": metrics["complexity_score"],
        "analysis_results": analysis_result["analysis_details"],
        "suggestions": analysis_result["suggestions"],
        "status": "completed",
        "analyzed_at": datetime.utcnow(),
    }

    await db["submissions"].update_one(
        {"id": submission_id},
        {"$set": update_fields},
    )

    # Invalidate related caches
    try:
        await delete_cache(cache_key_user_metrics(current_user.id))
        await delete_cache(cache_key_leaderboard("week"))
        await delete_cache(cache_key_leaderboard("month"))
        await delete_cache(cache_key_leaderboard("all"))
        await delete_cache(cache_key_user_badges(current_user.id))
    except Exception:
        pass

    try:
        await streak_service.update_streak(current_user.id, db)
    except Exception as e:
        green_logger.logger.warning(f"Failed to update streak: {e}")
    
    try:
        newly_awarded = await badge_service.check_and_award_badges(
            current_user.id, db
        )
        if newly_awarded:
            green_logger.logger.info(
                f"User {current_user.id} earned {len(newly_awarded)} new badges"
            )
    except Exception as e:
        green_logger.logger.warning(f"Failed to check badges: {e}")
    
    green_logger.log_code_analysis(
        submission_id=submission_id,
        language=submission["language"],
        metrics=metrics,
    )
    
    return AnalysisResponse(
        green_score=metrics["green_score"],
        energy_consumption_wh=metrics["energy_consumption_wh"],
        co2_emissions_g=metrics["co2_emissions_g"],
        cpu_time_ms=metrics["cpu_time_ms"],
        memory_usage_mb=metrics["memory_usage_mb"],
        complexity_score=metrics["complexity_score"],
        suggestions=[OptimizationSuggestion(**s) for s in analysis_result["suggestions"]],
        analysis_details=analysis_result["analysis_details"],
    )


@router.post("/{submission_id}/analyze-async")
async def analyze_submission_async(
    submission_id: int,
    current_user=Depends(get_current_active_user),
    db=Depends(get_mongo_db),
):
    """Queue analysis in Celery and return task id."""
    submission = await db["submissions"].find_one(
        {"id": submission_id, "user_id": current_user.id}
    )
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    task = analyze_submission_task.apply_async(args=[submission_id])
    await db["submissions"].update_one(
        {"id": submission_id},
        {"$set": {"status": "queued", "analysis_task_id": task.id}},
    )
    return {"task_id": task.id, "status": "queued"}


@router.get("/tasks/{task_id}")
async def get_analysis_task_status(task_id: str):
    """Poll Celery task status."""
    result = AsyncResult(task_id, app=celery_app)
    payload = {"task_id": task_id, "status": result.status}
    if result.successful():
        payload["result"] = result.result
    elif result.failed():
        payload["error"] = str(result.result)
    return payload


@router.post("/quick-analyze", response_model=AnalysisResponse)
async def quick_analyze(
    request: CodeAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Quick analysis without saving to database"""
    
    # Perform analysis
    analysis_result = green_predictor.analyze_code(
        request.code,
        request.language,
        region=request.region or "usa"
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
async def get_user_submission_history(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_active_user),
    db=Depends(get_mongo_db),
):
    """Get user's submission history with pagination"""
    
    # Validate pagination
    skip, limit = validate_pagination_params(skip, limit)
    
    # Check if user can access this data
    role_value = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if current_user.id != user_id and role_value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get total count
    total = await db["submissions"].count_documents({"user_id": user_id, "status": "completed"})
    
    # Get paginated results
    cursor = (
        db["submissions"]
        .find({"user_id": user_id, "status": "completed"})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )
    submissions = await cursor.to_list(length=limit)
    for s in submissions:
        s.pop("_id", None)
    
    return {
        "items": submissions,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total
    }


@router.get("/user/{user_id}/stats")
async def get_user_stats(
    user_id: int,
    current_user=Depends(get_current_active_user),
    db=Depends(get_mongo_db),
):
    """Get user's coding statistics"""
    
    # Check if user can access this data
    role_value = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if current_user.id != user_id and role_value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    submissions = await db["submissions"].find(
        {"user_id": user_id, "status": "completed"}
    ).to_list(length=None)
    
    if not submissions:
        return {
            "total_submissions": 0,
            "average_green_score": 0,
            "total_co2_saved": 0,
            "total_energy_saved": 0,
            "best_score": 0,
            "improvement_trend": "No data"
        }
    
    total_submissions = len(submissions)
    average_green_score = sum(s.get("green_score") or 0 for s in submissions) / total_submissions
    total_co2_saved = sum(s.get("co2_emissions_g") or 0 for s in submissions)
    total_energy_saved = sum(s.get("energy_consumption_wh") or 0 for s in submissions)
    best_score = max(s.get("green_score") or 0 for s in submissions)
    
    # Calculate improvement trend
    recent_scores = [s.get("green_score") or 0 for s in submissions[-10:]]
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
    analysis_result = green_predictor.analyze_code(
        request.code, 
        request.language,
        region=request.region or "usa"
    )
    
    # Include real-world impact in analysis details
    analysis_details = analysis_result.get("analysis_details", {})
    real_world_impact = analysis_result.get("real_world_impact", {})
    analysis_details["real_world_impact"] = real_world_impact
    
    # Convert suggestions to OptimizationSuggestion objects
    suggestions_list = []
    for suggestion in analysis_result["suggestions"]:
        if isinstance(suggestion, dict):
            suggestions_list.append(OptimizationSuggestion(**suggestion))
        else:
            # If it's a string, create a simple suggestion object
            suggestions_list.append(OptimizationSuggestion(
                finding="Optimization opportunity",
                before_code="",
                after_code="",
                explanation=str(suggestion),
                predicted_improvement={},
                severity="medium"
            ))
    
    response = AnalysisResponse(
        green_score=analysis_result["metrics"]["green_score"],
        energy_consumption_wh=analysis_result["metrics"]["energy_consumption_wh"],
        co2_emissions_g=analysis_result["metrics"]["co2_emissions_g"],
        cpu_time_ms=analysis_result["metrics"]["cpu_time_ms"],
        memory_usage_mb=analysis_result["metrics"]["memory_usage_mb"],
        complexity_score=analysis_result["metrics"]["complexity_score"],
        suggestions=suggestions_list,
        analysis_details=analysis_details
    )
    
    # Add real_world_impact to response dict for frontend access
    response_dict = response.dict()
    response_dict["real_world_impact"] = real_world_impact
    return response_dict


@router.post("/optimize")
async def optimize_code(request: CodeAnalysisRequest):
    """Generate fully optimized code (not just suggestions).
    
    This endpoint:
    - Automatically detects the programming language
    - Analyzes the code for inefficiencies
    - Generates a FULL optimized version
    - Returns both original and optimized code with comparison metrics
    """
    try:
        # Validate and sanitize input
        code = sanitize_code_content(request.code, max_length=1000000)
        language = request.language if request.language else None
        
        # Generate optimized code
        optimization_result = green_predictor.optimize_code(
            code=code,
            language=language,
            region=request.region or "usa"
        )
        
        return optimization_result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")


@router.post("/optimize/report")
async def generate_optimization_report(
    request: CodeAnalysisRequest,
    format: str = Query("pdf", regex="^(pdf|json|html)$"),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Generate a comprehensive report from code optimization.
    
    This endpoint:
    - Optimizes the code
    - Generates a complete downloadable report
    - Supports PDF, JSON, and HTML formats
    """
    try:
        from fastapi.responses import Response, StreamingResponse
        from ..report_generator import report_generator
        
        # Validate and sanitize input
        code = sanitize_code_content(request.code, max_length=1000000)
        language = request.language if request.language else None
        
        # Generate optimized code
        optimization_result = green_predictor.optimize_code(
            code=code,
            language=language,
            region=request.region or "usa"
        )
        
        # Also analyze the original code for metrics
        analysis_result = green_predictor.analyze_code(
            code=code,
            language=optimization_result.get("detected_language", language or "python"),
            region=request.region or "usa"
        )
        
        # Prepare submission data
        submission_data = {
            "id": 0,  # No submission ID for direct optimization
            "filename": f"code.{optimization_result.get('detected_language', 'py')}",
            "language": optimization_result.get("detected_language", language or "python"),
            "code_content": code,
            "green_score": analysis_result["metrics"]["green_score"],
            "energy_consumption_wh": analysis_result["metrics"]["energy_consumption_wh"],
            "co2_emissions_g": analysis_result["metrics"]["co2_emissions_g"],
            "cpu_time_ms": analysis_result["metrics"]["cpu_time_ms"],
            "memory_usage_mb": analysis_result["metrics"]["memory_usage_mb"],
            "complexity_score": analysis_result["metrics"]["complexity_score"],
            "suggestions": analysis_result.get("suggestions", []),
            "real_world_impact": analysis_result.get("real_world_impact", {}),
            "created_at": datetime.utcnow().isoformat()
        }
        
        user_data = {
            "username": current_user.username if current_user else "Guest",
            "email": current_user.email if current_user else "guest@example.com"
        } if current_user else None
        
        # Generate report based on format
        if format == "pdf":
            pdf_buffer = report_generator.generate_comprehensive_pdf_report(
                submission_data,
                optimization_result,
                user_data,
                None
            )
            return StreamingResponse(
                pdf_buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=green-coding-optimization-report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                }
            )
        elif format == "json":
            json_report = report_generator.generate_json_report(
                submission_data,
                optimization_result,
                user_data,
                None
            )
            return Response(
                content=json_report,
                media_type="application/json",
                headers={
                    "Content-Disposition": f"attachment; filename=green-coding-optimization-report-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                }
            )
        elif format == "html":
            html_report = report_generator.generate_html_report(
                submission_data,
                optimization_result,
                user_data,
                None
            )
            return Response(
                content=html_report,
                media_type="text/html",
                headers={
                    "Content-Disposition": f"attachment; filename=green-coding-optimization-report-{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
                }
            )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


async def analyze_code_background(submission_id: int, code: str, language: str):
    """Background task for code analysis"""
    
    try:
        # Perform analysis
        from ..config import settings
        analysis_result = green_predictor.analyze_code(
            code, 
            language,
            region=getattr(settings, 'codecarbon_region', 'usa')
        )
        
        # Update database (this would need a separate database session)
        # For now, we'll just log the completion
        green_logger.logger.info(
            "background_analysis_completed",
            submission_id=submission_id,
            green_score=analysis_result["metrics"]["green_score"]
        )
        
    except Exception as e:
        green_logger.log_error(e, {"submission_id": submission_id})