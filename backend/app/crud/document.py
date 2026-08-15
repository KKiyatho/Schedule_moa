"""
CRUD operations for Document
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.models import Document
from app.models.document import DocumentStatus, DocumentType
from app.schemas import DocumentCreate


def get_document_by_id(db: Session, document_id: int) -> Document:
    """Get document by ID"""
    return db.query(Document).filter(Document.id == document_id).first()


def get_user_documents(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[DocumentStatus] = None
) -> tuple[List[Document], int]:
    """Get all documents for a user with pagination"""
    query = db.query(Document).filter(Document.owner_id == user_id)
    
    if status:
        query = query.filter(Document.status == status)
    
    total = query.count()
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    return documents, total


def create_document(
    db: Session,
    owner_id: int,
    file_name: str,
    file_path: str,
    file_type: DocumentType,
    file_size: Optional[int] = None
) -> Document:
    """Create a new document record"""
    db_document = Document(
        owner_id=owner_id,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        status=DocumentStatus.UPLOADED,
        processing_progress=0
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document_status(
    db: Session,
    document_id: int,
    status: DocumentStatus,
    progress: int = None
) -> Document:
    """Update document status and optionally progress"""
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    
    db_document.status = status
    if progress is not None:
        db_document.processing_progress = progress
    
    if status == DocumentStatus.PROCESSING and db_document.processing_started_at is None:
        db_document.processing_started_at = datetime.utcnow()
    elif status in (DocumentStatus.COMPLETED, DocumentStatus.FAILED):
        db_document.processing_completed_at = datetime.utcnow()
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document_extraction(
    db: Session,
    document_id: int,
    extracted_text: str,
    extraction_method: str,
    ai_model_used: Optional[str] = None,
    ai_summary: Optional[str] = None
) -> Document:
    """Update document with extracted text and AI results"""
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    
    db_document.extracted_text = extracted_text
    db_document.extraction_method = extraction_method
    db_document.ai_model_used = ai_model_used
    db_document.ai_summary = ai_summary
    db_document.status = DocumentStatus.COMPLETED
    db_document.processing_progress = 100
    db_document.processing_completed_at = datetime.utcnow()
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def set_document_error(
    db: Session,
    document_id: int,
    error_message: str
) -> Document:
    """Mark document as failed with error message"""
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    
    db_document.status = DocumentStatus.FAILED
    db_document.error_message = error_message
    db_document.processing_completed_at = datetime.utcnow()
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def delete_document(db: Session, document_id: int) -> bool:
    """Delete document"""
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return False
    
    db.delete(db_document)
    db.commit()
    return True
