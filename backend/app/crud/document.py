"""
CRUD operations for Document
"""

from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.models import Document
from app.schemas import DocumentCreate


def get_document_by_id(db: Session, document_id: UUID) -> Document:
    """Get document by ID"""
    return db.query(Document).filter(Document.id == document_id).first()


def get_user_documents(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    """Get all documents for a user"""
    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_document(
    db: Session, user_id: UUID, file_name: str, file_path: str, file_type: str
) -> Document:
    """Create a new document record"""
    db_document = Document(
        user_id=user_id,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        status="pending"
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document_text(
    db: Session, document_id: UUID, extracted_text: str, status: str = "extracted"
) -> Document:
    """Update document with extracted text"""
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    
    db_document.extracted_text = extracted_text
    db_document.status = status
    db_document.updated_at = datetime.utcnow()
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document_status(
    db: Session, document_id: UUID, status: str
) -> Document:
    """Update document status"""
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    
    db_document.status = status
    db_document.updated_at = datetime.utcnow()
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def delete_document(db: Session, document_id: UUID) -> bool:
    """Delete document"""
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return False
    
    db.delete(db_document)
    db.commit()
    return True
