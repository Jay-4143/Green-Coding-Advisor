from fastapi import APIRouter


router = APIRouter()


@router.post("/answer")
def answer():
    return {"answer": "This loop is inefficient due to redundant indexing. Prefer iterating over items directly."}


