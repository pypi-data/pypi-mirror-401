"""
Conversation management router with real-time sync
Provides CRUD operations for conversations and messages
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.conversation import Conversation, Message
from aidiscuss.app.services.broadcast import broadcast_service

router = APIRouter()


# Pydantic models
class ConversationCreate(BaseModel):
    """Request model for creating a conversation"""

    id: str | None = None
    title: str | None = None
    orchestration_strategy: str = "round-robin"
    agent_ids: list[str] = Field(default_factory=list)
    meta: dict[str, Any] | None = None


class ConversationUpdate(BaseModel):
    """Request model for updating a conversation"""

    title: str | None = None
    orchestration_strategy: str | None = None
    agent_ids: list[str] | None = None
    meta: dict[str, Any] | None = None


class MessageCreate(BaseModel):
    """Request model for creating a message"""

    id: str | None = None
    role: str
    content: str
    agent_id: str | None = None
    turn_number: int | None = None
    meta: dict[str, Any] | None = None


class MessageUpdate(BaseModel):
    """Request model for updating a message"""

    content: str | None = None
    meta: dict[str, Any] | None = None


class MessageResponse(BaseModel):
    """Response model for a message"""

    id: str
    conversation_id: str
    role: str
    content: str
    agent_id: str | None
    turn_number: int | None
    meta: dict[str, Any] | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationResponse(BaseModel):
    """Response model for conversation metadata (without messages)"""

    id: str
    title: str | None
    orchestration_strategy: str
    agent_ids: list[str]
    meta: dict[str, Any] | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class ConversationDetailResponse(BaseModel):
    """Response model for conversation with all messages"""

    id: str
    title: str | None
    orchestration_strategy: str
    agent_ids: list[str]
    meta: dict[str, Any] | None
    messages: list[MessageResponse]
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


# Conversation endpoints
@router.get("", response_model=list[ConversationResponse])
async def list_conversations(
    limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)
):
    """
    List conversations (metadata only, no messages)
    Ordered by most recently updated first
    """
    result = await db.execute(
        select(Conversation).order_by(desc(Conversation.updated_at)).limit(limit).offset(offset)
    )
    conversations = result.scalars().all()
    return conversations


@router.post("", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    data: ConversationCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    """Create a new conversation"""
    import uuid

    conversation_id = data.id or str(uuid.uuid4())

    # Check if conversation already exists
    if data.id:
        result = await db.execute(select(Conversation).where(Conversation.id == data.id))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"Conversation with ID '{data.id}' already exists")

    conversation = Conversation(
        id=conversation_id,
        title=data.title,
        orchestration_strategy=data.orchestration_strategy,
        agent_ids=data.agent_ids,
        meta=data.meta,
    )

    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)

    # Broadcast to all clients
    background_tasks.add_task(
        broadcast_service.broadcast_conversation_created,
        {
            "id": conversation.id,
            "title": conversation.title,
            "orchestration_strategy": conversation.orchestration_strategy,
            "agent_ids": conversation.agent_ids,
            "meta": conversation.meta,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
        },
    )

    return conversation


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """Get a conversation with all its messages"""
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Load messages
    messages_result = await db.execute(
        select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    )
    messages = messages_result.scalars().all()

    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        orchestration_strategy=conversation.orchestration_strategy,
        agent_ids=conversation.agent_ids,
        meta=conversation.meta,
        messages=[MessageResponse.model_validate(msg) for msg in messages],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    data: ConversationUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Update a conversation's metadata"""
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(conversation, key, value)

    await db.commit()
    await db.refresh(conversation)

    # Broadcast to all clients
    background_tasks.add_task(
        broadcast_service.broadcast_conversation_updated,
        {
            "id": conversation.id,
            "title": conversation.title,
            "orchestration_strategy": conversation.orchestration_strategy,
            "agent_ids": conversation.agent_ids,
            "meta": conversation.meta,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
        },
    )

    return conversation


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    """Delete a conversation and all its messages"""
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # SQLAlchemy will handle cascading deletion of messages
    await db.delete(conversation)
    await db.commit()

    # Broadcast to all clients
    background_tasks.add_task(broadcast_service.broadcast_conversation_deleted, conversation_id)


# Message endpoints
@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
async def add_message(
    conversation_id: str,
    data: MessageCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Add a message to a conversation"""
    import uuid

    # Verify conversation exists
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    message_id = data.id or str(uuid.uuid4())

    message = Message(
        id=message_id,
        conversation_id=conversation_id,
        role=data.role,
        content=data.content,
        agent_id=data.agent_id,
        turn_number=data.turn_number,
        meta=data.meta,
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    # Broadcast to all clients
    background_tasks.add_task(
        broadcast_service.broadcast_message_added,
        conversation_id,
        {
            "id": message.id,
            "conversation_id": message.conversation_id,
            "role": message.role,
            "content": message.content,
            "agent_id": message.agent_id,
            "turn_number": message.turn_number,
            "meta": message.meta,
            "created_at": message.created_at.isoformat(),
        },
    )

    return message


@router.patch("/{conversation_id}/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    conversation_id: str,
    message_id: str,
    data: MessageUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Update a message"""
    result = await db.execute(
        select(Message).where(Message.id == message_id, Message.conversation_id == conversation_id)
    )
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(message, key, value)

    await db.commit()
    await db.refresh(message)

    # Broadcast to all clients
    background_tasks.add_task(
        broadcast_service.broadcast_message_updated,
        conversation_id,
        {
            "id": message.id,
            "conversation_id": message.conversation_id,
            "role": message.role,
            "content": message.content,
            "agent_id": message.agent_id,
            "turn_number": message.turn_number,
            "meta": message.meta,
            "created_at": message.created_at.isoformat(),
        },
    )

    return message


@router.delete("/{conversation_id}/messages/{message_id}", status_code=204)
async def delete_message(
    conversation_id: str,
    message_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Delete a message"""
    result = await db.execute(
        select(Message).where(Message.id == message_id, Message.conversation_id == conversation_id)
    )
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    await db.delete(message)
    await db.commit()

    # Broadcast to all clients
    background_tasks.add_task(broadcast_service.broadcast_message_deleted, conversation_id, message_id)
