"""
CRUD operations for ScheduleItem
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Optional
from app.models import ScheduleItem, Tag
from app.models.schedule_item import ItemType, ItemStatus
from app.schemas import ScheduleItemCreate, ScheduleItemUpdate


def get_schedule_item_by_id(db: Session, item_id: int) -> ScheduleItem:
    """Get schedule item by ID"""
    return db.query(ScheduleItem).filter(ScheduleItem.id == item_id).first()


def get_schedule_items_by_calendar(
    db: Session, 
    calendar_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[ItemStatus] = None,
    item_type: Optional[ItemType] = None
) -> tuple[List[ScheduleItem], int]:
    """Get schedule items by calendar with pagination"""
    query = db.query(ScheduleItem).filter(ScheduleItem.calendar_id == calendar_id)
    
    if status:
        query = query.filter(ScheduleItem.status == status)
    if item_type:
        query = query.filter(ScheduleItem.type == item_type)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return items, total


def get_schedule_items_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[ScheduleItem], int]:
    """Get all schedule items for a user"""
    query = db.query(ScheduleItem).filter(ScheduleItem.creator_id == user_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_upcoming_items(
    db: Session,
    user_id: int,
    days: int = 7
) -> List[ScheduleItem]:
    """Get upcoming items in the next N days"""
    from datetime import timedelta
    now = datetime.utcnow()
    end_date = now + timedelta(days=days)
    
    return db.query(ScheduleItem).filter(
        and_(
            ScheduleItem.creator_id == user_id,
            ScheduleItem.start_date >= now,
            ScheduleItem.start_date <= end_date,
            ScheduleItem.status != ItemStatus.COMPLETED
        )
    ).order_by(ScheduleItem.start_date).all()


def get_overdue_items(db: Session, user_id: int) -> List[ScheduleItem]:
    """Get overdue items"""
    now = datetime.utcnow()
    return db.query(ScheduleItem).filter(
        and_(
            ScheduleItem.creator_id == user_id,
            ScheduleItem.due_date < now,
            ScheduleItem.status != ItemStatus.COMPLETED
        )
    ).order_by(ScheduleItem.due_date).all()


def create_schedule_item(
    db: Session,
    calendar_id: int,
    creator_id: int,
    item_data: ScheduleItemCreate
) -> ScheduleItem:
    """Create a new schedule item"""
    db_item = ScheduleItem(
        calendar_id=calendar_id,
        creator_id=creator_id,
        title=item_data.title,
        description=item_data.description,
        type=item_data.type,
        status=ItemStatus.PENDING,
        priority=item_data.priority,
        is_all_day=item_data.is_all_day,
        start_date=item_data.start_date,
        end_date=item_data.end_date,
        due_date=item_data.due_date,
        source="manual"
    )
    
    # Add tags if provided
    if item_data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(item_data.tag_ids)).all()
        db_item.tags = tags
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_schedule_item(
    db: Session,
    item_id: int,
    item_update: ScheduleItemUpdate
) -> ScheduleItem:
    """Update a schedule item"""
    db_item = get_schedule_item_by_id(db, item_id)
    if not db_item:
        return None
    
    update_data = item_update.dict(exclude_unset=True)
    
    # Handle tags separately
    tag_ids = update_data.pop("tag_ids", None)
    
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    if tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        db_item.tags = tags
    
    # If status changed to completed, set completed_at
    if db_item.status == ItemStatus.COMPLETED and db_item.completed_at is None:
        db_item.completed_at = datetime.utcnow()
    elif db_item.status != ItemStatus.COMPLETED:
        db_item.completed_at = None
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_schedule_item(db: Session, item_id: int) -> bool:
    """Delete a schedule item"""
    db_item = get_schedule_item_by_id(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True


def mark_item_complete(db: Session, item_id: int) -> ScheduleItem:
    """Mark item as completed"""
    db_item = get_schedule_item_by_id(db, item_id)
    if not db_item:
        return None
    
    db_item.status = ItemStatus.COMPLETED
    db_item.completed_at = datetime.utcnow()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def sync_item_with_calendar(db: Session, item_id: UUID, google_event_id: str) -> ExtractedItem:
    """Sync item with Google Calendar"""
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return None
    
    db_item.google_event_id = google_event_id
    db_item.status = "synced"
    db_item.updated_at = datetime.utcnow()
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: UUID) -> bool:
    """Delete item"""
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True
