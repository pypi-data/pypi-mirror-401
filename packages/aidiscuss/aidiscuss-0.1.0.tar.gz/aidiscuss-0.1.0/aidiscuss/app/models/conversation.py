"""
Conversation and Message models
"""

from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from aidiscuss.app.db.base import Base


class Conversation(Base):
    """Conversation/Session model"""

    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False, default="New Conversation")
    orchestration_strategy = Column(String, default="round-robin")
    agent_ids = Column(JSON, nullable=False)  # List of agent IDs participating
    # `metadata` is reserved on Declarative base. Map DB column `metadata` to attribute `meta`.
    meta = Column("metadata", JSON, nullable=True)  # Analytics, settings, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # LangGraph support (from migration 001)
    chat_config_id = Column(String, nullable=True)
    langgraph_state = Column(JSON, nullable=True)

    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Message model"""

    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # "user", "assistant", "system"
    content = Column(Text, nullable=False)
    agent_id = Column(String, nullable=True)  # Which agent generated this (if role="assistant")
    turn_number = Column(Integer, nullable=True)  # Turn number in conversation
    # Map DB column `metadata` to attribute `meta` to avoid Declarative reserved name.
    meta = Column("metadata", JSON, nullable=True)  # Token counts, latency, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Quality tracking (from migration 001)
    quality_score = Column(Integer, nullable=True)
    regeneration_count = Column(Integer, nullable=True, server_default='0')

    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")
