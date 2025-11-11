"""
Code migration models
"""
from sqlalchemy import Column, String, Text, Integer, Enum, JSON, Float
from backend.models.base import BaseModel
import enum


class MigrationStatus(str, enum.Enum):
    """Migration status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIALLY_COMPLETED = "partially_completed"


class MigrationType(str, enum.Enum):
    """Types of migrations"""
    FRAMEWORK_UPGRADE = "framework_upgrade"
    LANGUAGE_VERSION = "language_version"
    API_VERSION = "api_version"
    LIBRARY_REPLACEMENT = "library_replacement"
    PATTERN_REFACTOR = "pattern_refactor"


class Migration(BaseModel):
    """Code migration tracking"""

    __tablename__ = "migrations"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    migration_type = Column(Enum(MigrationType), nullable=False)
    status = Column(Enum(MigrationStatus), default=MigrationStatus.PENDING)

    # Source and target
    source_version = Column(String(100), nullable=True)
    target_version = Column(String(100), nullable=True)
    source_framework = Column(String(100), nullable=True)
    target_framework = Column(String(100), nullable=True)

    # Files
    total_files = Column(Integer, default=0)
    files_migrated = Column(Integer, default=0)
    files_failed = Column(Integer, default=0)

    # Statistics
    lines_changed = Column(Integer, default=0)
    success_rate = Column(Float, nullable=True)  # 0-1

    # Results
    migration_plan = Column(JSON, nullable=True)
    migration_results = Column(JSON, nullable=True)
    error_log = Column(Text, nullable=True)

    # Metadata
    repository_id = Column(Integer, nullable=True)
    branch_name = Column(String(255), nullable=True)
    metadata = Column(JSON, nullable=True)
