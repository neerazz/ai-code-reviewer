"""
Repository model
"""
from sqlalchemy import Column, String, Integer, Boolean, JSON
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel


class Repository(BaseModel):
    """Repository model"""

    __tablename__ = "repositories"

    name = Column(String(255), nullable=False)
    full_name = Column(String(500), nullable=False, unique=True)  # owner/repo
    url = Column(String(500), nullable=False)

    # Platform
    platform = Column(String(50), nullable=False)  # github, gitlab
    external_id = Column(String(100), nullable=True)  # Platform-specific ID

    # Configuration
    is_active = Column(Boolean, default=True, nullable=False)
    auto_review_enabled = Column(Boolean, default=True, nullable=False)
    auto_comment_enabled = Column(Boolean, default=False, nullable=False)

    # Settings
    review_config = Column(JSON, nullable=True)  # Custom review settings

    # Statistics
    total_reviews = Column(Integer, default=0)
    total_issues_found = Column(Integer, default=0)

    # Relationships
    reviews = relationship("CodeReview", back_populates="repository", cascade="all, delete-orphan")
