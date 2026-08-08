"""
Extracted items (schedule, deadline, todo) endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date, time
from typing import Optional

from app.db.session import get_db
from app.schemas import ExtractedItemResponse, ExtractedItemCreate, ExtractedItemUpdate
from app.crud.item import (
    get_item_by_id,
    get_user_items,
    create_item,
    update_item,
    mark_item_completed,
    delete_item
)

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.get("/", response_model=list[ExtractedItemResponse])
async def list_items(
    user_id: str = "test",  # TODO: Get from current user
    item_type: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all items for current user
    Optionally filter by type (schedule, deadline, todo) or status
    """
    items = get_user_items(db, UUID(user_id), status=status, skip=skip, limit=limit)
    
    if item_type:
        items = [item for item in items if item.item_type == item_type]
    
    return [ExtractedItemResponse.model_validate(item) for item in items]


@router.get("/{item_id}", response_model=ExtractedItemResponse)
async def get_item(
    item_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific item by ID
    """
    item = get_item_by_id(db, UUID(item_id))
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    return ExtractedItemResponse.model_validate(item)


@router.post("/", response_model=ExtractedItemResponse)
async def create_extracted_item(
    item_data: ExtractedItemCreate,
    user_id: str = "test",  # TODO: Get from current user
    db: Session = Depends(get_db)
):
    """
    Create a new extracted item
    """
    db_item = create_item(
        db=db,
        user_id=UUID(user_id),
        document_id=item_data.document_id,
        title=item_data.title,
        item_type=item_data.item_type,
        description=item_data.description,
        due_date=item_data.due_date,
        due_time=item_data.due_time,
        location=item_data.location,
        priority=item_data.priority
    )
    
    return ExtractedItemResponse.model_validate(db_item)


@router.put("/{item_id}", response_model=ExtractedItemResponse)
async def update_extracted_item(
    item_id: str,
    item_update: ExtractedItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an extracted item
    """
    item = get_item_by_id(db, UUID(item_id))
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    updated_item = update_item(db, UUID(item_id), item_update)
    
    return ExtractedItemResponse.model_validate(updated_item)


@router.post("/{item_id}/complete")
async def complete_item(
    item_id: str,
    db: Session = Depends(get_db)
):
    """
    Mark an item as completed
    """
    item = get_item_by_id(db, UUID(item_id))
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    completed_item = mark_item_completed(db, UUID(item_id))
    
    return ExtractedItemResponse.model_validate(completed_item)


@router.delete("/{item_id}")
async def delete_extracted_item(
    item_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an item
    """
    item = get_item_by_id(db, UUID(item_id))
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    delete_item(db, UUID(item_id))
    
    return {"message": "Item deleted successfully"}
