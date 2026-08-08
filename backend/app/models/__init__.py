"""
SQLAlchemy Models for Database Tables
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.base import Base


class User(Base):
    """User Model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    google_access_token = Column(String, nullable=True)
    google_refresh_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    extracted_items = relationship("ExtractedItem", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Document(Base):
    """Uploaded Document Model"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, image, text
    extracted_text = Column(Text, nullable=True)
    status = Column(String, default="pending", nullable=False)  # pending, extracted, classified
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="documents")
    extracted_items = relationship("ExtractedItem", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document(id={self.id}, file_name={self.file_name})>"


class ExtractedItem(Base):
    """Extracted Schedule/Deadline/Todo Item"""
    __tablename__ = "extracted_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    item_type = Column(String, nullable=False)  # schedule, deadline, todo
    due_date = Column(Date, nullable=True)
    due_time = Column(Time, nullable=True)
    location = Column(String, nullable=True)
    priority = Column(Integer, default=3)  # 1-5 (1=낮음, 5=높음)
    
    status = Column(String, default="pending", nullable=False)  # pending, confirmed, synced
    google_event_id = Column(String, nullable=True, unique=True)
    
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="extracted_items")
    user = relationship("User", back_populates="extracted_items")

    def __repr__(self):
        return f"<ExtractedItem(id={self.id}, title={self.title}, type={self.item_type})>"
