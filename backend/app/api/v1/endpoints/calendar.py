"""
Google Calendar integration endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/api/v1/calendar", tags=["calendar"])


@router.post("/sync")
async def sync_calendar(
    user_id: str = "test",  # TODO: Get from current user
    db: Session = Depends(get_db)
):
    """
    Sync extracted items with Google Calendar
    TODO: Implement Google Calendar sync
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google Calendar sync coming soon"
    )


@router.get("/events")
async def get_calendar_events(
    user_id: str = "test",  # TODO: Get from current user
    db: Session = Depends(get_db)
):
    """
    Get events from Google Calendar
    TODO: Implement Google Calendar API integration
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google Calendar integration coming soon"
    )
