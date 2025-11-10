from fastapi import APIRouter


router = APIRouter()


@router.post("")
def create_project():
    return {"project": {"id": "proj_demo", "name": "Demo"}}


@router.get("/{project_id}/summary")
def project_summary(project_id: str):
    return {"project": {"id": project_id}, "aggregates": {"avgScore": 80}}


