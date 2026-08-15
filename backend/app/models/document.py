"""
Document model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.db.base import Base


class DocumentStatus(str, Enum):
    """Status of document processing"""
    UPLOADED = "uploaded"          # Just uploaded
    PROCESSING = "processing"      # Being processed by AI
    COMPLETED = "completed"        # Processing complete
    FAILED = "failed"              # Processing failed


class DocumentType(str, Enum):
    """Type of document"""
    PDF = "pdf"
    IMAGE = "image"
    DOCUMENT = "document"  # docx, etc


class Document(Base):
    """Document model - represents uploaded files for extraction"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # File info
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False, unique=True)
    file_type = Column(SQLEnum(DocumentType), nullable=False)
    file_size = Column(Integer)  # in bytes
    
    # Processing
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.UPLOADED, nullable=False, index=True)
    processing_progress = Column(Integer, default=0)  # 0-100%
    
    # Extracted content
    extracted_text = Column(Text, nullable=True)
    extraction_method = Column(String(50), nullable=True)  # ocr, pdf_text, etc
    
    # AI processing
    ai_summary = Column(Text, nullable=True)
    ai_model_used = Column(String(100), nullable=True)  # gpt-4, etc
    
    # Metadata
    original_upload_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    schedule_items = relationship("ScheduleItem", back_populates="document")

    def __repr__(self):
        return f"<Document(id={self.id}, file_name={self.file_name}, status={self.status})>"
