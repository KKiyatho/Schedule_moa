"""
CRUD operations for Calendar
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models import Calendar
from app.schemas import CalendarCreate, CalendarUpdate


def get_calendar_by_id(db: Session, calendar_id: int) -> Calendar:
    """Get calendar by ID"""
    return db.query(Calendar).filter(Calendar.id == calendar_id).first()


def get_user_calendars(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[Calendar], int]:
    """Get all calendars for a user"""
    query = db.query(Calendar).filter(Calendar.owner_id == owner_id)
    total = query.count()
    calendars = query.order_by(Calendar.created_at.desc()).offset(skip).limit(limit).all()
    return calendars, total


def get_default_calendar(db: Session, owner_id: int) -> Optional[Calendar]:
    """Get user's default calendar"""
    return db.query(Calendar).filter(
        (Calendar.owner_id == owner_id) & (Calendar.is_default == True)
    ).first()


def get_calendar_by_google_id(db: Session, google_calendar_id: str) -> Optional[Calendar]:
    """Get calendar by Google Calendar ID"""
    return db.query(Calendar).filter(Calendar.google_calendar_id == google_calendar_id).first()


def create_calendar(
    db: Session,
    owner_id: int,
    calendar_data: CalendarCreate
) -> Calendar:
    """Create a new calendar"""
    # If no default exists, make this one default
    existing_default = get_default_calendar(db, owner_id)
    is_default = calendar_data.is_default or (existing_default is None)
    
    # If this is being set as default, unset others
    if is_default and existing_default and existing_default.id != calendar_data.id:
        existing_default.is_default = False
        db.add(existing_default)
    
    db_calendar = Calendar(
        owner_id=owner_id,
        name=calendar_data.name,
        description=calendar_data.description,
        color=calendar_data.color,
        is_default=is_default
    )
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


def update_calendar(
    db: Session,
    calendar_id: int,
    calendar_update: CalendarUpdate
) -> Optional[Calendar]:
    """Update a calendar"""
    db_calendar = get_calendar_by_id(db, calendar_id)
    if not db_calendar:
        return None
    
    update_data = calendar_update.dict(exclude_unset=True)
    
    # Handle is_default separately
    if update_data.get("is_default"):
        # Unset other defaults for this owner
        existing_default = db.query(Calendar).filter(
            (Calendar.owner_id == db_calendar.owner_id) & 
            (Calendar.is_default == True) &
            (Calendar.id != calendar_id)
        ).first()
        if existing_default:
            existing_default.is_default = False
            db.add(existing_default)
    
    for field, value in update_data.items():
        setattr(db_calendar, field, value)
    
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


def sync_calendar_to_google(
    db: Session,
    calendar_id: int,
    google_calendar_id: str
) -> Optional[Calendar]:
    """Link calendar to Google Calendar"""
    db_calendar = get_calendar_by_id(db, calendar_id)
    if not db_calendar:
        return None
    
    db_calendar.google_calendar_id = google_calendar_id
    db_calendar.is_synced_to_google = True
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar


def delete_calendar(db: Session, calendar_id: int) -> bool:
    """Delete a calendar"""
    db_calendar = get_calendar_by_id(db, calendar_id)
    if not db_calendar:
        return False
    
    db.delete(db_calendar)
    db.commit()
    return True
