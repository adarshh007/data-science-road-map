"""
Analytics routes
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models import StudySession, Topic, Module, StatusEnum
from app.schemas import AnalyticsOverviewResponse, StudyHoursOverTimeResponse
from app.api.users import get_current_user

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get overview analytics"""
    
    # Total study hours
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id
    ).all()
    
    total_study_minutes = sum(s.duration_minutes for s in sessions)
    total_study_hours = total_study_minutes / 60
    avg_session_duration = total_study_minutes / len(sessions) if sessions else 0
    
    # Get all topics
    all_topics = db.query(Topic).all()
    completed_topics = sum(1 for t in all_topics if t.status in ["COMPLETED", "MASTERED"])
    total_topics = len(all_topics)
    
    # Module progress
    modules = db.query(Module).order_by(Module.order).all()
    modules_progress = []
    
    for module in modules:
        module_topics = db.query(Topic).filter(Topic.module_id == module.id).all()
        if module_topics:
            completed = sum(1 for t in module_topics if t.status in ["COMPLETED", "MASTERED"])
            avg_progress = sum(t.progress for t in module_topics) / len(module_topics)
            modules_progress.append({
                "module_id": module.id,
                "module_name": module.title,
                "progress": round(avg_progress, 2),
                "completed_topics": completed,
                "total_topics": len(module_topics)
            })
    
    # Topic status distribution
    status_counts = {}
    for topic in all_topics:
        status = topic.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    topic_status_distribution = [
        {
            "status": status,
            "count": count
        }
        for status, count in status_counts.items()
    ]
    
    # Streaks
    streak_response = await get_streak_data(db, current_user.id)
    
    return {
        "total_study_hours": round(total_study_hours, 2),
        "average_session_duration": round(avg_session_duration, 1),
        "current_streak": streak_response["current_streak"],
        "longest_streak": streak_response["longest_streak"],
        "completed_topics": completed_topics,
        "total_topics": total_topics,
        "modules_progress": modules_progress,
        "topic_status_distribution": topic_status_distribution
    }

@router.get("/study-hours-over-time", response_model=List[StudyHoursOverTimeResponse])
async def get_study_hours_over_time(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get study hours over time (last N days)"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.date >= start_date
    ).all()
    
    # Group by date
    hours_by_date = {}
    for session in sessions:
        date_key = session.date.date().isoformat()
        if date_key not in hours_by_date:
            hours_by_date[date_key] = 0
        hours_by_date[date_key] += session.duration_minutes / 60
    
    # Sort by date
    result = [
        {
            "date": date,
            "hours": round(hours, 2)
        }
        for date, hours in sorted(hours_by_date.items())
    ]
    
    return result

@router.get("/study-hours-by-module")
async def get_study_hours_by_module(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get study hours breakdown by module"""
    
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id
    ).all()
    
    modules = db.query(Module).all()
    total_minutes_all = sum(s.duration_minutes for s in sessions)
    
    hours_by_module = {}
    for session in sessions:
        if session.module_id:
            if session.module_id not in hours_by_module:
                hours_by_module[session.module_id] = 0
            hours_by_module[session.module_id] += session.duration_minutes / 60
    
    result = []
    for module in modules:
        hours = hours_by_module.get(module.id, 0)
        percentage = (hours / (total_minutes_all / 60)) * 100 if total_minutes_all > 0 else 0
        result.append({
            "module_name": module.title,
            "hours": round(hours, 2),
            "percentage": round(percentage, 1)
        })
    
    return result

@router.get("/study-hours-by-topic")
async def get_study_hours_by_topic(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get top N topics by study hours"""
    
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id
    ).all()
    
    hours_by_topic = {}
    for session in sessions:
        if session.topic_id:
            if session.topic_id not in hours_by_topic:
                hours_by_topic[session.topic_id] = 0
            hours_by_topic[session.topic_id] += session.duration_minutes / 60
    
    # Get topic names and sort
    result = []
    for topic_id, hours in sorted(hours_by_topic.items(), key=lambda x: x[1], reverse=True)[:limit]:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if topic:
            result.append({
                "topic_name": topic.title,
                "hours": round(hours, 2)
            })
    
    return result

@router.get("/weekly-stats")
async def get_weekly_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get weekly study statistics"""
    
    start_date = datetime.utcnow() - timedelta(weeks=12)
    
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.date >= start_date
    ).all()
    
    # Group by week
    weeks_data = {}
    for session in sessions:
        week_start = session.date - timedelta(days=session.date.weekday())
        week_key = week_start.date().isoformat()
        
        if week_key not in weeks_data:
            weeks_data[week_key] = {"hours": 0, "sessions": 0}
        
        weeks_data[week_key]["hours"] += session.duration_minutes / 60
        weeks_data[week_key]["sessions"] += 1
    
    result = [
        {
            "week_start": week_key,
            "hours": round(data["hours"], 2),
            "sessions": data["sessions"]
        }
        for week_key, data in sorted(weeks_data.items())
    ]
    
    return result

async def get_streak_data(db: Session, user_id: int):
    """Helper function to calculate streaks"""
    
    sessions = db.query(StudySession).filter(
        StudySession.user_id == user_id
    ).order_by(StudySession.date.desc()).all()
    
    if not sessions:
        return {
            "current_streak": 0,
            "longest_streak": 0
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
        "longest_streak": longest_streak
    }
