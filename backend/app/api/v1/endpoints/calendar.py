"""
Calendar management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas import (
    CalendarCreate,
    CalendarUpdate,
    CalendarResponse,
    CalendarWithItems
)
from app.crud import calendar as calendar_crud
from app.crud.user import get_user_by_id

router = APIRouter(prefix="/api/v1/calendars", tags=["calendars"])


@router.post("", response_model=CalendarResponse)
async def create_calendar(
    calendar_data: CalendarCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new calendar
    """
    user_id = int(current_user["user_id"])
    
    # Verify user exists
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db_calendar = calendar_crud.create_calendar(db, user_id, calendar_data)
    return CalendarResponse.model_validate(db_calendar)


@router.get("", response_model=List[CalendarResponse])
async def list_calendars(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all calendars for current user
    """
    user_id = int(current_user["user_id"])
    calendars, _ = calendar_crud.get_user_calendars(db, user_id, skip, limit)
    return [CalendarResponse.model_validate(cal) for cal in calendars]


@router.get("/{calendar_id}", response_model=CalendarWithItems)
async def get_calendar(
    calendar_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get calendar details with items
    """
    user_id = int(current_user["user_id"])
    calendar = calendar_crud.get_calendar_by_id(db, calendar_id)
    
    if not calendar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    
    if calendar.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this calendar")
    
    return CalendarWithItems.model_validate(calendar)


@router.put("/{calendar_id}", response_model=CalendarResponse)
async def update_calendar(
    calendar_id: int,
    calendar_update: CalendarUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a calendar
    """
    user_id = int(current_user["user_id"])
    calendar = calendar_crud.get_calendar_by_id(db, calendar_id)
    
    if not calendar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    
    if calendar.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this calendar")
    
    updated = calendar_crud.update_calendar(db, calendar_id, calendar_update)
    return CalendarResponse.model_validate(updated)


@router.delete("/{calendar_id}")
async def delete_calendar(
    calendar_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a calendar
    """
    user_id = int(current_user["user_id"])
    calendar = calendar_crud.get_calendar_by_id(db, calendar_id)
    
    if not calendar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    
    if calendar.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this calendar")
    
    calendar_crud.delete_calendar(db, calendar_id)
    return {"message": "Calendar deleted successfully"}


@router.post("/{calendar_id}/set-default", response_model=CalendarResponse)
async def set_default_calendar(
    calendar_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set calendar as default
    """
    user_id = int(current_user["user_id"])
    calendar = calendar_crud.get_calendar_by_id(db, calendar_id)
    
    if not calendar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    
    if calendar.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this calendar")
    
    updated = calendar_crud.update_calendar(
        db,
        calendar_id,
        CalendarUpdate(is_default=True)
    )
    return CalendarResponse.model_validate(updated)

