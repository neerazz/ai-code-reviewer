"""
User model
"""
from sqlalchemy import Column, String, Boolean
from backend.models.base import BaseModel


class User(BaseModel):
    """User model"""

    __tablename__ = "users"

    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    full_name = Column(String(255), nullable=True)

    # Authentication
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # External accounts
    github_username = Column(String(255), nullable=True)
    gitlab_username = Column(String(255), nullable=True)
