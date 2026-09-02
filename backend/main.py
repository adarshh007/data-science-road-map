"""
DS Journey Backend - Main Application
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import routers and database
from app.database import engine, Base, get_db
from app.core.config import settings
from app.api import auth, users, modules, topics, study_sessions, analytics, recommendations, revisions

# Load environment variables
load_dotenv()

# Create database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified")
    yield
    # Shutdown
    print("Application shutting down")

# Initialize FastAPI app
app = FastAPI(
    title="DS Journey API",
    description="Backend API for DS Journey - Data Science Learning Tracker",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted hosts middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(modules.router, prefix="/api/modules", tags=["modules"])
app.include_router(topics.router, prefix="/api/topics", tags=["topics"])
app.include_router(study_sessions.router, prefix="/api/study-sessions", tags=["study_sessions"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(revisions.router, prefix="/api/revisions", tags=["revisions"])

@app.get("/")
async def root():
    return {
        "message": "DS Journey API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
