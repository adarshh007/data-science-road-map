"""
Study sessions routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models import StudySession, Topic
from app.schemas import StudySessionResponse, StudySessionCreate, StudySessionUpdate
from app.api.users import get_current_user

router = APIRouter()

@router.post("", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
async def create_study_session(
    session: StudySessionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new study session"""
    
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.id == session.topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # Calculate duration
    duration_minutes = int((session.end_time - session.start_time).total_seconds() / 60)
    
    if duration_minutes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    
    db_session = StudySession(
        user_id=current_user.id,
        module_id=session.module_id,
        topic_id=session.topic_id,
        date=session.date,
        start_time=session.start_time,
        end_time=session.end_time,
        duration_minutes=duration_minutes,
        what_learned=session.what_learned,
        what_practiced=session.what_practiced,
        difficulty=session.difficulty,
        confidence_before=session.confidence_before,
        confidence_after=session.confidence_after,
        notes=session.notes
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return db_session

@router.get("", response_model=List[StudySessionResponse])
async def get_study_sessions(
    topic_id: int = Query(None),
    module_id: int = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get study sessions for current user with optional filters"""
    
    query = db.query(StudySession).filter(StudySession.user_id == current_user.id)
    
    if topic_id:
        query = query.filter(StudySession.topic_id == topic_id)
    
    if module_id:
        query = query.filter(StudySession.module_id == module_id)
    
    if start_date:
        query = query.filter(StudySession.date >= start_date)
    
    if end_date:
        query = query.filter(StudySession.date <= end_date)
    
    sessions = query.order_by(StudySession.date.desc()).limit(limit).all()
    
    return sessions

@router.get("/{session_id}", response_model=StudySessionResponse)
async def get_study_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific study session"""
    
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found"
        )
    
    return session

@router.put("/{session_id}", response_model=StudySessionResponse)
async def update_study_session(
    session_id: int,
    session_update: StudySessionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a study session"""
    
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found"
        )
    
    if session_update.what_learned is not None:
        session.what_learned = session_update.what_learned
    if session_update.what_practiced is not None:
        session.what_practiced = session_update.what_practiced
    if session_update.difficulty is not None:
        session.difficulty = session_update.difficulty
    if session_update.confidence_before is not None:
        session.confidence_before = session_update.confidence_before
    if session_update.confidence_after is not None:
        session.confidence_after = session_update.confidence_after
    if session_update.notes is not None:
        session.notes = session_update.notes
    
    session.updated_at = datetime.utcnow()
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_study_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a study session"""
    
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found"
        )
    
    db.delete(session)
    db.commit()

@router.get("/stats/today")
async def get_today_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get study stats for today"""
    
    today = datetime.utcnow().date()
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        func.date(StudySession.date) == today
    ).all()
    
    total_minutes = sum(s.duration_minutes for s in sessions)
    total_hours = total_minutes / 60
    avg_confidence_before = (
        sum(s.confidence_before for s in sessions) / len(sessions)
        if sessions else 0
    )
    avg_confidence_after = (
        sum(s.confidence_after for s in sessions) / len(sessions)
        if sessions else 0
    )
    
    return {
        "date": today,
        "session_count": len(sessions),
        "total_minutes": total_minutes,
        "total_hours": round(total_hours, 2),
        "avg_confidence_before": round(avg_confidence_before, 1),
        "avg_confidence_after": round(avg_confidence_after, 1)
    }

@router.get("/stats/streak")
async def get_streak(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get current and longest study streak"""
    
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id
    ).order_by(StudySession.date.desc()).all()
    
    if not sessions:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "last_study_date": None
        }
    
    # Calculate streaks
    streak_dates = set()
    for session in sessions:
        streak_dates.add(session.date.date())
    
    sorted_dates = sorted(list(streak_dates), reverse=True)
    
    current_streak = 0
    expected_date = datetime.utcnow().date()
    
    for date in sorted_dates:
        if date == expected_date or (expected_date - date).days == 1:
            current_streak += 1
            expected_date = date
        else:
            break
    
    # Calculate longest streak
    if not sorted_dates:
        longest_streak = 0
    else:
        longest_streak = 1
        temp_streak = 1
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i-1] - sorted_dates[i]).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
    
    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_study_date": sorted_dates[0] if sorted_dates else None
    }
