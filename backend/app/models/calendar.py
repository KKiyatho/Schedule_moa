"""
Calendar model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Calendar(Base):
    """Calendar model - represents a user's calendar"""
    __tablename__ = "calendars"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Calendar info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), default="#1f77b4")  # Hex color code
    
    # Integration
    is_default = Column(Boolean, default=False)
    google_calendar_id = Column(String(255), unique=True, nullable=True, index=True)
    is_synced_to_google = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="calendars")
    schedule_items = relationship("ScheduleItem", back_populates="calendar", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Calendar(id={self.id}, name={self.name}, owner_id={self.owner_id})>"
