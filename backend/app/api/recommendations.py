"""
Recommendations routes
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Topic, Module
from app.schemas import RecommendationsResponse
from app.api.users import get_current_user

router = APIRouter()

@router.get("", response_model=RecommendationsResponse)
async def get_recommendations(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get recommended topics to study next"""
    
    all_topics = db.query(Topic).all()
    
    # Filter out completed/mastered topics
    available_topics = [t for t in all_topics if t.status not in ["COMPLETED", "MASTERED"]]
    
    recommendations = []
    
    for topic in available_topics:
        # Calculate recommendation score
        score = calculate_recommendation_score(topic)
        
        # Determine priority
        if score > 0.8:
            priority = "HIGH"
        elif score > 0.5:
            priority = "MEDIUM"
        else:
            priority = "LOW"
        
        # Generate reason
        reason = generate_recommendation_reason(topic)
        
        module = db.query(Module).filter(Module.id == topic.module_id).first()
        
        recommendations.append({
            "topic_id": topic.id,
            "topic_name": topic.title,
            "module_name": module.title if module else "Unknown",
            "priority": priority,
            "reason": reason,
            "confidence_score": round(score, 2)
        })
    
    # Sort by confidence score (descending)
    recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
    
    return {
        "recommendations": recommendations[:limit]
    }

def calculate_recommendation_score(topic: Topic) -> float:
    """Calculate a recommendation score for a topic"""
    
    score = 0.0
    
    # Status factor (NOT_STARTED > LEARNING > PRACTICING)
    status_scores = {
        "NOT_STARTED": 0.4,
        "LEARNING": 0.3,
        "PRACTICING": 0.2,
        "COMPLETED": 0.0,
        "MASTERED": 0.0,
        "NEEDS_REVISION": 0.5
    }
    score += status_scores.get(topic.status, 0.2)
    
    # Importance factor
    score += (topic.importance / 5.0) * 0.3
    
    # Confidence factor (lower confidence = higher recommendation)
    score += ((5 - topic.confidence) / 5.0) * 0.2
    
    # Progress factor (partial progress = higher recommendation)
    if 0 < topic.progress < 100:
        score += 0.15
    
    return min(1.0, score)

def generate_recommendation_reason(topic: Topic) -> str:
    """Generate a human-readable reason for recommending a topic"""
    
    reasons = []
    
    if topic.status == "NEEDS_REVISION":
        reasons.append("Needs revision")
    elif topic.status == "NOT_STARTED":
        reasons.append("Not started yet")
    elif topic.status == "LEARNING":
        reasons.append("Currently learning")
    
    if topic.confidence <= 2:
        reasons.append("Low confidence")
    
    if topic.importance >= 4:
        reasons.append("High importance")
    
    if topic.progress > 0 and topic.progress < 100:
        reasons.append(f"{topic.progress:.0f}% progress")
    
    return " • ".join(reasons) if reasons else "Recommended for you"
