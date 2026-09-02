"""
Revisions routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Revision, Topic
from app.schemas import RevisionResponse, RevisionCreate, RevisionUpdate
from app.api.users import get_current_user

router = APIRouter()

@router.post("", response_model=RevisionResponse, status_code=status.HTTP_201_CREATED)
async def create_revision(
    revision: RevisionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a revision reminder"""
    
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.id == revision.topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    db_revision = Revision(
        user_id=current_user.id,
        topic_id=revision.topic_id,
        due_date=revision.due_date,
        revision_number=1,
        notes=revision.notes
    )
    
    db.add(db_revision)
    db.commit()
    db.refresh(db_revision)
    
    return db_revision

@router.get("/due", response_model=List[RevisionResponse])
async def get_revisions_due(
    status_filter: str = Query("pending"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get revisions due for current user"""
    
    query = db.query(Revision).filter(Revision.user_id == current_user.id)
    
    if status_filter == "pending":
        query = query.filter(Revision.is_completed == False)
    elif status_filter == "overdue":
        query = query.filter(
            and_(
                Revision.is_completed == False,
                Revision.due_date < datetime.utcnow()
            )
        )
    elif status_filter == "completed":
        query = query.filter(Revision.is_completed == True)
    
    revisions = query.order_by(Revision.due_date).all()
    
    return revisions

@router.get("", response_model=List[RevisionResponse])
async def get_all_revisions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all revisions for current user"""
    
    revisions = db.query(Revision).filter(
        Revision.user_id == current_user.id
    ).order_by(Revision.due_date).all()
    
    return revisions

@router.get("/{revision_id}", response_model=RevisionResponse)
async def get_revision(
    revision_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific revision"""
    
    revision = db.query(Revision).filter(
        and_(
            Revision.id == revision_id,
            Revision.user_id == current_user.id
        )
    ).first()
    
    if not revision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revision not found"
        )
    
    return revision

@router.put("/{revision_id}", response_model=RevisionResponse)
async def update_revision(
    revision_id: int,
    revision_update: RevisionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a revision"""
    
    revision = db.query(Revision).filter(
        and_(
            Revision.id == revision_id,
            Revision.user_id == current_user.id
        )
    ).first()
    
    if not revision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revision not found"
        )
    
    if revision_update.completed_date is not None:
        revision.completed_date = revision_update.completed_date
    
    if revision_update.is_completed is not None:
        revision.is_completed = revision_update.is_completed
        if revision_update.is_completed:
            revision.completed_date = datetime.utcnow()
    
    if revision_update.notes is not None:
        revision.notes = revision_update.notes
    
    revision.updated_at = datetime.utcnow()
    db.add(revision)
    db.commit()
    db.refresh(revision)
    
    return revision

@router.delete("/{revision_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_revision(
    revision_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a revision"""
    
    revision = db.query(Revision).filter(
        and_(
            Revision.id == revision_id,
            Revision.user_id == current_user.id
        )
    ).first()
    
    if not revision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revision not found"
        )
    
    db.delete(revision)
    db.commit()

@router.post("/{revision_id}/snooze")
async def snooze_revision(
    revision_id: int,
    days: int = Query(1, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Snooze a revision by N days"""
    
    revision = db.query(Revision).filter(
        and_(
            Revision.id == revision_id,
            Revision.user_id == current_user.id
        )
    ).first()
    
    if not revision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revision not found"
        )
    
    revision.due_date = datetime.utcnow() + timedelta(days=days)
    revision.updated_at = datetime.utcnow()
    
    db.add(revision)
    db.commit()
    db.refresh(revision)
    
    return {
        "message": f"Revision snoozed for {days} days",
        "new_due_date": revision.due_date
    }

@router.post("/schedule/{topic_id}")
async def schedule_revision(
    topic_id: int,
    days_until: int = Query(1, ge=1, le=60),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Schedule a revision for a topic"""
    
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # Check if revision already exists
    existing_revision = db.query(Revision).filter(
        and_(
            Revision.user_id == current_user.id,
            Revision.topic_id == topic_id,
            Revision.is_completed == False
        )
    ).first()
    
    if existing_revision:
        existing_revision.due_date = datetime.utcnow() + timedelta(days=days_until)
        db.add(existing_revision)
        db.commit()
        db.refresh(existing_revision)
        return existing_revision
    
    # Create new revision
    due_date = datetime.utcnow() + timedelta(days=days_until)
    
    db_revision = Revision(
        user_id=current_user.id,
        topic_id=topic_id,
        due_date=due_date,
        revision_number=topic.revision_count + 1
    )
    
    # Update topic revision count
    topic.revision_count += 1
    topic.next_revision = due_date
    
    db.add(db_revision)
    db.add(topic)
    db.commit()
    db.refresh(db_revision)
    
    return db_revision
