"""
Pydantic Schemas for API request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date, time
from uuid import UUID


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    pass


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    google_access_token: Optional[str] = None
    google_refresh_token: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Document Schemas ====================

class DocumentBase(BaseModel):
    """Base document schema"""
    file_name: str
    file_type: str  # pdf, image, text


class DocumentCreate(DocumentBase):
    """Document creation schema"""
    pass


class DocumentResponse(DocumentBase):
    """Document response schema"""
    id: UUID
    user_id: UUID
    status: str  # pending, extracted, classified
    extracted_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Extracted Item Schemas ====================

class ExtractedItemBase(BaseModel):
    """Base extracted item schema"""
    title: str
    description: Optional[str] = None
    item_type: str  # schedule, deadline, todo
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    location: Optional[str] = None
    priority: int = Field(default=3, ge=1, le=5)


class ExtractedItemCreate(ExtractedItemBase):
    """Item creation schema"""
    document_id: UUID


class ExtractedItemUpdate(BaseModel):
    """Item update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    item_type: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    location: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
    is_completed: Optional[bool] = None


class ExtractedItemResponse(ExtractedItemBase):
    """Item response schema"""
    id: UUID
    document_id: UUID
    user_id: UUID
    status: str
    google_event_id: Optional[str] = None
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== AI Response Schema ====================

class AIClassificationResponse(BaseModel):
    """AI classification response"""
    items: List[ExtractedItemCreate]
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    extracted_text: str


# ==================== Auth Schemas ====================

class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class GoogleAuthRequest(BaseModel):
    """Google auth request"""
    code: str
