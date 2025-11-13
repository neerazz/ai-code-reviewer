"""
Pydantic schemas for code review API.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CodeSnippet(BaseModel):
    """Request schema for code review."""
    code: str = Field(..., description="Code snippet to review", min_length=1)
    language: Optional[str] = Field(None, description="Programming language (auto-detected if not provided)")
    context: Optional[str] = Field(None, description="Additional context for the review")


class ReviewResponse(BaseModel):
    """Response schema for code review."""
    review: str = Field(..., description="Comprehensive code review text")
    suggestions: List[str] = Field(..., description="List of actionable suggestions")
    quality_score: int = Field(..., description="Code quality score (0-100)", ge=0, le=100)
    language: str = Field(..., description="Detected or specified programming language")
    metrics: Dict[str, Any] = Field(..., description="Code metrics")
    issues_count: int = Field(..., description="Number of issues found", ge=0)
