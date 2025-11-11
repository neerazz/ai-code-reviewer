"""
Code migration endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from backend.services.migration_engine import migration_engine
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class MigrationRequest(BaseModel):
    """Migration request model"""
    code: str
    migration_type: str
    language: str
    source_version: Optional[str] = None
    target_version: Optional[str] = None


class MigrationAnalysisRequest(BaseModel):
    """Migration analysis request"""
    files: List[Dict[str, str]]  # List of {path, content}
    migration_type: str


@router.post("/migrate")
async def migrate_code(request: MigrationRequest):
    """
    Migrate code from one framework/version to another

    Args:
        request: Migration request

    Returns:
        Migrated code and analysis
    """
    try:
        result = await migration_engine.migrate_code(
            code=request.code,
            migration_type=request.migration_type,
            language=request.language,
            source_version=request.source_version,
            target_version=request.target_version,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:
        logger.error(f"Error migrating code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze")
async def analyze_migration(request: MigrationAnalysisRequest):
    """
    Analyze migration scope for multiple files

    Args:
        request: Migration analysis request

    Returns:
        Migration scope and effort estimate
    """
    try:
        result = await migration_engine.analyze_migration_scope(
            files=request.files,
            migration_type=request.migration_type,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:
        logger.error(f"Error analyzing migration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def list_migration_templates():
    """List available migration templates"""
    templates = migration_engine.list_available_migrations()

    return {
        "templates": templates,
    }


@router.get("/templates/{migration_type}")
async def get_migration_template(migration_type: str):
    """Get specific migration template"""
    template = migration_engine.get_migration_template(migration_type)

    if not template:
        raise HTTPException(status_code=404, detail="Migration template not found")

    return template
