"""
Health check endpoints
"""
from fastapi import APIRouter
from backend.utils.cache import cache_service
from config.settings import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    redis_status = cache_service.ping()

    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {
            "redis": "up" if redis_status else "down",
            "llm_provider": settings.LLM_PROVIDER,
        },
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check for k8s"""
    redis_status = cache_service.ping()

    if not redis_status:
        return {"status": "not_ready", "reason": "redis unavailable"}, 503

    return {"status": "ready"}
