"""
RAG (Retrieval-Augmented Generation) router
"""

import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
from nanoid import generate

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.document import Document, DocumentChunk
from aidiscuss.app.services.rag_service import rag_service
from aidiscuss.app.core.config import settings

logger = logging.getLogger("aidiscuss.routers.rag")

router = APIRouter()

# Upload directory - store in DATA_DIR alongside databases
UPLOAD_DIR = str(settings.DATA_DIR / "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


class DocumentResponse(BaseModel):
    """Document response"""

    id: str
    filename: str
    file_type: str
    file_size: int
    namespace: str
    chunk_count: int

    model_config = {"from_attributes": True}


class DuplicateFileResponse(BaseModel):
    """Response when duplicate file is detected"""

    status: str = "duplicate_detected"
    existing_document_id: str
    filename: str
    message: str


class SearchRequest(BaseModel):
    """Search request"""

    query: str
    namespace: str = "default"
    k: int = 5
    min_score: float = 0.7


class SearchResult(BaseModel):
    """Search result"""

    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    namespace: str = "default",
    db: AsyncSession = Depends(get_db),
):
    """Upload and process document
    
    Automatically renames file with '(copy)' suffix if duplicate exists.
    
    Args:
        file: Document file (PDF, TXT, or MD)
        namespace: Collection namespace
        
    Returns:
        DocumentResponse with upload details
    """
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file_ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Check for duplicate filename and auto-rename if needed
    original_filename = file.filename
    stmt = select(Document).where(
        Document.filename == file.filename,
        Document.namespace == namespace
    )
    result = await db.execute(stmt)
    existing_doc = result.scalar_one_or_none()
    
    if existing_doc:
        # Auto-rename with (copy) suffix
        name, ext = os.path.splitext(file.filename)
        counter = 1
        file.filename = f"{name} (copy){ext}"
        
        # Check if "(copy)" version also exists, increment counter if needed
        while True:
            stmt = select(Document).where(
                Document.filename == file.filename,
                Document.namespace == namespace
            )
            result = await db.execute(stmt)
            if not result.scalar_one_or_none():
                break
            counter += 1
            file.filename = f"{name} (copy {counter}){ext}"

    # Ensure embedding model is loaded
    if not rag_service.is_model_loaded():
        load_result = rag_service.load_model()
        if not load_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=f"Failed to load embedding model: {load_result.get('message')}",
            )

    # Generate document ID and save file
    doc_id = generate()
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    # Process document
    try:
        chunks = rag_service.process_document(file_path, file_ext)
        chunk_count = rag_service.add_documents(namespace, doc_id, chunks)

        # Store document metadata
        document = Document(
            id=doc_id,
            filename=file.filename,
            file_type=file_ext,
            file_size=len(contents),
            namespace=namespace,
            chunk_count=chunk_count,
        )

        db.add(document)
        await db.commit()
        await db.refresh(document)
        
        return document

    except RuntimeError as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=503,
            detail=f"Embedding model error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing document: {str(e)}"
        )


@router.post("/search", response_model=List[SearchResult])
async def search_documents(request: SearchRequest):
    """Search documents using vector similarity"""
    # Ensure embedding model is loaded
    if not rag_service.is_model_loaded():
        load_result = rag_service.load_model()
        if not load_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=f"Failed to load embedding model: {load_result.get('message')}",
            )

    try:
        results = rag_service.search(
            query=request.query,
            namespace=request.namespace,
            k=request.k,
            min_score=request.min_score,
        )
        
        return [
            SearchResult(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                content=r["content"],
                score=r["score"],
                metadata=r.get("metadata", {}),
            )
            for r in results
        ]
    
    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Embedding model error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid search parameters: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(namespace: str = None, db: AsyncSession = Depends(get_db)):
    """List all documents"""

    query = select(Document)
    if namespace:
        query = query.where(Document.namespace == namespace)

    result = await db.execute(query)
    documents = result.scalars().all()

    return documents


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: AsyncSession = Depends(get_db)):
    """Get document by ID"""

    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Delete document"""

    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete from database
    await db.delete(document)
    await db.commit()

    # Delete from vector store in background
    def _delete_from_vector_store():
        rag_service.delete_document(document.namespace, document_id)

        # Delete file
        file_path = os.path.join(UPLOAD_DIR, f"{document_id}_{document.filename}")
        if os.path.exists(file_path):
            os.remove(file_path)

    background_tasks.add_task(_delete_from_vector_store)


@router.get("/namespaces", response_model=List[str])
async def list_namespaces():
    """List available namespaces"""
    return rag_service.get_namespaces()


@router.get("/stats/{namespace}")
async def get_namespace_stats(namespace: str):
    """Get statistics for namespace"""
    return rag_service.get_stats(namespace)
