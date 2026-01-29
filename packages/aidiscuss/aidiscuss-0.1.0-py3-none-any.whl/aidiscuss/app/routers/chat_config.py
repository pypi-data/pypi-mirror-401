"""
Chat Configuration API Router

Endpoints for managing chat configurations:
- Create new configuration
- Retrieve configuration
- Update configuration (only if not locked)
- Lock configuration (after chat starts)
- Delete configuration
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from nanoid import generate

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.chat_config import ChatConfig, ChatConfigSchema


router = APIRouter(prefix="/api/chat-config", tags=["chat-config"])


@router.post("/create", response_model=dict)
async def create_chat_config(
    conversation_id: str,
    config: ChatConfigSchema,
    db: AsyncSession = Depends(get_db)
):
    """
    Create configuration for new chat

    Args:
        conversation_id: Unique conversation identifier
        config: Chat configuration settings
        db: Database session

    Returns:
        Created configuration with ID

    Raises:
        HTTPException: If configuration already exists for conversation
    """
    # Check if configuration already exists
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Configuration already exists for conversation {conversation_id}"
        )

    # Create new configuration
    chat_config = ChatConfig.from_schema(
        conversation_id=conversation_id,
        schema=config,
        config_id=generate(size=12)
    )

    db.add(chat_config)
    await db.commit()
    await db.refresh(chat_config)

    return {
        "id": chat_config.id,
        "conversation_id": chat_config.conversation_id,
        "is_locked": chat_config.is_locked,
        "created_at": chat_config.created_at.isoformat(),
        "config": config.model_dump()
    }


@router.get("/{conversation_id}", response_model=ChatConfigSchema)
async def get_chat_config(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get configuration for conversation

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        Chat configuration

    Raises:
        HTTPException: If configuration not found
    """
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    config = result.scalar_one_or_none()

    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration not found for conversation {conversation_id}"
        )

    return config.to_schema()


@router.get("/{conversation_id}/full", response_model=dict)
async def get_chat_config_full(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get full configuration details including metadata

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        Full configuration with metadata

    Raises:
        HTTPException: If configuration not found
    """
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    config = result.scalar_one_or_none()

    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration not found for conversation {conversation_id}"
        )

    return {
        "id": config.id,
        "conversation_id": config.conversation_id,
        "is_locked": config.is_locked,
        "created_at": config.created_at.isoformat(),
        "updated_at": config.updated_at.isoformat() if config.updated_at else None,
        "config": config.to_schema().model_dump()
    }


@router.put("/{conversation_id}", response_model=dict)
async def update_chat_config(
    conversation_id: str,
    config: ChatConfigSchema,
    db: AsyncSession = Depends(get_db)
):
    """
    Update configuration (only if not locked)

    Args:
        conversation_id: Conversation identifier
        config: Updated configuration
        db: Database session

    Returns:
        Updated configuration

    Raises:
        HTTPException: If not found or locked
    """
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    chat_config = result.scalar_one_or_none()

    if not chat_config:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration not found for conversation {conversation_id}"
        )

    if chat_config.is_locked:
        raise HTTPException(
            status_code=400,
            detail="Cannot modify locked configuration. Chat has already started."
        )

    # Update configuration
    chat_config.config_json = config.model_dump()

    await db.commit()
    await db.refresh(chat_config)

    return {
        "id": chat_config.id,
        "conversation_id": chat_config.conversation_id,
        "is_locked": chat_config.is_locked,
        "updated_at": chat_config.updated_at.isoformat() if chat_config.updated_at else None,
        "config": config.model_dump()
    }


@router.post("/{conversation_id}/lock", response_model=dict)
async def lock_chat_config(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Lock configuration (after chat starts)

    Once locked, configuration cannot be modified.

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        Updated configuration status

    Raises:
        HTTPException: If not found
    """
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    chat_config = result.scalar_one_or_none()

    if not chat_config:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration not found for conversation {conversation_id}"
        )

    # Lock configuration
    chat_config.is_locked = True

    await db.commit()
    await db.refresh(chat_config)

    return {
        "id": chat_config.id,
        "conversation_id": chat_config.conversation_id,
        "is_locked": chat_config.is_locked,
        "message": "Configuration locked successfully"
    }


@router.post("/{conversation_id}/unlock", response_model=dict)
async def unlock_chat_config(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Unlock configuration (admin only - for testing/debugging)

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        Updated configuration status

    Raises:
        HTTPException: If not found
    """
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    chat_config = result.scalar_one_or_none()

    if not chat_config:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration not found for conversation {conversation_id}"
        )

    # Unlock configuration
    chat_config.is_locked = False

    await db.commit()
    await db.refresh(chat_config)

    return {
        "id": chat_config.id,
        "conversation_id": chat_config.conversation_id,
        "is_locked": chat_config.is_locked,
        "message": "Configuration unlocked successfully"
    }


@router.delete("/{conversation_id}", response_model=dict)
async def delete_chat_config(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete configuration

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        Deletion confirmation

    Raises:
        HTTPException: If not found
    """
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    chat_config = result.scalar_one_or_none()

    if not chat_config:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration not found for conversation {conversation_id}"
        )

    await db.delete(chat_config)
    await db.commit()

    return {
        "conversation_id": conversation_id,
        "message": "Configuration deleted successfully"
    }


@router.get("/", response_model=List[dict])
async def list_chat_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    List all chat configurations

    Args:
        skip: Number of records to skip
        limit: Maximum records to return
        db: Database session

    Returns:
        List of configurations
    """
    result = await db.execute(
        select(ChatConfig).offset(skip).limit(limit)
    )
    configs = result.scalars().all()

    return [
        {
            "id": config.id,
            "conversation_id": config.conversation_id,
            "is_locked": config.is_locked,
            "created_at": config.created_at.isoformat(),
            "conversation_goal": config.config_json.get("conversation_goal", ""),
            "turn_strategy": config.config_json.get("turn_strategy", ""),
            "max_turns": config.config_json.get("max_turns", 0)
        }
        for config in configs
    ]


@router.get("/{conversation_id}/summary", response_model=dict)
async def get_config_summary(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get configuration summary for display badges

    Returns key settings in a concise format for UI badges/chips.

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        Configuration summary

    Raises:
        HTTPException: If not found
    """
    result = await db.execute(
        select(ChatConfig).where(ChatConfig.conversation_id == conversation_id)
    )
    config = result.scalar_one_or_none()

    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration not found for conversation {conversation_id}"
        )

    config_data = config.config_json

    return {
        "goal": config_data.get("conversation_goal", "")[:100],
        "strategy": config_data.get("turn_strategy", "round-robin"),
        "max_turns": config_data.get("max_turns", 20),
        "quality_enabled": config_data.get("enable_reflection", False),
        "system_ai_mode": config_data.get("system_ai_mode", "passive"),
        "consensus_enabled": config_data.get("consensus_enabled", False),
        "rag_enabled": config_data.get("enable_rag", False),
        "is_locked": config.is_locked
    }
