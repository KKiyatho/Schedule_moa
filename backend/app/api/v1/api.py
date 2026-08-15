"""
API v1 router
Combines all v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, documents, items, calendar
from app.core.config import settings

router = APIRouter(prefix="/api/v1")

# Health check endpoint for API v1
@router.get("/health")
async def health_check():
    """Health check endpoint for API v1"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "api_version": "v1"
    }

router.include_router(auth.router)
router.include_router(documents.router)
router.include_router(items.router)
router.include_router(calendar.router)
