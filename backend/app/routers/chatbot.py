from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..mongo import get_mongo_db
from ..schemas import User
from ..schemas import ChatMessage, ChatResponse
from ..auth import get_current_active_user
from ..chatbot_service import green_chatbot
from ..logger import green_logger

router = APIRouter()


@router.post("/answer", response_model=ChatResponse)
async def answer_question(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    """Answer a question about green coding practices"""
    
    if not chat_message.message or not chat_message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Get answer from chatbot
    result = green_chatbot.answer(
        message=chat_message.message,
        context=chat_message.context
    )
    
    # Log the interaction
    green_logger.log_user_action(
        user_id=current_user.id,
        action="chatbot_question",
        details={
            "message": chat_message.message[:100],  # Truncate for logging
            "topics": result.get("related_topics", [])
        }
    )
    
    return ChatResponse(
        answer=result["answer"],
        suggestions=result.get("suggestions", []),
        related_topics=result.get("related_topics", [])
    )


@router.get("/suggestions")
def get_suggestions(
    topic: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get suggested questions based on topic"""
    
    suggestions = {
        "loop_optimization": [
            "How to optimize nested loops?",
            "When should I use list comprehensions?",
            "What's the difference between range(len()) and enumerate()?"
        ],
        "data_structures": [
            "Which data structure is most efficient?",
            "When to use sets vs lists?",
            "How to choose the right data structure?"
        ],
        "memory_usage": [
            "How to reduce memory usage?",
            "When to use generators?",
            "How to optimize memory in Python?"
        ],
        "algorithm_complexity": [
            "What is algorithm complexity?",
            "How to improve algorithm performance?",
            "What's the difference between O(n) and O(n²)?"
        ],
        "general": [
            "How to write efficient code?",
            "What are best practices for green coding?",
            "How to optimize my code?"
        ]
    }
    
    if topic and topic in suggestions:
        return {"suggestions": suggestions[topic]}
    
    # Return all suggestions
    all_suggestions = []
    for topic_suggestions in suggestions.values():
        all_suggestions.extend(topic_suggestions)
    
    return {"suggestions": all_suggestions[:10]}
