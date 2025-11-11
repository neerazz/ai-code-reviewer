"""
Code review endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.services.code_analyzer import code_analyzer
from backend.models.review import CodeReview, ReviewComment, ReviewStatus
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ReviewRequest(BaseModel):
    """Request model for code review"""
    code: str
    file_path: str
    language: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class PRReviewRequest(BaseModel):
    """Request model for PR review"""
    repository: str
    pr_number: int
    auto_comment: bool = False


@router.post("/analyze")
async def analyze_code(request: ReviewRequest):
    """
    Analyze a single file or code snippet

    Args:
        request: Review request with code and metadata

    Returns:
        Analysis results
    """
    try:
        result = await code_analyzer.analyze_file(
            file_path=request.file_path,
            content=request.code,
            context=request.context,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pr")
async def review_pull_request(request: PRReviewRequest, db: Session = Depends(get_db)):
    """
    Review a GitHub/GitLab pull request

    Args:
        request: PR review request
        db: Database session

    Returns:
        Review results
    """
    try:
        from backend.services.github_service import github_service

        # Get PR details
        pr_details = github_service.get_pull_request(
            request.repository,
            request.pr_number,
        )

        if not pr_details:
            raise HTTPException(status_code=404, detail="Pull request not found")

        # Get changed files
        files = github_service.get_pr_files(request.repository, request.pr_number)

        # Create review record
        review = CodeReview(
            repository_id=1,  # TODO: Get actual repository ID
            pr_number=request.pr_number,
            commit_sha=pr_details["head_sha"],
            branch_name=pr_details["head_branch"],
            status=ReviewStatus.IN_PROGRESS,
        )
        db.add(review)
        db.commit()

        # Analyze each file
        all_issues = []
        total_lines = 0

        for file in files[:10]:  # Limit to 10 files for now
            if file["status"] == "removed":
                continue

            # Get file content
            content = github_service.get_file_content(
                request.repository,
                file["filename"],
                pr_details["head_sha"],
            )

            if not content:
                continue

            # Analyze file
            analysis = await code_analyzer.analyze_file(
                file_path=file["filename"],
                content=content,
                context={"pr": pr_details},
            )

            total_lines += analysis.get("lines_of_code", 0)

            # Extract issues from LLM review
            llm_review = analysis.get("llm_review", {})
            issues = llm_review.get("issues", [])

            for issue in issues:
                comment = ReviewComment(
                    review_id=review.id,
                    file_path=file["filename"],
                    line_number=issue.get("line"),
                    severity=issue.get("severity", "info"),
                    category=issue.get("category", "general"),
                    title=issue.get("title", ""),
                    description=issue.get("description", ""),
                    suggestion=issue.get("suggestion"),
                    confidence_score=issue.get("confidence", 0.8),
                )
                db.add(comment)
                all_issues.append(issue)

        # Update review statistics
        review.status = ReviewStatus.COMPLETED
        review.total_issues = len(all_issues)
        review.files_analyzed = len(files)
        review.lines_of_code = total_lines
        review.critical_issues = len([i for i in all_issues if i.get("severity") == "critical"])
        review.warnings = len([i for i in all_issues if i.get("severity") == "warning"])

        db.commit()

        return {
            "success": True,
            "review_id": review.id,
            "pr_number": request.pr_number,
            "files_analyzed": len(files),
            "total_issues": len(all_issues),
            "issues": all_issues[:20],  # Return first 20 issues
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reviewing PR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{review_id}")
async def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get review details"""
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    comments = db.query(ReviewComment).filter(ReviewComment.review_id == review_id).all()

    return {
        "id": review.id,
        "status": review.status,
        "created_at": review.created_at.isoformat(),
        "total_issues": review.total_issues,
        "critical_issues": review.critical_issues,
        "warnings": review.warnings,
        "files_analyzed": review.files_analyzed,
        "lines_of_code": review.lines_of_code,
        "comments": [
            {
                "id": c.id,
                "file_path": c.file_path,
                "line_number": c.line_number,
                "severity": c.severity,
                "category": c.category,
                "title": c.title,
                "description": c.description,
                "suggestion": c.suggestion,
            }
            for c in comments
        ],
    }
