"""
Topics routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import Topic, Subtopic, TopicProgress, StudySession
from app.schemas import TopicResponse, TopicCreate, TopicUpdate, TopicProgressUpdate
from app.api.users import get_current_user

router = APIRouter()

@router.get("", response_model=List[TopicResponse])
async def get_topics(
    module_id: int = Query(None),
    status_filter: str = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get topics with optional filters"""
    
    query = db.query(Topic)
    
    if module_id:
        query = query.filter(Topic.module_id == module_id)
    
    if status_filter:
        query = query.filter(Topic.status == status_filter)
    
    topics = query.order_by(Topic.day_start).all()
    return topics

@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get topic by ID with subtopics"""
    
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    return topic

@router.put("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: int,
    topic_update: TopicUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update topic progress and details"""
    
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # Update allowed fields
    if topic_update.title is not None:
        topic.title = topic_update.title
    if topic_update.description is not None:
        topic.description = topic_update.description
    if topic_update.status is not None:
        topic.status = topic_update.status
        if topic_update.status in ["COMPLETED", "MASTERED"]:
            topic.progress = 100.0
    if topic_update.progress is not None:
        topic.progress = min(100.0, max(0.0, topic_update.progress))
    if topic_update.confidence is not None:
        topic.confidence = topic_update.confidence
    if topic_update.importance is not None:
        topic.importance = topic_update.importance
    if topic_update.estimated_hours is not None:
        topic.estimated_hours = topic_update.estimated_hours
    if topic_update.notes is not None:
        topic.notes = topic_update.notes
    
    topic.last_studied = datetime.utcnow()
    topic.updated_at = datetime.utcnow()
    
    db.add(topic)
    db.commit()
    db.refresh(topic)
    
    return topic

@router.post("/{topic_id}/subtopics", status_code=status.HTTP_201_CREATED)
async def add_subtopic(
    topic_id: int,
    subtopic_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Add a subtopic to a topic"""
    
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    subtopic = Subtopic(
        topic_id=topic_id,
        title=subtopic_data.get("title"),
        description=subtopic_data.get("description"),
        status="NOT_STARTED",
        progress=0.0,
        order=subtopic_data.get("order", len(topic.subtopics) + 1)
    )
    
    db.add(subtopic)
    db.commit()
    db.refresh(subtopic)
    
    return {
        "id": subtopic.id,
        "topic_id": subtopic.topic_id,
        "title": subtopic.title,
        "description": subtopic.description,
        "status": subtopic.status,
        "progress": subtopic.progress,
        "confidence": subtopic.confidence
    }

@router.get("/{topic_id}/subtopics", response_model=List[dict])
async def get_subtopics(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all subtopics for a topic"""
    
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    subtopics = db.query(Subtopic).filter(Subtopic.topic_id == topic_id).order_by(Subtopic.order).all()
    
    return [
        {
            "id": s.id,
            "topic_id": s.topic_id,
            "title": s.title,
            "description": s.description,
            "status": s.status,
            "progress": s.progress,
            "confidence": s.confidence,
            "order": s.order
        }
        for s in subtopics
    ]

@router.put("/subtopics/{subtopic_id}")
async def update_subtopic(
    subtopic_id: int,
    subtopic_update: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a subtopic"""
    
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtopic not found"
        )
    
    if "title" in subtopic_update:
        subtopic.title = subtopic_update["title"]
    if "description" in subtopic_update:
        subtopic.description = subtopic_update["description"]
    if "status" in subtopic_update:
        subtopic.status = subtopic_update["status"]
    if "progress" in subtopic_update:
        subtopic.progress = subtopic_update["progress"]
    if "confidence" in subtopic_update:
        subtopic.confidence = subtopic_update["confidence"]
    
    subtopic.updated_at = datetime.utcnow()
    db.add(subtopic)
    db.commit()
    db.refresh(subtopic)
    
    return {
        "id": subtopic.id,
        "topic_id": subtopic.topic_id,
        "title": subtopic.title,
        "description": subtopic.description,
        "status": subtopic.status,
        "progress": subtopic.progress,
        "confidence": subtopic.confidence
    }

@router.get("/{topic_id}/study-sessions", response_model=List[dict])
async def get_topic_study_sessions(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all study sessions for a topic"""
    
    sessions = db.query(StudySession).filter(
        StudySession.topic_id == topic_id,
        StudySession.user_id == current_user.id
    ).order_by(StudySession.date.desc()).all()
    
    return [
        {
            "id": s.id,
            "date": s.date,
            "duration_minutes": s.duration_minutes,
            "confidence_before": s.confidence_before,
            "confidence_after": s.confidence_after,
            "what_learned": s.what_learned
        }
        for s in sessions
    ]
