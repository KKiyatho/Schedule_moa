"""
ScheduleItem model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.db.base import Base


# Association table for many-to-many relationship
schedule_item_tag = Table(
    'schedule_item_tag',
    Base.metadata,
    Column('schedule_item_id', Integer, ForeignKey('schedule_items.id', ondelete='CASCADE')),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'))
)


class ItemType(str, Enum):
    """Type of schedule item"""
    SCHEDULE = "schedule"      # 회의/일정
    DEADLINE = "deadline"      # 제출 마감
    TODO = "todo"              # 할 일


class ItemStatus(str, Enum):
    """Status of schedule item"""
    PENDING = "pending"        # 예정된 상태
    IN_PROGRESS = "in_progress" # 진행 중
    COMPLETED = "completed"    # 완료
    CANCELLED = "cancelled"    # 취소됨


class ScheduleItem(Base):
    """Schedule item model - unified item for schedule, deadline, and todo"""
    __tablename__ = "schedule_items"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False, index=True)
    
    # Basic info
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Type and Status
    type = Column(SQLEnum(ItemType), default=ItemType.TODO, nullable=False, index=True)
    status = Column(SQLEnum(ItemStatus), default=ItemStatus.PENDING, nullable=False, index=True)
    
    # Dates
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True, index=True)  # For deadline/todo
    
    # Priority
    priority = Column(Integer, default=3)  # 1 (high) - 5 (low)
    
    # Flags
    is_all_day = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)  # For future enhancement
    is_notified = Column(Boolean, default=False)
    
    # Source
    source = Column(String(50), default="manual")  # manual, auto (from document), google
    extracted_from_document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    
    # Google Calendar
    google_event_id = Column(String(255), unique=True, nullable=True, index=True)
    is_synced_to_google = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User", back_populates="schedule_items")
    calendar = relationship("Calendar", back_populates="schedule_items")
    tags = relationship("Tag", secondary=schedule_item_tag, back_populates="schedule_items")
    document = relationship("Document", back_populates="schedule_items")

    def __repr__(self):
        return f"<ScheduleItem(id={self.id}, title={self.title}, type={self.type})>"
