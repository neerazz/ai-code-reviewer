"""
Webhook endpoints for GitHub/GitLab integration
"""
from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import hmac
import hashlib

from config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


def verify_github_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature"""
    if not settings.GITHUB_WEBHOOK_SECRET:
        return True  # Skip verification if secret not set

    expected = "sha256=" + hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None),
):
    """
    GitHub webhook handler

    Handles events:
    - pull_request (opened, synchronize)
    - push
    """
    # Get payload
    payload = await request.body()

    # Verify signature
    if x_hub_signature_256:
        if not verify_github_signature(payload, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse payload
    data = await request.json()

    logger.info(f"Received GitHub webhook: {x_github_event}")

    if x_github_event == "pull_request":
        action = data.get("action")

        if action in ["opened", "synchronize", "reopened"]:
            # Trigger code review
            pr = data.get("pull_request", {})
            repo = data.get("repository", {})

            logger.info(
                f"PR {action}: {repo.get('full_name')} #{pr.get('number')}"
            )

            # TODO: Trigger async review task
            # This would normally be done via Celery or similar

            return {
                "status": "accepted",
                "message": f"Review queued for PR #{pr.get('number')}",
            }

    elif x_github_event == "ping":
        return {"status": "ok", "message": "Webhook configured successfully"}

    return {"status": "ignored", "event": x_github_event}


@router.post("/gitlab")
async def gitlab_webhook(request: Request, x_gitlab_token: Optional[str] = Header(None)):
    """
    GitLab webhook handler

    Handles events:
    - merge_request
    - push
    """
    # Verify token
    if settings.GITLAB_WEBHOOK_SECRET and x_gitlab_token != settings.GITLAB_WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid token")

    data = await request.json()
    event_type = data.get("object_kind")

    logger.info(f"Received GitLab webhook: {event_type}")

    if event_type == "merge_request":
        action = data.get("object_attributes", {}).get("action")

        if action in ["open", "update", "reopen"]:
            mr = data.get("object_attributes", {})
            project = data.get("project", {})

            logger.info(
                f"MR {action}: {project.get('path_with_namespace')} !{mr.get('iid')}"
            )

            # TODO: Trigger async review task

            return {
                "status": "accepted",
                "message": f"Review queued for MR !{mr.get('iid')}",
            }

    return {"status": "ignored", "event": event_type}
