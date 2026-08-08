"""
Document upload and management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import os
from uuid import UUID

from app.db.session import get_db
from app.schemas import DocumentResponse
from app.crud.document import create_document, get_user_documents, get_document_by_id
from app.models import Document

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = "test",  # TODO: Get from current user
    db: Session = Depends(get_db)
):
    """
    Upload a document (PDF, image, or text)
    """
    # Validate file type
    allowed_types = {"pdf", "png", "jpg", "jpeg", "gif", "docx"}
    file_ext = file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save file
    file_path = f"uploads/{user_id}_{file.filename}"
    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    
    # Create document record in database
    db_document = create_document(
        db=db,
        user_id=UUID(user_id),
        file_name=file.filename,
        file_path=file_path,
        file_type=file_ext
    )
    
    return DocumentResponse.model_validate(db_document)


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    user_id: str = "test",  # TODO: Get from current user
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all documents for current user
    """
    documents = get_user_documents(db, UUID(user_id), skip=skip, limit=limit)
    return [DocumentResponse.model_validate(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific document by ID
    """
    document = get_document_by_id(db, UUID(document_id))
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return DocumentResponse.model_validate(document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a document
    """
    document = get_document_by_id(db, UUID(document_id))
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
