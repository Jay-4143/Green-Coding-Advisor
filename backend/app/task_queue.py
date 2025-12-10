"""
Celery task queue for offloading heavy code analysis.

Broker/backend: Redis (configured via REDIS_URL).
"""
import os
import asyncio
from typing import Any, Dict

from celery import Celery
from pymongo import MongoClient

from .config import settings
from .ml_predictor import green_predictor


REDIS_URL = os.getenv("REDIS_URL", settings.redis_url)
celery_app = Celery(
    "green_coding_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
)


def _get_sync_db():
    client = MongoClient(settings.mongodb_uri)
    return client[settings.mongodb_db]


@celery_app.task(name="analyze_submission")
def analyze_submission_task(submission_id: int) -> Dict[str, Any]:
    """
    Analyze a submission in the background and persist results to MongoDB.
    Returns metrics for quick polling.
    """
    db = _get_sync_db()
    submission = db["submissions"].find_one({"id": submission_id})
    if not submission:
        return {"error": "submission not found", "id": submission_id}

    result = green_predictor.analyze_code(
        submission.get("code_content", ""),
        submission.get("language", "python"),
        region=submission.get("region") or getattr(settings, "codecarbon_region", "usa"),
    )

    metrics = result["metrics"]
    update_fields = {
        "green_score": metrics["green_score"],
        "energy_consumption_wh": metrics["energy_consumption_wh"],
        "co2_emissions_g": metrics["co2_emissions_g"],
        "cpu_time_ms": metrics["cpu_time_ms"],
        "memory_usage_mb": metrics["memory_usage_mb"],
        "complexity_score": metrics["complexity_score"],
        "analysis_results": result["analysis_details"],
        "suggestions": result["suggestions"],
        "status": "completed",
    }
    db["submissions"].update_one({"id": submission_id}, {"$set": update_fields})
    return {"id": submission_id, **metrics}

