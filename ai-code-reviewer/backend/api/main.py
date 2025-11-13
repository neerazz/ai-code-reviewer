"""
AI Code Reviewer - FastAPI Application
Main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import review

# Application metadata
app = FastAPI(
    title="AI Code Reviewer",
    description="Intelligent code review system using AI and static analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - allows frontend to communicate with backend
origins = [
    "http://localhost:3000",
    "http://localhost:80",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(review.router, tags=["Code Review"])


@app.get("/", tags=["Health"])
def read_root():
    """
    Root endpoint - health check.

    Returns:
        dict: Welcome message and API status
    """
    return {
        "message": "AI Code Reviewer API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.

    Returns:
        dict: API health status
    """
    return {
        "status": "healthy",
        "service": "ai-code-reviewer"
    }
