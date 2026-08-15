"""
Document schemas - Pydantic models for Document
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from app.models.document import DocumentStatus, DocumentType

if TYPE_CHECKING:
    from app.schemas.schedule_item import ScheduleItemResponse


class DocumentBase(BaseModel):
    """Base document schema"""
    file_name: str


class DocumentCreate(DocumentBase):
    """Schema for creating a document (file upload)"""
    pass


class DocumentResponse(DocumentBase):
    """Schema for document response"""
    id: int
    owner_id: int
    file_type: DocumentType
    file_size: Optional[int] = None
    status: DocumentStatus
    processing_progress: int
    extracted_text: Optional[str] = None
    extraction_method: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_model_used: Optional[str] = None
    original_upload_time: datetime
    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentWithItems(DocumentResponse):
    """Schema for document with extracted items"""
    schedule_items: List = []

    class Config:
        from_attributes = True


class DocumentProcessingRequest(BaseModel):
    """Schema for requesting document processing"""
    calendar_id: int
    auto_create_items: bool = True


class DocumentProcessingResponse(BaseModel):
    """Schema for document processing response"""
    document_id: int
    status: DocumentStatus
    message: str
    processing_progress: int
