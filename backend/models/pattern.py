"""
Code pattern models for learning from team preferences
"""
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, Enum, JSON
from backend.models.base import BaseModel
import enum


class PatternCategory(str, enum.Enum):
    """Pattern categories"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    CODE_STYLE = "code_style"
    BEST_PRACTICE = "best_practice"
    ANTI_PATTERN = "anti_pattern"
    MIGRATION = "migration"


class Pattern(BaseModel):
    """Code pattern model - learned from team's code reviews"""

    __tablename__ = "patterns"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(PatternCategory), nullable=False)

    # Pattern matching
    language = Column(String(50), nullable=True)  # python, javascript, etc.
    regex_pattern = Column(Text, nullable=True)
    ast_pattern = Column(JSON, nullable=True)  # AST-based pattern

    # Detection
    severity = Column(String(50), nullable=False)  # info, warning, error, critical
    confidence_threshold = Column(Float, default=0.7)

    # Learning
    times_detected = Column(Integer, default=0)
    times_confirmed = Column(Integer, default=0)
    times_rejected = Column(Integer, default=0)

    # Suggestion
    suggestion_template = Column(Text, nullable=True)
    auto_fix_available = Column(Boolean, default=False)
    auto_fix_template = Column(Text, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    is_custom = Column(Boolean, default=False)  # User-defined vs built-in
    tags = Column(JSON, nullable=True)
