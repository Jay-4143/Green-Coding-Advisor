from fastapi import APIRouter


router = APIRouter()


@router.get("/{team_id}/dashboard")
def team_dashboard(team_id: str):
    return {
        "team": {"id": team_id, "name": "Team Demo"},
        "members": [],
        "aggregates": {"avgScore": 82},
        "leaderboard": [],
    }


