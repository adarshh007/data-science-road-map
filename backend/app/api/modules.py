"""
Modules routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Module, Topic
from app.schemas import ModuleResponse, ModuleCreate
from app.api.users import get_current_user

router = APIRouter()

@router.get("", response_model=List[ModuleResponse])
async def get_all_modules(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all modules"""
    modules = db.query(Module).order_by(Module.order).all()
    return modules

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get module by ID"""
    module = db.query(Module).filter(Module.id == module_id).first()
    
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    return module

@router.get("/{module_id}/progress")
async def get_module_progress(
    module_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get module progress for current user"""
    
    module = db.query(Module).filter(Module.id == module_id).first()
    
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    topics = db.query(Topic).filter(Topic.module_id == module_id).all()
    
    if not topics:
        return {
            "module_id": module_id,
            "module_name": module.title,
            "total_topics": 0,
            "completed_topics": 0,
            "progress": 0.0
        }
    
    # Calculate progress from topic statuses
    completed_count = sum(1 for t in topics if t.status in ["COMPLETED", "MASTERED"])
    total_count = len(topics)
    avg_progress = sum(t.progress for t in topics) / total_count if total_count > 0 else 0
    
    return {
        "module_id": module_id,
        "module_name": module.title,
        "total_topics": total_count,
        "completed_topics": completed_count,
        "progress": avg_progress
    }
