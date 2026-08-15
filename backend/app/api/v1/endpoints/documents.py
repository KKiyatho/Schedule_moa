"""
Document upload and management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas import (
    DocumentResponse,
    DocumentWithItems,
    DocumentProcessingRequest,
    DocumentProcessingResponse
)
from app.crud import document as document_crud
from app.crud.user import get_user_by_id
from app.models.document import DocumentType, DocumentStatus

router = APIRouter(prefix="/documents", tags=["documents"])

# Configuration
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif", "docx"}
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 52428800  # 50MB


def get_file_type(filename: str) -> DocumentType:
    """Determine document type from file extension"""
    ext = filename.split(".")[-1].lower()
    if ext == "pdf":
        return DocumentType.PDF
    elif ext in {"png", "jpg", "jpeg", "gif"}:
        return DocumentType.IMAGE
    else:
        return DocumentType.DOCUMENT


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document (PDF, image, or text file)
    """
    user_id = int(current_user["user_id"])
    
    # Verify user exists
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Validate file type
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Read file content
    contents = await file.read()
    
    # Check file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE} bytes"
        )
    
    # Save file with timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_path = f"{UPLOAD_DIR}/{user_id}_{timestamp}_{file.filename}"
    
    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Create document record in database
    doc_type = get_file_type(file.filename)
    db_document = document_crud.create_document(
        db=db,
        owner_id=user_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=doc_type,
        file_size=len(contents)
    )
    
    return DocumentResponse.model_validate(db_document)


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all documents for current user
    """
    user_id = int(current_user["user_id"])
    
    status_enum = None
    if status_filter:
        try:
            status_enum = DocumentStatus[status_filter.upper()]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter. Allowed values: {', '.join([s.value for s in DocumentStatus])}"
            )
    
    documents, total = document_crud.get_user_documents(db, user_id, skip, limit, status_enum)
    return [DocumentResponse.model_validate(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentWithItems)
async def get_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific document with extracted items
    """
    user_id = int(current_user["user_id"])
    document = document_crud.get_document_by_id(db, document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if document.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this document"
        )
    
    return DocumentWithItems.model_validate(document)


@router.post("/{document_id}/process", response_model=DocumentProcessingResponse)
async def process_document(
    document_id: int,
    processing_request: DocumentProcessingRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process a document (extract text and classify items)
    Note: Actual AI processing will be implemented later
    """
    user_id = int(current_user["user_id"])
    document = document_crud.get_document_by_id(db, document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if document.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to process this document"
        )
    
    # Update status to processing
    updated = document_crud.update_document_status(
        db,
        document_id,
        DocumentStatus.PROCESSING,
        progress=0
    )
    
    return DocumentProcessingResponse(
        document_id=updated.id,
        status=updated.status,
        message="Document processing started",
        processing_progress=updated.processing_progress
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document and associated file
    """
    user_id = int(current_user["user_id"])
    document = document_crud.get_document_by_id(db, document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if document.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this document"
        )
    
    # Delete file from filesystem
    if os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            # Log error but continue with DB deletion
            print(f"Error deleting file {document.file_path}: {e}")
    
    # Delete from database
    document_crud.delete_document(db, document_id)
    
    return {"message": "Document deleted successfully"}

