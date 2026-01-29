"""
Conversation Memory model - stores memory state for conversations
"""

from sqlalchemy import Column, String, Text, Integer, JSON, DateTime
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class ConversationMemory(Base):
    """
    Conversation Memory model - stores facts, checkpoints, and summaries
    per conversation for long-term memory functionality
    """

    __tablename__ = "conversation_memories"

    conversation_id = Column(String, primary_key=True)
    rolling_summary = Column(Text, nullable=True)
    facts = Column(JSON, nullable=False, default=list)  # List of fact objects
    checkpoints = Column(JSON, nullable=False, default=list)  # List of checkpoint objects
    last_summary_turn = Column(Integer, nullable=False, default=0)
    last_checkpoint_turn = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
