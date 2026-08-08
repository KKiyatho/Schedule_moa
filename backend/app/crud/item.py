"""
CRUD operations for Extracted Items
"""

from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.models import ExtractedItem
from app.schemas import ExtractedItemCreate, ExtractedItemUpdate


def get_item_by_id(db: Session, item_id: UUID) -> ExtractedItem:
    """Get item by ID"""
    return db.query(ExtractedItem).filter(ExtractedItem.id == item_id).first()


def get_document_items(db: Session, document_id: UUID):
    """Get all items from a document"""
    return db.query(ExtractedItem).filter(ExtractedItem.document_id == document_id).all()


def get_user_items(
    db: Session, user_id: UUID, status: str = None, skip: int = 0, limit: int = 100
):
    """Get all items for a user"""
    query = db.query(ExtractedItem).filter(ExtractedItem.user_id == user_id)
    
    if status:
        query = query.filter(ExtractedItem.status == status)
    
    return query.offset(skip).limit(limit).all()


def create_item(
    db: Session,
    user_id: UUID,
    document_id: UUID,
    title: str,
    item_type: str,
    description: str = None,
    due_date = None,
    due_time = None,
    location: str = None,
    priority: int = 3
) -> ExtractedItem:
    """Create a new extracted item"""
    db_item = ExtractedItem(
        user_id=user_id,
        document_id=document_id,
        title=title,
        item_type=item_type,
        description=description,
        due_date=due_date,
        due_time=due_time,
        location=location,
        priority=priority,
        status="pending"
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(
    db: Session, item_id: UUID, item_update: ExtractedItemUpdate
) -> ExtractedItem:
    """Update extracted item"""
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return None
    
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db_item.updated_at = datetime.utcnow()
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def mark_item_completed(db: Session, item_id: UUID) -> ExtractedItem:
    """Mark item as completed"""
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        return None
    
    db_item.is_completed = True
    db_item.completed_at = datetime.utcnow()
    db_item.updated_at = datetime.utcnow()
    
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
