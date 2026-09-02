"""
Database models for DS Journey
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class StatusEnum(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    LEARNING = "LEARNING"
    PRACTICING = "PRACTICING"
    COMPLETED = "COMPLETED"
    MASTERED = "MASTERED"
    NEEDS_REVISION = "NEEDS_REVISION"

class ConfidenceEnum(int, enum.Enum):
    DONT_KNOW = 0
    VERY_WEAK = 1
    WEAK = 2
    AVERAGE = 3
    GOOD = 4
    STRONG = 5

class ResourceTypeEnum(str, enum.Enum):
    YOUTUBE = "YOUTUBE"
    DOCUMENTATION = "DOCUMENTATION"
    COURSE = "COURSE"
    ARTICLE = "ARTICLE"
    BOOK = "BOOK"
    PRACTICE = "PRACTICE"
    GITHUB = "GITHUB"
    OTHER = "OTHER"

class ResourceStatusEnum(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class ProjectStatusEnum(str, enum.Enum):
    PLANNING = "PLANNING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"

# User and Authentication
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    theme = Column(String(20), default="system")  # system, light, dark
    daily_goal_hours = Column(Float, default=2.0)
    weekly_goal_hours = Column(Float, default=10.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    study_sessions = relationship("StudySession", back_populates="user", cascade="all, delete-orphan")
    revisions = relationship("Revision", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")
    topic_progress = relationship("TopicProgress", back_populates="user", cascade="all, delete-orphan")

# Course Structure
class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    total_days = Column(Integer, default=2)
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    days = relationship("Day", back_populates="module", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="module", cascade="all, delete-orphan")

class Day(Base):
    __tablename__ = "days"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    module = relationship("Module", back_populates="days")
    topics = relationship("Topic", back_populates="day")
    
    __table_args__ = (UniqueConstraint('module_id', 'day_number', name='uq_module_day'),)

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    day_id = Column(Integer, ForeignKey("days.id"))
    day_start = Column(Integer, nullable=False)  # e.g., 1 for days 1-2
    day_end = Column(Integer, nullable=False)    # e.g., 2 for days 1-2
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.NOT_STARTED)
    progress = Column(Float, default=0.0)  # 0-100
    confidence = Column(Integer, default=0)  # 0-5
    importance = Column(Integer, default=3)  # 1-5
    estimated_hours = Column(Float, default=2.0)
    actual_hours = Column(Float, default=0.0)
    notes = Column(Text)
    last_studied = Column(DateTime)
    next_revision = Column(DateTime)
    revision_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    module = relationship("Module", back_populates="topics")
    day = relationship("Day", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    progress_records = relationship("TopicProgress", back_populates="topic", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="topic", cascade="all, delete-orphan")
    revisions = relationship("Revision", back_populates="topic", cascade="all, delete-orphan")
    topic_notes = relationship("Note", back_populates="topic", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="topic", cascade="all, delete-orphan")
    project_topics = relationship("ProjectTopic", back_populates="topic", cascade="all, delete-orphan")

class Subtopic(Base):
    __tablename__ = "subtopics"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.NOT_STARTED)
    progress = Column(Float, default=0.0)
    confidence = Column(Integer, default=0)
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    topic = relationship("Topic", back_populates="subtopics")

# Progress Tracking
class TopicProgress(Base):
    __tablename__ = "topic_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.NOT_STARTED)
    progress = Column(Float, default=0.0)
    confidence = Column(Integer, default=0)
    total_hours = Column(Float, default=0.0)
    last_studied = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="topic_progress")
    topic = relationship("Topic", back_populates="progress_records")
    
    __table_args__ = (UniqueConstraint('user_id', 'topic_id', name='uq_user_topic'),)

# Study Sessions
class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    what_learned = Column(Text)
    what_practiced = Column(Text)
    difficulty = Column(Integer, default=3)  # 1-5
    confidence_before = Column(Integer, default=0)  # 0-5
    confidence_after = Column(Integer, default=0)  # 0-5
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    topic = relationship("Topic", back_populates="study_sessions")

# Revision System
class Revision(Base):
    __tablename__ = "revisions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    revision_number = Column(Integer, default=1)
    due_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="revisions")
    topic = relationship("Topic", back_populates="revisions")

# Notes
class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(500))  # Comma-separated
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="notes")
    topic = relationship("Topic", back_populates="topic_notes")

# Resources
class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(2000))
    resource_type = Column(SQLEnum(ResourceTypeEnum), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(ResourceStatusEnum), default=ResourceStatusEnum.NOT_STARTED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    topic = relationship("Topic", back_populates="resources")

# Projects
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(ProjectStatusEnum), default=ProjectStatusEnum.PLANNING)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    technologies = Column(String(500))  # Comma-separated
    github_url = Column(String(2000))
    demo_url = Column(String(2000))
    progress = Column(Float, default=0.0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    project_topics = relationship("ProjectTopic", back_populates="project", cascade="all, delete-orphan")

class ProjectTopic(Base):
    __tablename__ = "project_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="project_topics")
    topic = relationship("Topic", back_populates="project_topics")
    
    __table_args__ = (UniqueConstraint('project_id', 'topic_id', name='uq_project_topic'),)

# Achievements
class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    earned_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    
    __table_args__ = (UniqueConstraint('user_id', 'name', name='uq_user_achievement'),)
