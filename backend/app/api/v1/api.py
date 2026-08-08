"""
API v1 router
Combines all v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, documents, items, calendar

router = APIRouter()

router.include_router(auth.router)
router.include_router(documents.router)
router.include_router(items.router)
router.include_router(calendar.router)
