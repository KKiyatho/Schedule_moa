"""
Tag schemas - Pydantic models for Tag
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TagBase(BaseModel):
    """Base tag schema"""
    name: str
    color: str = "#808080"


class TagCreate(TagBase):
    """Schema for creating a tag"""
    pass


class TagUpdate(BaseModel):
    """Schema for updating a tag"""
    name: Optional[str] = None
    color: Optional[str] = None


class TagResponse(TagBase):
    """Schema for tag response"""
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
