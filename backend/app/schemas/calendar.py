"""
Calendar schemas - Pydantic models for Calendar
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CalendarBase(BaseModel):
    """Base calendar schema"""
    name: str
    description: Optional[str] = None
    color: str = "#1f77b4"
    is_default: bool = False


class CalendarCreate(CalendarBase):
    """Schema for creating a calendar"""
    pass


class CalendarUpdate(BaseModel):
    """Schema for updating a calendar"""
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    is_default: Optional[bool] = None


class CalendarResponse(CalendarBase):
    """Schema for calendar response"""
    id: int
    owner_id: int
    is_synced_to_google: bool
    google_calendar_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CalendarWithItems(CalendarResponse):
    """Schema for calendar with schedule items"""
    from app.schemas.schedule_item import ScheduleItemResponse
    
    schedule_items: List[ScheduleItemResponse] = []

    class Config:
        from_attributes = True
