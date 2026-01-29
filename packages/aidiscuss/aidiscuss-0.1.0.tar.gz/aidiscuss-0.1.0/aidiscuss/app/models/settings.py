"""
Settings model - stores application settings as a singleton
"""

from sqlalchemy import Column, Integer, JSON, DateTime
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class Settings(Base):
    """
    Settings model - singleton for application-wide settings
    Only one row should exist (id=1)
    """

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, default=1)
    appearance = Column(
        JSON, nullable=False, default=lambda: {"theme": "system", "density": "comfortable", "fontSize": "medium"}
    )
    safety = Column(
        JSON,
        nullable=False,
        default=lambda: {"enabled": True, "strictness": "medium", "toxicityDetection": False},
    )
    models = Column(
        JSON, nullable=False, default=lambda: {"preset": "standard", "primaryProvider": "openai", "apiKeys": {}}
    )
    storage = Column(JSON, nullable=False, default=lambda: {"encrypted": True})
    rag = Column(
        JSON,
        nullable=False,
        default=lambda: {
            "enabled": False,  # RAG model not loaded by default for fast startup
            "chunkSize": 1000,
            "chunkOverlap": 200,
            "maxResults": 5,
            "minRelevance": 0.7,
        },
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
