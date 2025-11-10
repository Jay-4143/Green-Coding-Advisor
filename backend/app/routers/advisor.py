from fastapi import APIRouter


router = APIRouter()


@router.post("/quick-check")
def quick_check():
    return {"hints": [{"message": "Consider list comprehension.", "severity": "info"}]}


@router.post("/inline-suggest")
def inline_suggest():
    return {
        "suggestions": [
            {
                "before": "for i in range(len(a)): ...",
                "after": "for item in a: ...",
                "rationale": "Avoid index-based iteration when possible.",
                "predictedDelta": {"greenScore": 4},
            }
        ]
    }


