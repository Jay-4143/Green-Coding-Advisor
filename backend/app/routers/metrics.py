from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from ..database import get_db
from ..models import Submission, SubmissionStatus, User
from ..schemas import MetricsHistory


router = APIRouter()


@router.get("/summary")
def summary(
    user_id: Optional[int] = Query(None, description="If provided, filter metrics by user id"),
    db: Session = Depends(get_db),
):
    """Return aggregate metrics computed from completed submissions."""

    query = db.query(Submission).filter(Submission.status == SubmissionStatus.COMPLETED)
    if user_id is not None:
        query = query.filter(Submission.user_id == user_id)

    submissions = query.all()
    if not submissions:
        return {
            "average_green_score": 0.0,
            "total_submissions": 0,
            "total_co2_saved": 0.0,
            "total_energy_saved": 0.0,
            "badges_earned": 0,
            "current_streak": 0,
        }

    total_submissions = len(submissions)
    green_scores = [s.green_score or 0 for s in submissions]
    avg_score = sum(green_scores) / total_submissions if total_submissions else 0
    total_co2 = sum(s.co2_emissions_g or 0 for s in submissions)
    total_energy = sum(s.energy_consumption_wh or 0 for s in submissions)

    return {
        "average_green_score": round(avg_score, 2),
        "total_submissions": total_submissions,
        "total_co2_saved": round(total_co2, 3),
        "total_energy_saved": round(total_energy, 3),
        "badges_earned": 0,
        "current_streak": 0,
    }


@router.get("/history")
def history(
    user_id: Optional[int] = Query(None, description="If provided, filter by user id"),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return chronological list of recent completed submissions for charting."""

    query = db.query(Submission).filter(Submission.status == SubmissionStatus.COMPLETED)
    if user_id is not None:
        query = query.filter(Submission.user_id == user_id)

    rows = (
        query.order_by(Submission.created_at.desc())
        .limit(limit)
        .all()
    )

    # Reverse to chronological order
    rows = list(reversed(rows))

    points = [
        {
            "date": (r.created_at or datetime.utcnow()).date().isoformat(),
            "greenScore": r.green_score or 0.0,
            "energyWh": r.energy_consumption_wh or 0.0,
            "co2g": r.co2_emissions_g or 0.0,
        }
        for r in rows
    ]

    # Simple aggregates for convenience
    avg_score = round(
        (sum(p["greenScore"] for p in points) / len(points)) if points else 0.0, 2
    )
    total_co2 = round(sum(p["co2g"] for p in points), 3)

    return {
        "points": points,
        "aggregates": {"avgScore": avg_score, "totalSavingsCo2g": total_co2},
    }


@router.get("/leaderboard")
def leaderboard(
    timeframe: str = Query("month", pattern="^(week|month|all)$"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return top users by average green score and totals.
    timeframe: week (7 days), month (30 days), all (no filter)
    """

    base_query = db.query(Submission, User).join(User, User.id == Submission.user_id).filter(
        Submission.status == SubmissionStatus.COMPLETED
    )

    if timeframe == "week":
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(days=7)
        base_query = base_query.filter(Submission.created_at >= since)
    elif timeframe == "month":
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(days=30)
        base_query = base_query.filter(Submission.created_at >= since)

    rows = base_query.all()
    if not rows:
        return {"entries": []}

    # Aggregate per user
    from collections import defaultdict
    agg = defaultdict(lambda: {
        "username": "",
        "green_scores": [],
        "submissions": 0,
        "carbon_saved": 0.0,
        "user_id": None,
    })

    for sub, user in rows:
        a = agg[user.id]
        a["username"] = user.username
        a["user_id"] = user.id
        a["submissions"] += 1
        a["green_scores"].append(sub.green_score or 0.0)
        a["carbon_saved"] += (sub.co2_emissions_g or 0.0)

    entries = []
    for user_id, a in agg.items():
        avg = sum(a["green_scores"]) / len(a["green_scores"]) if a["green_scores"] else 0.0
        entries.append({
            "username": a["username"],
            "greenScore": round(avg, 2),
            "carbonSaved": round(a["carbon_saved"], 3),
            "submissions": a["submissions"],
            "badges": [],
        })

    # Sort by greenScore desc, then submissions desc
    entries.sort(key=lambda e: (e["greenScore"], e["submissions"]), reverse=True)
    # Add rank
    for idx, e in enumerate(entries[:limit], start=1):
        e["rank"] = idx

    return {"entries": entries[:limit]}


