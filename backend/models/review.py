"""
Code Review models
"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Enum, JSON, Float
from sqlalchemy.orm import relationship
import enum
from backend.models.base import BaseModel


class ReviewStatus(str, enum.Enum):
    """Review status enum"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ReviewSeverity(str, enum.Enum):
    """Review comment severity"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class CodeReview(BaseModel):
    """Code review model"""

    __tablename__ = "code_reviews"

    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    pr_number = Column(Integer, nullable=True)
    commit_sha = Column(String(40), nullable=True)
    branch_name = Column(String(255), nullable=True)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)

    # Analysis results
    total_issues = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    warnings = Column(Integer, default=0)
    suggestions = Column(Integer, default=0)

    # Metrics
    code_quality_score = Column(Float, nullable=True)  # 0-100
    security_score = Column(Float, nullable=True)  # 0-100
    performance_score = Column(Float, nullable=True)  # 0-100

    # Metadata
    files_analyzed = Column(Integer, default=0)
    lines_of_code = Column(Integer, default=0)
    analysis_duration_ms = Column(Integer, nullable=True)

    # Additional data
    metadata = Column(JSON, nullable=True)

    # Relationships
    repository = relationship("Repository", back_populates="reviews")
    comments = relationship("ReviewComment", back_populates="review", cascade="all, delete-orphan")


class ReviewComment(BaseModel):
    """Individual review comment/finding"""

    __tablename__ = "review_comments"

    review_id = Column(Integer, ForeignKey("code_reviews.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    line_number = Column(Integer, nullable=True)
    line_end = Column(Integer, nullable=True)

    # Issue details
    severity = Column(Enum(ReviewSeverity), default=ReviewSeverity.INFO, nullable=False)
    category = Column(String(100), nullable=False)  # security, performance, style, etc.
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # Code context
    code_snippet = Column(Text, nullable=True)
    suggestion = Column(Text, nullable=True)  # Suggested fix

    # Pattern matching
    pattern_id = Column(Integer, ForeignKey("patterns.id"), nullable=True)
    confidence_score = Column(Float, nullable=True)  # 0-1

    # GitHub/GitLab integration
    external_comment_id = Column(String(100), nullable=True)

    # Additional data
    metadata = Column(JSON, nullable=True)

    # Relationships
    review = relationship("CodeReview", back_populates="comments")
    pattern = relationship("Pattern")
