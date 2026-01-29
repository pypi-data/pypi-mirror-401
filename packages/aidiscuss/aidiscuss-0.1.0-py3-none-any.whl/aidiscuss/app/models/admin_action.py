"""
Admin Action Model and Schema

Stores audit log of admin override actions during conversations.
Admin has highest authority and can redirect, kick agents, inject context, etc.
"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, JSON, DateTime, Text
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class AdminOverrideSchema(BaseModel):
    """Pydantic schema for admin override action"""

    action_type: Literal[
        "redirect",
        "kick_agent",
        "add_agent",
        "modify_goal",
        "inject_context",
        "pause",
        "resume",
        "toggle_system_ai_mode"
    ] = Field(
        ...,
        description="Type of admin action to execute"
    )

    target_agent_id: Optional[str] = Field(
        default=None,
        description="Target agent ID (for kick_agent or add_agent actions)"
    )

    new_goal: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="New conversation goal (for redirect or modify_goal actions)"
    )

    injected_context: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Context or information to inject (for inject_context action)"
    )

    new_system_ai_mode: Optional[Literal["active", "passive"]] = Field(
        default=None,
        description="New System AI mode (for toggle_system_ai_mode action)"
    )

    user_id: str = Field(
        default="admin",
        description="User ID performing the action"
    )

    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of action submission"
    )

    action_metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata for the action"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "redirect",
                "new_goal": "Focus on ethical implications rather than technical details",
                "user_id": "admin",
                "action_metadata": {"reason": "Conversation drifting from intended focus"}
            }
        }


class AdminAction(Base):
    """Database model for admin action audit log"""
    __tablename__ = "admin_actions"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False, index=True)

    # Action details
    action_type = Column(String, nullable=False)
    target_agent_id = Column(String, nullable=True)
    new_goal = Column(Text, nullable=True)
    injected_context = Column(Text, nullable=True)
    new_system_ai_mode = Column(String, nullable=True)

    # Audit fields
    user_id = Column(String, default="admin", nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    action_metadata = Column(JSON, nullable=True)

    # Execution tracking
    executed = Column(String, default=False, nullable=False)  # Boolean stored as string
    execution_timestamp = Column(DateTime(timezone=True), nullable=True)
    execution_result = Column(JSON, nullable=True)

    def to_schema(self) -> AdminOverrideSchema:
        """Convert database model to Pydantic schema"""
        return AdminOverrideSchema(
            action_type=self.action_type,
            target_agent_id=self.target_agent_id,
            new_goal=self.new_goal,
            injected_context=self.injected_context,
            new_system_ai_mode=self.new_system_ai_mode,
            user_id=self.user_id,
            timestamp=self.timestamp,
            action_metadata=self.action_metadata
        )

    @staticmethod
    def from_schema(
        conversation_id: str,
        schema: AdminOverrideSchema,
        action_id: str
    ) -> "AdminAction":
        """Create database model from Pydantic schema"""
        return AdminAction(
            id=action_id,
            conversation_id=conversation_id,
            action_type=schema.action_type,
            target_agent_id=schema.target_agent_id,
            new_goal=schema.new_goal,
            injected_context=schema.injected_context,
            new_system_ai_mode=schema.new_system_ai_mode,
            user_id=schema.user_id,
            timestamp=schema.timestamp,
            action_metadata=schema.action_metadata,
            executed=False
        )

    def mark_executed(self, result: Optional[dict] = None):
        """Mark action as executed with optional result"""
        self.executed = True
        self.execution_timestamp = datetime.now()
        self.execution_result = result

    def __repr__(self) -> str:
        return (
            f"<AdminAction(id={self.id}, type={self.action_type}, "
            f"conversation_id={self.conversation_id}, executed={self.executed})>"
        )
