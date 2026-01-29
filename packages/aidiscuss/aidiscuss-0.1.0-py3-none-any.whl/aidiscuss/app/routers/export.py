"""
Export/Import router for data management
Provides endpoints for exporting chats, agents, and full backups
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel, validator
from typing import Any
from datetime import datetime
import json
import io

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.conversation import Conversation, Message
from aidiscuss.app.models.agent import Agent
from aidiscuss.app.models.provider import Provider
from aidiscuss.app.models.settings import Settings
from aidiscuss.app.models.conversation_memory import ConversationMemory

router = APIRouter(prefix="/api/export", tags=["export"])


# Pydantic models for validation
class BackupSchema(BaseModel):
    """Schema for validating backup files"""

    version: str
    exported_at: str
    conversations: list[dict[str, Any]]
    agents: list[dict[str, Any]]

    @validator("version")
    def check_version(cls, v):
        if not v.startswith("1."):
            raise ValueError("Unsupported backup version")
        return v


# Export endpoints
@router.get("/conversation/{conversation_id}/markdown")
async def export_conversation_markdown(
    conversation_id: str, db: AsyncSession = Depends(get_db)
):
    """
    Export a single conversation as Markdown
    Returns a formatted markdown file with all messages
    """
    # Get conversation
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get messages
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.turn_number, Message.created_at)
    )
    messages = messages_result.scalars().all()

    # Generate markdown content
    md_lines = [
        f"# {conversation.title or 'Untitled Chat'}",
        "",
        f"**Created:** {conversation.created_at.isoformat()}",
        f"**Agents:** {', '.join(conversation.agent_ids) if conversation.agent_ids else 'None'}",
        f"**Messages:** {len(messages)}",
        "",
        "---",
        "",
        "## Conversation",
        "",
    ]

    for msg in messages:
        # Format role name
        role_name = msg.role.title()
        if msg.role == "assistant" and msg.agent_id:
            role_name = f"Assistant ({msg.agent_id})"
        elif msg.role == "user":
            role_name = "User"
        elif msg.role == "system":
            role_name = "System"

        # Format timestamp
        timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")

        # Add message to markdown
        md_lines.extend([f"### {role_name} ({timestamp})", msg.content, ""])

    # Add footer
    md_lines.extend(
        [
            "---",
            "",
            "**Exported from AIDiscuss**",
            f"**Export Date:** {datetime.utcnow().isoformat()}",
        ]
    )

    markdown = "\n".join(md_lines)

    # Sanitize filename
    safe_title = "".join(
        c for c in (conversation.title or "chat") if c.isalnum() or c in (" ", "-", "_")
    )[:50]
    filename = f"chat-{safe_title}.md"

    return Response(
        content=markdown,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/full")
async def export_full_backup(db: AsyncSession = Depends(get_db)):
    """
    Export complete database as JSON
    Includes all conversations, messages, agents, and settings
    """
    # Get all conversations
    conversations_result = await db.execute(select(Conversation))
    conversations = conversations_result.scalars().all()

    # Get all messages
    messages_result = await db.execute(select(Message))
    messages = messages_result.scalars().all()

    # Get all agents
    agents_result = await db.execute(select(Agent))
    agents = agents_result.scalars().all()

    # Build export structure
    export_data = {
        "version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "conversations": [
            {
                "id": c.id,
                "title": c.title,
                "orchestration_strategy": c.orchestration_strategy,
                "agent_ids": c.agent_ids,
                "meta": c.meta,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                "messages": [
                    {
                        "id": m.id,
                        "role": m.role,
                        "content": m.content,
                        "agent_id": m.agent_id,
                        "turn_number": m.turn_number,
                        "meta": m.meta,
                        "created_at": m.created_at.isoformat(),
                    }
                    for m in messages
                    if m.conversation_id == c.id
                ],
            }
            for c in conversations
        ],
        "agents": [
            {
                "id": a.id,
                "name": a.name,
                "system_prompt": a.system_prompt,
                "provider_id": a.provider_id,
                "model": a.model,
                "temperature": a.temperature,
                "max_tokens": a.max_tokens,
                "color": a.color,
                "is_active": a.is_active,
                "meta": a.meta,
            }
            for a in agents
        ],
        "metadata": {
            "total_conversations": len(conversations),
            "total_messages": len(messages),
            "total_agents": len(agents),
        },
    }

    json_str = json.dumps(export_data, indent=2)

    return Response(
        content=json_str,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="aidiscuss-backup-{int(datetime.utcnow().timestamp())}.json"'
        },
    )


@router.get("/agents")
async def export_agents(db: AsyncSession = Depends(get_db)):
    """Export all agents as JSON"""
    agents_result = await db.execute(select(Agent))
    agents = agents_result.scalars().all()

    export_data = {
        "version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "agents": [
            {
                "id": a.id,
                "name": a.name,
                "system_prompt": a.system_prompt,
                "provider_id": a.provider_id,
                "model": a.model,
                "temperature": a.temperature,
                "max_tokens": a.max_tokens,
                "color": a.color,
                "is_active": a.is_active,
                "meta": a.meta,
            }
            for a in agents
        ],
    }

    json_str = json.dumps(export_data, indent=2)

    return Response(
        content=json_str,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="agents-{int(datetime.utcnow().timestamp())}.json"'
        },
    )


# Import endpoints
@router.post("/import/full")
async def import_full_backup(file: UploadFile, db: AsyncSession = Depends(get_db)):
    """
    Import full backup from JSON
    Validates schema and imports all data in a transaction
    """
    # Read and parse file
    content = await file.read()
    try:
        data = json.loads(content)
        backup = BackupSchema(**data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid backup file: {str(e)}")

    imported_counts = {
        "conversations": 0,
        "messages": 0,
        "agents": 0,
    }

    try:
        # Import agents first (conversations may reference them)
        for agent_data in backup.agents:
            # Check if agent already exists
            existing = await db.execute(select(Agent).where(Agent.id == agent_data["id"]))
            if not existing.scalar_one_or_none():
                agent = Agent(
                    id=agent_data["id"],
                    name=agent_data["name"],
                    system_prompt=agent_data["system_prompt"],
                    provider_id=agent_data.get("provider_id"),
                    model=agent_data.get("model"),
                    temperature=agent_data.get("temperature"),
                    max_tokens=agent_data.get("max_tokens"),
                    color=agent_data.get("color"),
                    is_active=agent_data.get("is_active", True),
                    meta=agent_data.get("meta"),
                )
                db.add(agent)
                imported_counts["agents"] += 1

        # Import conversations and messages
        for conv_data in backup.conversations:
            messages_data = conv_data.pop("messages", [])

            # Check if conversation already exists
            existing_conv = await db.execute(
                select(Conversation).where(Conversation.id == conv_data["id"])
            )
            if existing_conv.scalar_one_or_none():
                # Skip existing conversations to avoid duplicates
                continue

            # Create conversation
            conversation = Conversation(
                id=conv_data["id"],
                title=conv_data.get("title"),
                orchestration_strategy=conv_data.get("orchestration_strategy", "round-robin"),
                agent_ids=conv_data.get("agent_ids", []),
                meta=conv_data.get("meta"),
            )
            db.add(conversation)
            imported_counts["conversations"] += 1

            # Import messages
            for msg_data in messages_data:
                message = Message(
                    id=msg_data["id"],
                    conversation_id=conversation.id,
                    role=msg_data["role"],
                    content=msg_data["content"],
                    agent_id=msg_data.get("agent_id"),
                    turn_number=msg_data.get("turn_number"),
                    meta=msg_data.get("meta"),
                )
                db.add(message)
                imported_counts["messages"] += 1

        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

    return {"status": "success", "imported": imported_counts}


@router.post("/import/agents")
async def import_agents(file: UploadFile, db: AsyncSession = Depends(get_db)):
    """Import agents from JSON file"""
    content = await file.read()
    try:
        data = json.loads(content)
        agents_data = data.get("agents", [])
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid file: {str(e)}")

    if not agents_data:
        raise HTTPException(status_code=400, detail="No agents found in file")

    imported_ids = []

    try:
        for agent_data in agents_data:
            # Check if agent already exists
            existing = await db.execute(
                select(Agent).where(Agent.id == agent_data["id"])
            )
            if existing.scalar_one_or_none():
                # Skip existing agents
                continue

            agent = Agent(
                id=agent_data["id"],
                name=agent_data["name"],
                system_prompt=agent_data["system_prompt"],
                provider_id=agent_data.get("provider_id"),
                model=agent_data.get("model"),
                temperature=agent_data.get("temperature"),
                max_tokens=agent_data.get("max_tokens"),
                color=agent_data.get("color"),
                is_active=agent_data.get("is_active", True),
                meta=agent_data.get("meta"),
            )
            db.add(agent)
            imported_ids.append(agent.id)

        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

    return {"status": "success", "imported_agents": imported_ids}


# Data management endpoints
@router.delete("/data/conversations")
async def clear_all_conversations(db: AsyncSession = Depends(get_db)):
    """
    Delete all conversations and messages
    Keeps agents, providers, and settings intact
    """
    try:
        # Delete messages first (foreign key constraint)
        await db.execute(delete(Message))
        # Delete conversations
        await db.execute(delete(Conversation))
        # Delete conversation memories
        await db.execute(delete(ConversationMemory))
        await db.commit()

        return {"status": "success", "message": "All conversations cleared"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear conversations: {str(e)}")


@router.delete("/data/all")
async def factory_reset(db: AsyncSession = Depends(get_db)):
    """
    Complete factory reset - delete ALL user data
    Recreates default settings after deletion
    """
    try:
        # Delete in order (respect foreign keys)
        await db.execute(delete(Message))
        await db.execute(delete(Conversation))
        await db.execute(delete(ConversationMemory))
        await db.execute(delete(Agent))
        # Keep providers and provider keys (they contain API keys)
        # Users may want to keep their API configuration

        # Reset settings to defaults
        settings_result = await db.execute(select(Settings).where(Settings.id == 1))
        settings = settings_result.scalar_one_or_none()

        if settings:
            await db.delete(settings)

        # Create default settings
        default_settings = Settings(id=1)
        db.add(default_settings)

        await db.commit()

        return {"status": "success", "message": "Factory reset complete"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Factory reset failed: {str(e)}")
