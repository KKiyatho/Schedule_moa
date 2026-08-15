"""
CRUD operations for Tag
"""

from sqlalchemy.orm import Session
from typing import List
from app.models import Tag
from app.schemas import TagCreate, TagUpdate


def get_tag_by_id(db: Session, tag_id: int) -> Tag:
    """Get tag by ID"""
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_user_tags(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[Tag], int]:
    """Get all tags for a user"""
    query = db.query(Tag).filter(Tag.owner_id == owner_id)
    total = query.count()
    tags = query.order_by(Tag.created_at.desc()).offset(skip).limit(limit).all()
    return tags, total


def get_tag_by_name(db: Session, owner_id: int, name: str) -> Tag:
    """Get tag by name for a user"""
    return db.query(Tag).filter(
        (Tag.owner_id == owner_id) & (Tag.name == name)
    ).first()


def create_tag(
    db: Session,
    owner_id: int,
    tag_data: TagCreate
) -> Tag:
    """Create a new tag"""
    db_tag = Tag(
        owner_id=owner_id,
        name=tag_data.name,
        color=tag_data.color
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(
    db: Session,
    tag_id: int,
    tag_update: TagUpdate
) -> Tag:
    """Update a tag"""
    db_tag = get_tag_by_id(db, tag_id)
    if not db_tag:
        return None
    
    update_data = tag_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)
    
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int) -> bool:
    """Delete a tag"""
    db_tag = get_tag_by_id(db, tag_id)
    if not db_tag:
        return False
    
    db.delete(db_tag)
    db.commit()
    return True


def bulk_create_tags(
    db: Session,
    owner_id: int,
    tag_names: List[str]
) -> List[Tag]:
    """Create multiple tags at once"""
    tags = []
    for name in tag_names:
        existing = get_tag_by_name(db, owner_id, name)
        if not existing:
            tag = create_tag(db, owner_id, TagCreate(name=name, color="#808080"))
            tags.append(tag)
        else:
            tags.append(existing)
    return tags
