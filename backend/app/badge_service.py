from datetime import datetime
from typing import List, Dict, Any

from .mongo import get_next_sequence


class BadgeService:
    """Service for managing badge awarding and checking using MongoDB."""

    @staticmethod
    async def check_and_award_badges(user_id: int, db) -> List[Dict[str, Any]]:
        """Check all badge criteria for a user and award new badges."""
        user = await db["users"].find_one({"id": user_id})
        if not user:
            return []

        badges = await db["badges"].find({}).to_list(length=None)
        newly_awarded: List[Dict[str, Any]] = []

        for badge in badges:
            existing_badge = await db["user_badges"].find_one(
                {"user_id": user_id, "badge_id": badge["id"]}
            )
            if existing_badge:
                continue

            if await BadgeService._check_badge_criteria(user, badge, db):
                user_badge = {
                    "id": await get_next_sequence(db, "user_badges"),
                    "user_id": user_id,
                    "badge_id": badge["id"],
                    "earned_at": datetime.utcnow(),
                }
                await db["user_badges"].insert_one(user_badge)

                newly_awarded.append(
                    {
                        "id": badge["id"],
                        "name": badge["name"],
                        "description": badge.get("description"),
                        "icon": badge.get("icon"),
                        "points": badge.get("points", 0),
                        "earned_at": user_badge["earned_at"].isoformat(),
                    }
                )

        return newly_awarded

    @staticmethod
    async def _check_badge_criteria(user: Dict[str, Any], badge: Dict[str, Any], db) -> bool:
        """Check if user meets badge criteria."""
        criteria = badge.get("criteria") or {}
        if not criteria:
            return False

        criteria_type = criteria.get("type")

        submissions = await db["submissions"].find(
            {"user_id": user["id"], "status": "completed"}
        ).to_list(length=None)

        if criteria_type == "total_submissions":
            required_count = criteria.get("value", 0)
            return len(submissions) >= required_count

        if criteria_type == "average_green_score":
            if not submissions:
                return False
            avg_score = sum(s.get("green_score") or 0 for s in submissions) / len(
                submissions
            )
            required_score = criteria.get("value", 0)
            return avg_score >= required_score

        if criteria_type == "total_co2_saved":
            total_co2 = sum(s.get("co2_emissions_g") or 0 for s in submissions)
            required_co2 = criteria.get("value", 0)
            return total_co2 >= required_co2

        if criteria_type == "consecutive_high_scores":
            required_count = criteria.get("count", 0)
            min_score = criteria.get("min_score", 80)
            if len(submissions) < required_count:
                return False
            recent_submissions = sorted(
                submissions, key=lambda x: x.get("created_at"), reverse=True
            )[:required_count]
            return all(
                (s.get("green_score") or 0) >= min_score for s in recent_submissions
            )

        if criteria_type == "first_submission":
            return len(submissions) >= 1

        if criteria_type == "carbon_saver":
            total_co2 = sum(s.get("co2_emissions_g") or 0 for s in submissions)
            required_co2 = criteria.get("value", 0)
            return total_co2 >= required_co2

        if criteria_type == "efficient_coder":
            if not submissions:
                return False
            avg_score = sum(s.get("green_score") or 0 for s in submissions) / len(
                submissions
            )
            min_avg_score = criteria.get("min_avg_score", 85)
            min_submissions = criteria.get("min_submissions", 10)
            return len(submissions) >= min_submissions and avg_score >= min_avg_score

        if criteria_type == "eco_champion":
            total_co2 = sum(s.get("co2_emissions_g") or 0 for s in submissions)
            min_co2 = criteria.get("min_co2", 100)
            min_submissions = criteria.get("min_submissions", 50)
            return len(submissions) >= min_submissions and total_co2 >= min_co2

        return False

    @staticmethod
    async def get_user_badges(user_id: int, db) -> List[Dict[str, Any]]:
        """Get all badges earned by a user."""
        user_badges = await db["user_badges"].find({"user_id": user_id}).to_list(
            length=None
        )
        if not user_badges:
            return []

        badge_ids = [ub["badge_id"] for ub in user_badges]
        badges = await db["badges"].find({"id": {"$in": badge_ids}}).to_list(
            length=None
        )
        badge_by_id = {b["id"]: b for b in badges}

        result: List[Dict[str, Any]] = []
        for ub in user_badges:
            badge = badge_by_id.get(ub["badge_id"])
            if not badge:
                continue
            result.append(
                {
                    "id": badge["id"],
                    "name": badge["name"],
                    "description": badge.get("description"),
                    "icon": badge.get("icon"),
                    "points": badge.get("points", 0),
                    "earned_at": ub.get("earned_at").isoformat()
                    if ub.get("earned_at")
                    else None,
                }
            )

        return result

    @staticmethod
    async def get_all_badges(db) -> List[Dict[str, Any]]:
        """Get all available badges."""
        badges = await db["badges"].find({}).to_list(length=None)
        # Auto-initialize defaults if collection is empty (safety net)
        if not badges:
            await BadgeService.initialize_default_badges(db)
            badges = await db["badges"].find({}).to_list(length=None)
        return [
            {
                "id": b["id"],
                "name": b["name"],
                "description": b.get("description"),
                "icon": b.get("icon"),
                "points": b.get("points", 0),
                "criteria": b.get("criteria") or {},
            }
            for b in badges
        ]

    @staticmethod
    async def initialize_default_badges(db):
        """Initialize default badges in the database."""
        default_badges = [
            {
                "name": "First Steps",
                "description": "Submit your first code for analysis",
                "icon": "🌱",
                "points": 10,
                "criteria": {"type": "first_submission", "value": 1},
            },
            {
                "name": "Carbon Saver",
                "description": "Save 50g of CO2 through optimized code",
                "icon": "🌍",
                "points": 25,
                "criteria": {"type": "carbon_saver", "value": 50},
            },
            {
                "name": "Efficient Coder",
                "description": "Maintain an average green score of 85+ with 10+ submissions",
                "icon": "⚡",
                "points": 50,
                "criteria": {
                    "type": "efficient_coder",
                    "min_avg_score": 85,
                    "min_submissions": 10,
                },
            },
            {
                "name": "Eco-Friendly Champion",
                "description": "Save 100g+ CO2 with 50+ submissions",
                "icon": "🏆",
                "points": 100,
                "criteria": {
                    "type": "eco_champion",
                    "min_co2": 100,
                    "min_submissions": 50,
                },
            },
            {
                "name": "Green Master",
                "description": "Achieve 5 consecutive submissions with 90+ green score",
                "icon": "⭐",
                "points": 75,
                "criteria": {
                    "type": "consecutive_high_scores",
                    "count": 5,
                    "min_score": 90,
                },
            },
            {
                "name": "Code Analyzer",
                "description": "Submit 25 pieces of code for analysis",
                "icon": "📊",
                "points": 30,
                "criteria": {"type": "total_submissions", "value": 25},
            },
            {
                "name": "Sustainability Expert",
                "description": "Maintain an average green score of 80+",
                "icon": "🌿",
                "points": 40,
                "criteria": {"type": "average_green_score", "value": 80},
            },
            {
                "name": "Carbon Hero",
                "description": "Save 500g of CO2 through optimized code",
                "icon": "🦸",
                "points": 150,
                "criteria": {"type": "total_co2_saved", "value": 500},
            },
            {
                "name": "Loop Optimizer",
                "description": "Eliminate inefficient nested loops in 5+ submissions",
                "icon": "🔁",
                "points": 35,
                "criteria": {"type": "total_submissions", "value": 5},
            },
            {
                "name": "Memory Saver",
                "description": "Reduce memory usage across 10 submissions",
                "icon": "💾",
                "points": 45,
                "criteria": {"type": "total_submissions", "value": 10},
            },
            {
                "name": "Async Champion",
                "description": "Use async/batching patterns in 5 submissions",
                "icon": "⚙️",
                "points": 55,
                "criteria": {"type": "total_submissions", "value": 5},
            },
        ]

        for badge_data in default_badges:
            existing_badge = await db["badges"].find_one(
                {"name": badge_data["name"]}
            )
            if existing_badge:
                continue

            badge_doc = {
                "id": await get_next_sequence(db, "badges"),
                "name": badge_data["name"],
                "description": badge_data["description"],
                "icon": badge_data["icon"],
                "points": badge_data["points"],
                "criteria": badge_data["criteria"],
                "created_at": datetime.utcnow(),
            }
            await db["badges"].insert_one(badge_doc)


badge_service = BadgeService()


