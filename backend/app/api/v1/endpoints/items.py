"""
Schedule Items endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas import (
    ScheduleItemCreate,
    ScheduleItemUpdate,
    ScheduleItemResponse,
    ScheduleItemListResponse
)
from app.crud import item as item_crud
from app.crud.user import get_user_by_id

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.post("", response_model=ScheduleItemResponse)
async def create_item(
    item_data: ScheduleItemCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new schedule item
    """
    user_id = int(current_user["user_id"])
    
    # Verify user exists
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Verify calendar belongs to user
    from app.crud import calendar as calendar_crud
    calendar = calendar_crud.get_calendar_by_id(db, item_data.calendar_id)
    if not calendar or calendar.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Calendar not found or not owned by user")
    
    db_item = item_crud.create_schedule_item(db, item_data.calendar_id, user_id, item_data)
    return ScheduleItemResponse.model_validate(db_item)


@router.get("/{item_id}", response_model=ScheduleItemResponse)
async def get_item(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a schedule item by ID
    """
    user_id = int(current_user["user_id"])
    item = item_crud.get_schedule_item_by_id(db, item_id)
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if item.creator_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this item")
    
    return ScheduleItemResponse.model_validate(item)


@router.get("/calendar/{calendar_id}", response_model=ScheduleItemListResponse)
async def get_calendar_items(
    calendar_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all schedule items for a calendar
    """
    user_id = int(current_user["user_id"])
    
    # Verify calendar belongs to user
    from app.crud import calendar as calendar_crud
    calendar = calendar_crud.get_calendar_by_id(db, calendar_id)
    if not calendar or calendar.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Calendar not found or not owned by user")
    
    items, total = item_crud.get_schedule_items_by_calendar(db, calendar_id, skip, limit)
    
    return ScheduleItemListResponse(
        total=total,
        items=[ScheduleItemResponse.model_validate(item) for item in items],
        page=skip // limit + 1,
        page_size=limit
    )


@router.put("/{item_id}", response_model=ScheduleItemResponse)
async def update_item(
    item_id: int,
    item_update: ScheduleItemUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a schedule item
    """
    user_id = int(current_user["user_id"])
    
    # Verify item exists and belongs to user
    item = item_crud.get_schedule_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if item.creator_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this item")
    
    updated_item = item_crud.update_schedule_item(db, item_id, item_update)
    return ScheduleItemResponse.model_validate(updated_item)


@router.post("/{item_id}/complete", response_model=ScheduleItemResponse)
async def mark_complete(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark item as completed
    """
    user_id = int(current_user["user_id"])
    
    # Verify item exists and belongs to user
    item = item_crud.get_schedule_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if item.creator_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this item")
    
    completed_item = item_crud.mark_item_complete(db, item_id)
    return ScheduleItemResponse.model_validate(completed_item)


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a schedule item
    """
    user_id = int(current_user["user_id"])
    
    # Verify item exists and belongs to user
    item = item_crud.get_schedule_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if item.creator_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item")
    
    item_crud.delete_schedule_item(db, item_id)
    return {"message": "Item deleted successfully"}
    
    return {"message": "Item deleted successfully"}
