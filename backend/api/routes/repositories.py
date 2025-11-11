"""
Repository management endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.repository import Repository

router = APIRouter()


class RepositoryCreate(BaseModel):
    """Repository creation request"""
    name: str
    full_name: str
    url: str
    platform: str
    auto_review_enabled: bool = True


@router.post("/")
async def create_repository(repo: RepositoryCreate, db: Session = Depends(get_db)):
    """Create a new repository"""
    # Check if already exists
    existing = db.query(Repository).filter(Repository.full_name == repo.full_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Repository already exists")

    # Create repository
    new_repo = Repository(
        name=repo.name,
        full_name=repo.full_name,
        url=repo.url,
        platform=repo.platform,
        auto_review_enabled=repo.auto_review_enabled,
    )

    db.add(new_repo)
    db.commit()
    db.refresh(new_repo)

    return {
        "id": new_repo.id,
        "name": new_repo.name,
        "full_name": new_repo.full_name,
        "platform": new_repo.platform,
    }


@router.get("/")
async def list_repositories(db: Session = Depends(get_db)):
    """List all repositories"""
    repos = db.query(Repository).filter(Repository.is_active == True).all()

    return {
        "repositories": [
            {
                "id": r.id,
                "name": r.name,
                "full_name": r.full_name,
                "platform": r.platform,
                "total_reviews": r.total_reviews,
                "auto_review_enabled": r.auto_review_enabled,
            }
            for r in repos
        ]
    }


@router.get("/{repo_id}")
async def get_repository(repo_id: int, db: Session = Depends(get_db)):
    """Get repository details"""
    repo = db.query(Repository).filter(Repository.id == repo_id).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    return {
        "id": repo.id,
        "name": repo.name,
        "full_name": repo.full_name,
        "url": repo.url,
        "platform": repo.platform,
        "total_reviews": repo.total_reviews,
        "total_issues_found": repo.total_issues_found,
        "auto_review_enabled": repo.auto_review_enabled,
        "created_at": repo.created_at.isoformat(),
    }
