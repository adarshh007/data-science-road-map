"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Status and Confidence Enums for schemas
class StatusEnum(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    LEARNING = "LEARNING"
    PRACTICING = "PRACTICING"
    COMPLETED = "COMPLETED"
    MASTERED = "MASTERED"
    NEEDS_REVISION = "NEEDS_REVISION"

class ConfidenceEnum(int, Enum):
    DONT_KNOW = 0
    VERY_WEAK = 1
    WEAK = 2
    AVERAGE = 3
    GOOD = 4
    STRONG = 5

# ==================== Auth Schemas ====================
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    theme: Optional[str] = None
    daily_goal_hours: Optional[float] = None
    weekly_goal_hours: Optional[float] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    theme: str
    daily_goal_hours: float
    weekly_goal_hours: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ==================== Module Schemas ====================
class ModuleBase(BaseModel):
    number: int
    title: str
    description: Optional[str] = None
    total_days: int = 2
    order: Optional[int] = None

class ModuleCreate(ModuleBase):
    pass

class ModuleResponse(ModuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Day Schemas ====================
class DayBase(BaseModel):
    module_id: int
    day_number: int
    date: Optional[datetime] = None

class DayCreate(DayBase):
    pass

class DayResponse(DayBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Subtopic Schemas ====================
class SubtopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.NOT_STARTED
    progress: float = 0.0
    confidence: ConfidenceEnum = ConfidenceEnum.DONT_KNOW
    order: Optional[int] = None

class SubtopicCreate(SubtopicBase):
    pass

class SubtopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    progress: Optional[float] = None
    confidence: Optional[ConfidenceEnum] = None

class SubtopicResponse(SubtopicBase):
    id: int
    topic_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Topic Schemas ====================
class TopicBase(BaseModel):
    module_id: int
    day_start: int
    day_end: int
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.NOT_STARTED
    progress: float = 0.0
    confidence: ConfidenceEnum = ConfidenceEnum.DONT_KNOW
    importance: int = Field(3, ge=1, le=5)
    estimated_hours: float = 2.0

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    progress: Optional[float] = None
    confidence: Optional[ConfidenceEnum] = None
    importance: Optional[int] = None
    estimated_hours: Optional[float] = None
    notes: Optional[str] = None

class TopicProgressUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    progress: Optional[float] = None
    confidence: Optional[ConfidenceEnum] = None
    notes: Optional[str] = None

class TopicResponse(TopicBase):
    id: int
    day_id: Optional[int] = None
    actual_hours: float
    notes: Optional[str]
    last_studied: Optional[datetime]
    next_revision: Optional[datetime]
    revision_count: int
    created_at: datetime
    updated_at: datetime
    subtopics: List[SubtopicResponse] = []
    
    class Config:
        from_attributes = True

# ==================== Topic Progress Schemas ====================
class TopicProgressResponse(BaseModel):
    id: int
    user_id: int
    topic_id: int
    status: StatusEnum
    progress: float
    confidence: ConfidenceEnum
    total_hours: float
    last_studied: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Study Session Schemas ====================
class StudySessionBase(BaseModel):
    topic_id: int
    module_id: Optional[int] = None
    date: datetime
    start_time: datetime
    end_time: datetime
    what_learned: Optional[str] = None
    what_practiced: Optional[str] = None
    difficulty: int = Field(3, ge=1, le=5)
    confidence_before: ConfidenceEnum = ConfidenceEnum.DONT_KNOW
    confidence_after: ConfidenceEnum = ConfidenceEnum.DONT_KNOW
    notes: Optional[str] = None

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionUpdate(BaseModel):
    what_learned: Optional[str] = None
    what_practiced: Optional[str] = None
    difficulty: Optional[int] = None
    confidence_before: Optional[ConfidenceEnum] = None
    confidence_after: Optional[ConfidenceEnum] = None
    notes: Optional[str] = None

class StudySessionResponse(StudySessionBase):
    id: int
    user_id: int
    duration_minutes: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Revision Schemas ====================
class RevisionBase(BaseModel):
    topic_id: int
    due_date: datetime
    notes: Optional[str] = None

class RevisionCreate(RevisionBase):
    pass

class RevisionUpdate(BaseModel):
    completed_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    notes: Optional[str] = None

class RevisionResponse(RevisionBase):
    id: int
    user_id: int
    revision_number: int
    completed_date: Optional[datetime]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Note Schemas ====================
class NoteBase(BaseModel):
    title: str
    content: str
    topic_id: Optional[int] = None
    tags: Optional[str] = None
    is_pinned: bool = False

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    is_pinned: Optional[bool] = None

class NoteResponse(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Resource Schemas ====================
class ResourceBase(BaseModel):
    topic_id: int
    title: str
    url: Optional[str] = None
    resource_type: str  # YOUTUBE, DOCUMENTATION, etc.
    description: Optional[str] = None
    status: str = "NOT_STARTED"

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    resource_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ResourceResponse(ResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Project Schemas ====================
class ProjectTopicResponse(BaseModel):
    id: int
    topic_id: int
    is_completed: bool
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "PLANNING"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    technologies: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    progress: float = 0.0
    notes: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    technologies: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    progress: Optional[float] = None
    notes: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    project_topics: List[ProjectTopicResponse] = []
    
    class Config:
        from_attributes = True

# ==================== Achievement Schemas ====================
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class AchievementResponse(AchievementBase):
    id: int
    user_id: int
    earned_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Analytics Schemas ====================
class StudyHoursOverTimeResponse(BaseModel):
    date: str
    hours: float

class StudyHoursByModuleResponse(BaseModel):
    module_name: str
    hours: float
    percentage: float

class StudyHoursByTopicResponse(BaseModel):
    topic_name: str
    hours: float

class TopicStatusDistribution(BaseModel):
    status: StatusEnum
    count: int

class ModuleProgressResponse(BaseModel):
    module_id: int
    module_name: str
    progress: float
    completed_topics: int
    total_topics: int

class AnalyticsOverviewResponse(BaseModel):
    total_study_hours: float
    average_session_duration: float
    current_streak: int
    longest_streak: int
    completed_topics: int
    total_topics: int
    modules_progress: List[ModuleProgressResponse]
    topic_status_distribution: List[TopicStatusDistribution]

# ==================== Recommendation Schemas ====================
class TopicRecommendation(BaseModel):
    topic_id: int
    topic_name: str
    module_name: str
    priority: str  # HIGH, MEDIUM, LOW
    reason: str
    confidence_score: float

class RecommendationsResponse(BaseModel):
    recommendations: List[TopicRecommendation]
