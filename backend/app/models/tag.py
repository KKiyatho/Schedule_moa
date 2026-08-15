"""
Tag model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Tag(Base):
    """Tag model - for categorizing schedule items"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Tag info
    name = Column(String(100), nullable=False)
    color = Column(String(7), default="#808080")  # Hex color code
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="tags")
    schedule_items = relationship("ScheduleItem", secondary="schedule_item_tag", back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name}, owner_id={self.owner_id})>"
