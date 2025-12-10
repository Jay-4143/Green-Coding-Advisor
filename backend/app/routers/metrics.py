from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from collections import defaultdict
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db
from ..schemas import MetricsHistory
from ..badge_service import badge_service
from ..streak_service import streak_service
from ..security import validate_pagination_params
from ..cache import (
    get_cache, set_cache, cache_key_user_metrics,
    cache_key_leaderboard
)

router = APIRouter()


@router.get("/summary")
async def summary(
    user_id: Optional[int] = Query(None, description="If provided, filter metrics by user id"),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    """Return aggregate metrics computed from completed submissions."""
    # Check cache first
    if user_id:
        cache_key = cache_key_user_metrics(user_id)
        cached = await get_cache(cache_key)
        if cached:
            return cached
    
    query_filter = {"status": "completed"}
    if user_id is not None:
        query_filter["user_id"] = user_id

    cursor = db["submissions"].find(query_filter)
    submissions = await cursor.to_list(length=None)
    
    # Get badge count and streak
    badge_count = 0
    current_streak = 0
    if user_id is not None:
        badge_cursor = db["user_badges"].find({"user_id": user_id})
        badges = await badge_cursor.to_list(length=None)
        badge_count = len(badges)
        streak_info = await streak_service.get_streak_info(user_id, db)
        current_streak = streak_info.get("current_streak", 0)
    
    if not submissions:
        return {
            "average_green_score": 0.0,
            "total_submissions": 0,
            "total_co2_saved": 0.0,
            "total_energy_saved": 0.0,
            "badges_earned": badge_count,
            "current_streak": current_streak,
        }

    total_submissions = len(submissions)
    green_scores = [s.get("green_score", 0) or 0 for s in submissions]
    avg_score = sum(green_scores) / total_submissions if total_submissions else 0
    total_co2 = sum(s.get("co2_emissions_g", 0) or 0 for s in submissions)
    total_energy = sum(s.get("energy_consumption_wh", 0) or 0 for s in submissions)

    result = {
        "average_green_score": round(avg_score, 2),
        "total_submissions": total_submissions,
        "total_co2_saved": round(total_co2, 3),
        "total_energy_saved": round(total_energy, 3),
        "badges_earned": badge_count,
        "current_streak": current_streak,
    }
    
    # Cache result for 5 minutes
    if user_id:
        await set_cache(cache_key_user_metrics(user_id), result, ttl=300)
    
    return result


@router.get("/history")
async def history(
    user_id: Optional[int] = Query(None, description="If provided, filter by user id"),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    """Return chronological list of recent completed submissions for charting."""

    query_filter = {"status": "completed"}
    if user_id is not None:
        query_filter["user_id"] = user_id

    cursor = db["submissions"].find(query_filter).sort("created_at", -1).limit(limit)
    rows = await cursor.to_list(length=None)

    # Reverse to chronological order
    rows = list(reversed(rows))

    points = []
    for r in rows:
        created_at = r.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.utcnow()
        
        points.append({
            "date": created_at.date().isoformat(),
            "greenScore": r.get("green_score", 0) or 0.0,
            "energyWh": r.get("energy_consumption_wh", 0) or 0.0,
            "co2g": r.get("co2_emissions_g", 0) or 0.0,
        })

    # Simple aggregates for convenience
    avg_score = round(
        (sum(p["greenScore"] for p in points) / len(points)) if points else 0.0, 2
    )
    total_co2 = round(sum(p["co2g"] for p in points), 3)

    return {
        "points": points,
        "aggregates": {"avgScore": avg_score, "totalSavingsCo2g": total_co2},
    }


@router.get("/language-stats")
async def language_stats(
    user_id: Optional[int] = Query(None, description="If provided, filter by user id"),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    """Get statistics per programming language"""
    query_filter = {"status": "completed"}
    if user_id is not None:
        query_filter["user_id"] = user_id

    cursor = db["submissions"].find(query_filter)
    submissions = await cursor.to_list(length=None)
    
    # Group by language
    language_data = defaultdict(lambda: {
        "count": 0,
        "total_green_score": 0.0,
        "total_co2": 0.0,
        "total_energy": 0.0,
        "submissions": []
    })
    
    for sub in submissions:
        lang = sub.get("language", "unknown")
        lang_data = language_data[lang]
        lang_data["count"] += 1
        lang_data["total_green_score"] += sub.get("green_score", 0) or 0
        lang_data["total_co2"] += sub.get("co2_emissions_g", 0) or 0
        lang_data["total_energy"] += sub.get("energy_consumption_wh", 0) or 0
        lang_data["submissions"].append(sub)
    
    # Calculate averages
    stats = []
    for lang, data in language_data.items():
        count = data["count"]
        stats.append({
            "language": lang,
            "submissions": count,
            "average_green_score": round(data["total_green_score"] / count if count > 0 else 0, 2),
            "total_co2_saved": round(data["total_co2"], 3),
            "total_energy_saved": round(data["total_energy"], 3),
            "average_co2_per_submission": round(data["total_co2"] / count if count > 0 else 0, 3),
            "average_energy_per_submission": round(data["total_energy"] / count if count > 0 else 0, 4)
        })
    
    # Sort by average green score descending
    stats.sort(key=lambda x: x["average_green_score"], reverse=True)
    
    return {"language_stats": stats}


@router.get("/carbon-timeline")
async def carbon_timeline(
    user_id: Optional[int] = Query(None, description="If provided, filter by user id"),
    days: int = Query(30, ge=7, le=365),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    """Get carbon emissions timeline for the last N days"""
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    query_filter = {
        "status": "completed",
        "created_at": {"$gte": start_date, "$lte": end_date}
    }
    if user_id is not None:
        query_filter["user_id"] = user_id
    
    cursor = db["submissions"].find(query_filter).sort("created_at", 1)
    submissions = await cursor.to_list(length=None)
    
    # Group by date
    daily_data = defaultdict(lambda: {
        "date": None,
        "co2_saved": 0.0,
        "energy_saved": 0.0,
        "submissions": 0,
        "average_green_score": 0.0
    })
    
    for sub in submissions:
        created_at = sub.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.utcnow()
        
        sub_date = created_at.date()
        date_str = sub_date.isoformat()
        
        daily_data[date_str]["date"] = date_str
        daily_data[date_str]["co2_saved"] += sub.get("co2_emissions_g", 0) or 0
        daily_data[date_str]["energy_saved"] += sub.get("energy_consumption_wh", 0) or 0
        daily_data[date_str]["submissions"] += 1
    
    # Calculate averages and create timeline
    timeline = []
    for date_str in sorted(daily_data.keys()):
        data = daily_data[date_str]
        if data["submissions"] > 0:
            # Calculate cumulative values
            timeline.append({
                "date": date_str,
                "co2_saved": round(data["co2_saved"], 3),
                "energy_saved": round(data["energy_saved"], 3),
                "submissions": data["submissions"],
                "average_green_score": 0.0  # Would need to calculate from submissions
            })
    
    # Calculate cumulative totals
    cumulative_co2 = 0.0
    cumulative_energy = 0.0
    for point in timeline:
        cumulative_co2 += point["co2_saved"]
        cumulative_energy += point["energy_saved"]
        point["cumulative_co2"] = round(cumulative_co2, 3)
        point["cumulative_energy"] = round(cumulative_energy, 3)
    
    return {
        "timeline": timeline,
        "total_days": days,
        "total_co2_saved": round(cumulative_co2, 3),
        "total_energy_saved": round(cumulative_energy, 3)
    }


@router.get("/leaderboard")
async def leaderboard(
    timeframe: str = Query("month", pattern="^(week|month|all)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    """Return top users by average green score and totals with pagination.
    timeframe: week (7 days), month (30 days), all (no filter)
    """
    # Validate pagination
    skip, limit = validate_pagination_params(skip, limit)

    # Check cache first (only for first page)
    if skip == 0:
        cache_key = cache_key_leaderboard(timeframe)
        cached = await get_cache(cache_key)
        if cached:
            # Return cached first page, apply pagination
            total = cached.get("total", 0)
            entries = cached.get("entries", [])[:limit]
            return {
                "entries": entries,
                "total": total,
                "skip": skip,
                "limit": limit,
                "has_more": limit < total
            }

    query_filter = {"status": "completed"}

    if timeframe == "week":
        since = datetime.utcnow() - timedelta(days=7)
        query_filter["created_at"] = {"$gte": since}
    elif timeframe == "month":
        since = datetime.utcnow() - timedelta(days=30)
        query_filter["created_at"] = {"$gte": since}

    cursor = db["submissions"].find(query_filter)
    rows = await cursor.to_list(length=None)

    if not rows:
        return {"entries": []}

    # Aggregate per user
    agg = defaultdict(lambda: {
        "username": "",
        "green_scores": [],
        "submissions": 0,
        "carbon_saved": 0.0,
        "user_id": None,
    })

    for sub in rows:
        user_id = sub.get("user_id")
        if not user_id:
            continue
            
        a = agg[user_id]
        if not a["user_id"]:
            user = await db["users"].find_one({"id": user_id})
            a["username"] = user.get("username", "Unknown") if user else "Unknown"
            a["user_id"] = user_id
        
        a["submissions"] += 1
        a["green_scores"].append(sub.get("green_score", 0) or 0.0)
        a["carbon_saved"] += (sub.get("co2_emissions_g", 0) or 0.0)

    entries = []
    for user_id, a in agg.items():
        avg = sum(a["green_scores"]) / len(a["green_scores"]) if a["green_scores"] else 0.0
        # Get user badges
        badge_cursor = db["user_badges"].find({"user_id": user_id})
        user_badges = await badge_cursor.to_list(length=None)
        
        badge_names = []
        for ub in user_badges:
            badge = await db["badges"].find_one({"id": ub.get("badge_id")})
            if badge:
                badge_names.append(badge.get("name"))
        
        entries.append({
            "username": a["username"],
            "greenScore": round(avg, 2),
            "carbonSaved": round(a["carbon_saved"], 3),
            "submissions": a["submissions"],
            "badges": badge_names,
        })

    # Sort by greenScore desc, then submissions desc
    entries.sort(key=lambda e: (e["greenScore"], e["submissions"]), reverse=True)
    
    # Get total count before pagination
    total = len(entries)
    
    # Apply pagination
    paginated_entries = entries[skip:skip + limit]
    
    # Add rank (based on skip offset)
    for idx, e in enumerate(paginated_entries, start=skip + 1):
        e["rank"] = idx

    result = {
        "entries": paginated_entries,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total
    }
    
    # Cache full leaderboard for 10 minutes (only first page)
    if skip == 0:
        await set_cache(
            cache_key_leaderboard(timeframe),
            {"entries": entries, "total": total},  # Cache all entries for pagination
            ttl=600
        )
    
    return result
