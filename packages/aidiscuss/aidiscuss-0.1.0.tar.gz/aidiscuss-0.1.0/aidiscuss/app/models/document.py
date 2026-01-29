"""
Document models for RAG system
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, JSON
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class Document(Base):
    """Document metadata"""

    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    namespace = Column(String, default="default")
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    doc_metadata = Column(JSON, nullable=True)  # Renamed from 'metadata' to avoid SQLAlchemy conflict


class DocumentChunk(Base):
    """Text chunks with embeddings"""

    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True)
    document_id = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding_id = Column(String, nullable=True)
    chunk_metadata = Column(JSON, nullable=True)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
