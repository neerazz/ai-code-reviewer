"""
Code Review API Router
Handles code review requests and returns analysis results.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from api.schemas.review import CodeSnippet, ReviewResponse
from services.code_analyzer import get_code_analyzer
from services.llm_service import get_llm_service
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/review", response_model=ReviewResponse)
async def review_code(snippet: CodeSnippet) -> Dict[str, Any]:
    """
    Analyze and review code snippet.

    Args:
        snippet: Code snippet to review

    Returns:
        ReviewResponse: Comprehensive code review with suggestions

    Raises:
        HTTPException: If code analysis fails
    """
    try:
        if not snippet.code or not snippet.code.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code snippet cannot be empty"
            )

        logger.info(f"Reviewing code snippet ({len(snippet.code)} characters)")

        # Step 1: Static code analysis
        code_analyzer = get_code_analyzer()
        static_analysis = code_analyzer.analyze(snippet.code, snippet.language)

        logger.info(f"Detected language: {static_analysis['language']}")

        # Step 2: AI-powered analysis
        llm_service = get_llm_service()
        ai_analysis = llm_service.analyze_code(
            code=snippet.code,
            language=static_analysis['language'],
            context=snippet.context
        )

        # Step 3: Combine results
        combined_suggestions = []

        # Add static analysis issues as suggestions
        for issue in static_analysis.get('issues', []):
            severity_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(issue.get('severity', 'low'), '🔵')

            suggestion = f"{severity_emoji} {issue['issue']}: {issue['message']}"
            if 'line' in issue:
                suggestion += f" (Line {issue['line']})"
            combined_suggestions.append(suggestion)

        # Add AI suggestions
        if ai_analysis.get('suggestions'):
            combined_suggestions.extend(ai_analysis['suggestions'])

        # Build comprehensive review text
        review_parts = []

        # Add quality score
        quality_score = static_analysis.get('quality_score', 0)
        score_emoji = '🌟' if quality_score >= 80 else '⭐' if quality_score >= 60 else '💫'
        review_parts.append(f"{score_emoji} **Code Quality Score: {quality_score}/100**\n")

        # Add language info
        review_parts.append(f"**Language:** {static_analysis['language'].title()}\n")

        # Add metrics
        metrics = static_analysis.get('metrics', {})
        review_parts.append(f"**Metrics:**")
        review_parts.append(f"- Total lines: {metrics.get('total_lines', 0)}")
        review_parts.append(f"- Code lines: {metrics.get('code_lines', 0)}")
        review_parts.append(f"- Comment lines: {metrics.get('comment_lines', 0)}")
        review_parts.append(f"- Complexity: {static_analysis.get('complexity_score', 0)}/10\n")

        # Add AI review
        if ai_analysis.get('review'):
            review_parts.append(f"**AI Analysis:**\n{ai_analysis['review']}\n")

        # Add issue summary
        issues = static_analysis.get('issues', [])
        if issues:
            high_issues = len([i for i in issues if i.get('severity') == 'high'])
            medium_issues = len([i for i in issues if i.get('severity') == 'medium'])
            low_issues = len([i for i in issues if i.get('severity') == 'low'])

            review_parts.append(f"**Issues Found:** {len(issues)} total")
            if high_issues:
                review_parts.append(f"- 🔴 High: {high_issues}")
            if medium_issues:
                review_parts.append(f"- 🟡 Medium: {medium_issues}")
            if low_issues:
                review_parts.append(f"- 🟢 Low: {low_issues}")

        review_text = '\n'.join(review_parts)

        logger.info(f"Review completed. Quality score: {quality_score}")

        return {
            "review": review_text,
            "suggestions": combined_suggestions[:15],  # Limit to top 15
            "quality_score": quality_score,
            "language": static_analysis['language'],
            "metrics": metrics,
            "issues_count": len(issues)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reviewing code: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing code: {str(e)}"
        )
