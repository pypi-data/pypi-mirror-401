"""
Agent model - stores agent configurations
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class Agent(Base):
    """Agent configuration model"""

    __tablename__ = "agents"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    system_prompt = Column(Text, nullable=False)
    provider_id = Column(String, nullable=False)  # Reference to Provider.id
    model = Column(String, nullable=False)  # e.g., "gpt-4", "claude-3-sonnet"
    temperature = Column(String, default="0.7")
    max_tokens = Column(String, nullable=True)
    color = Column(String, default="#3B82F6")  # Hex color for UI
    avatar = Column(String, nullable=True)  # Avatar emoji or URL
    tools = Column(JSON, nullable=True, default=list)  # List of enabled tools: ["rag", "tools"]
    is_active = Column(Boolean, default=True)
    # `metadata` is a reserved attribute on Declarative base (Base.metadata).
    # Use the column name `metadata` but map it to the attribute `meta`.
    meta = Column("metadata", JSON, nullable=True)  # Additional configuration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
