"""
Admin Override API Router

Endpoints for admin control during conversations:
- Submit admin override actions
- Get admin action history
- Toggle System AI mode
- Get current admin status
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from nanoid import generate

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.admin_action import AdminAction, AdminOverrideSchema


router = APIRouter(prefix="/api/admin", tags=["admin"])


# Request models (defined before endpoints)
class RedirectRequest(BaseModel):
    """Request model for redirect endpoint"""
    conversation_id: str
    new_goal: str


class ToggleSystemAIModeRequest(BaseModel):
    """Request model for toggle system AI mode endpoint"""
    conversation_id: str
    mode: str


class KickAgentRequest(BaseModel):
    """Request model for kick agent endpoint"""
    conversation_id: str
    agent_id: str


class InjectContextRequest(BaseModel):
    """Request model for inject context endpoint"""
    conversation_id: str
    context: str


@router.post("/override", response_model=dict)
async def submit_admin_override(
    conversation_id: str,
    action: AdminOverrideSchema,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit admin override action

    Creates an admin action that will be executed in the conversation flow.
    The action is stored in database and can be picked up by the orchestrator.

    Args:
        conversation_id: Conversation to apply action to
        action: Admin override action details
        db: Database session

    Returns:
        Created action with ID

    Raises:
        HTTPException: If validation fails
    """
    # Validate action (basic validation)
    if action.action_type in ["kick_agent", "add_agent"] and not action.target_agent_id:
        raise HTTPException(
            status_code=400,
            detail=f"{action.action_type} requires target_agent_id"
        )

    if action.action_type in ["redirect", "modify_goal"] and not action.new_goal:
        raise HTTPException(
            status_code=400,
            detail=f"{action.action_type} requires new_goal"
        )

    if action.action_type == "inject_context" and not action.injected_context:
        raise HTTPException(
            status_code=400,
            detail="inject_context requires injected_context"
        )

    if action.action_type == "toggle_system_ai_mode" and not action.new_system_ai_mode:
        raise HTTPException(
            status_code=400,
            detail="toggle_system_ai_mode requires new_system_ai_mode"
        )

    # Create admin action record
    admin_action = AdminAction.from_schema(
        conversation_id=conversation_id,
        schema=action,
        action_id=generate(size=12)
    )

    db.add(admin_action)
    await db.commit()
    await db.refresh(admin_action)

    # Note: In a full implementation, this would also inject the action
    # into the running LangGraph orchestrator via a message queue or
    # shared state mechanism

    return {
        "action_id": admin_action.id,
        "conversation_id": admin_action.conversation_id,
        "action_type": admin_action.action_type,
        "executed": admin_action.executed,
        "timestamp": admin_action.timestamp.isoformat(),
        "message": f"Admin action {action.action_type} queued for execution"
    }


@router.get("/actions/{conversation_id}", response_model=List[dict])
async def get_admin_actions(
    conversation_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get admin action history for conversation

    Args:
        conversation_id: Conversation identifier
        limit: Maximum actions to return
        db: Database session

    Returns:
        List of admin actions (newest first)
    """
    result = await db.execute(
        select(AdminAction)
        .where(AdminAction.conversation_id == conversation_id)
        .order_by(AdminAction.timestamp.desc())
        .limit(limit)
    )
    actions = result.scalars().all()

    return [
        {
            "id": action.id,
            "action_type": action.action_type,
            "target_agent_id": action.target_agent_id,
            "new_goal": action.new_goal,
            "injected_context": action.injected_context,
            "new_system_ai_mode": action.new_system_ai_mode,
            "user_id": action.user_id,
            "timestamp": action.timestamp.isoformat(),
            "executed": action.executed,
            "execution_timestamp": action.execution_timestamp.isoformat() if action.execution_timestamp else None,
            "action_metadata": action.action_metadata
        }
        for action in actions
    ]


@router.get("/actions/{conversation_id}/pending", response_model=List[dict])
async def get_pending_admin_actions(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get pending (unexecuted) admin actions

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        List of pending admin actions
    """
    result = await db.execute(
        select(AdminAction)
        .where(
            AdminAction.conversation_id == conversation_id,
            AdminAction.executed == False
        )
        .order_by(AdminAction.timestamp.asc())
    )
    actions = result.scalars().all()

    return [
        {
            "id": action.id,
            "action_type": action.action_type,
            "target_agent_id": action.target_agent_id,
            "new_goal": action.new_goal,
            "timestamp": action.timestamp.isoformat()
        }
        for action in actions
    ]


@router.post("/toggle-system-ai-mode", response_model=dict)
async def toggle_system_ai_mode(
    request: ToggleSystemAIModeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Toggle System AI mode mid-conversation

    Convenience endpoint for toggling System AI between active and passive modes.

    Args:
        request: Toggle request with conversation_id and mode
        db: Database session

    Returns:
        Action confirmation

    Raises:
        HTTPException: If mode invalid
    """
    if request.mode not in ["active", "passive"]:
        raise HTTPException(
            status_code=400,
            detail="Mode must be 'active' or 'passive'"
        )

    # Create toggle action
    action = AdminOverrideSchema(
        action_type="toggle_system_ai_mode",
        new_system_ai_mode=request.mode,
        user_id="admin",
        timestamp=datetime.now()
    )

    admin_action = AdminAction.from_schema(
        conversation_id=request.conversation_id,
        schema=action,
        action_id=generate(size=12)
    )

    db.add(admin_action)
    await db.commit()

    return {
        "action_id": admin_action.id,
        "conversation_id": request.conversation_id,
        "new_mode": request.mode,
        "message": f"System AI mode change to '{request.mode}' queued"
    }


@router.post("/kick-agent", response_model=dict)
async def kick_agent(
    request: KickAgentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Kick agent from conversation

    Convenience endpoint for removing an agent mid-conversation.

    Args:
        request: Kick request with conversation_id and agent_id
        db: Database session

    Returns:
        Action confirmation
    """
    action = AdminOverrideSchema(
        action_type="kick_agent",
        target_agent_id=request.agent_id,
        user_id="admin",
        timestamp=datetime.now()
    )

    admin_action = AdminAction.from_schema(
        conversation_id=request.conversation_id,
        schema=action,
        action_id=generate(size=12)
    )

    db.add(admin_action)
    await db.commit()

    return {
        "action_id": admin_action.id,
        "conversation_id": request.conversation_id,
        "kicked_agent": request.agent_id,
        "message": f"Agent {request.agent_id} removal queued"
    }


@router.post("/redirect", response_model=dict)
async def redirect_conversation(
    request: RedirectRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Redirect conversation to new goal

    Convenience endpoint for changing conversation goal mid-stream.

    Args:
        request: Redirect request with conversation_id and new_goal
        db: Database session

    Returns:
        Action confirmation

    Raises:
        HTTPException: If goal invalid
    """
    if not request.new_goal or len(request.new_goal) < 10:
        raise HTTPException(
            status_code=400,
            detail="New goal must be at least 10 characters"
        )

    action = AdminOverrideSchema(
        action_type="redirect",
        new_goal=request.new_goal,
        user_id="admin",
        timestamp=datetime.now()
    )

    admin_action = AdminAction.from_schema(
        conversation_id=request.conversation_id,
        schema=action,
        action_id=generate(size=12)
    )

    db.add(admin_action)
    await db.commit()

    return {
        "action_id": admin_action.id,
        "conversation_id": request.conversation_id,
        "new_goal": request.new_goal,
        "message": "Conversation redirect queued"
    }


@router.post("/inject-context", response_model=dict)
async def inject_context(
    request: InjectContextRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Inject additional context into conversation

    Convenience endpoint for adding information mid-conversation.

    Args:
        request: Inject request with conversation_id and context
        db: Database session

    Returns:
        Action confirmation

    Raises:
        HTTPException: If context invalid
    """
    if not request.context:
        raise HTTPException(
            status_code=400,
            detail="Context cannot be empty"
        )

    action = AdminOverrideSchema(
        action_type="inject_context",
        injected_context=request.context,
        user_id="admin",
        timestamp=datetime.now()
    )

    admin_action = AdminAction.from_schema(
        conversation_id=request.conversation_id,
        schema=action,
        action_id=generate(size=12)
    )

    db.add(admin_action)
    await db.commit()

    return {
        "action_id": admin_action.id,
        "conversation_id": request.conversation_id,
        "message": "Context injection queued"
    }


@router.get("/status/{conversation_id}", response_model=dict)
async def get_admin_status(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get current admin status for conversation

    Returns statistics about admin actions for this conversation.

    Args:
        conversation_id: Conversation identifier
        db: Database session

    Returns:
        Admin status summary
    """
    # Get all actions
    result = await db.execute(
        select(AdminAction)
        .where(AdminAction.conversation_id == conversation_id)
    )
    actions = result.scalars().all()

    # Calculate stats
    total_actions = len(actions)
    executed_actions = sum(1 for a in actions if a.executed)
    pending_actions = total_actions - executed_actions

    # Count by type
    action_types = {}
    for action in actions:
        action_types[action.action_type] = action_types.get(action.action_type, 0) + 1

    # Get most recent action
    recent_action = None
    if actions:
        sorted_actions = sorted(actions, key=lambda a: a.timestamp, reverse=True)
        most_recent = sorted_actions[0]
        recent_action = {
            "action_type": most_recent.action_type,
            "timestamp": most_recent.timestamp.isoformat(),
            "executed": most_recent.executed
        }

    return {
        "conversation_id": conversation_id,
        "total_actions": total_actions,
        "executed_actions": executed_actions,
        "pending_actions": pending_actions,
        "action_types": action_types,
        "most_recent_action": recent_action
    }
