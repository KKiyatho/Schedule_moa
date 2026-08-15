"""
ScheduleItem schemas - Pydantic models for ScheduleItem
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.schedule_item import ItemType, ItemStatus


class TagResponse(BaseModel):
    """Schema for tag response"""
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True


class ScheduleItemBase(BaseModel):
    """Base schedule item schema"""
    title: str
    description: Optional[str] = None
    type: ItemType = ItemType.TODO
    priority: int = 3  # 1-5
    is_all_day: bool = False


class ScheduleItemCreate(ScheduleItemBase):
    """Schema for creating a schedule item"""
    calendar_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    tag_ids: List[int] = []


class ScheduleItemUpdate(BaseModel):
    """Schema for updating a schedule item"""
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ItemType] = None
    status: Optional[ItemStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    is_all_day: Optional[bool] = None
    tag_ids: Optional[List[int]] = None


class ScheduleItemResponse(ScheduleItemBase):
    """Schema for schedule item response"""
    id: int
    creator_id: int
    calendar_id: int
    status: ItemStatus
    start_date: datetime
    end_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    source: str
    is_synced_to_google: bool
    google_event_id: Optional[str] = None
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScheduleItemListResponse(BaseModel):
    """Schema for list of schedule items with pagination"""
    total: int
    items: List[ScheduleItemResponse]
    page: int
    page_size: int


class ScheduleItemBulkCreate(BaseModel):
    """Schema for creating multiple schedule items (from document extraction)"""
    calendar_id: int
    document_id: Optional[int] = None
    items: List[ScheduleItemCreate]
