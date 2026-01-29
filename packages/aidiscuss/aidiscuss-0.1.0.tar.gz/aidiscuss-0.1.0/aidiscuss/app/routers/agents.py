"""
Agent management router with caching
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Any
from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.agent import Agent
from aidiscuss.app.services.cache import cache
from aidiscuss.app.services.broadcast import broadcast_service

router = APIRouter()


class AgentCreate(BaseModel):
    """Agent creation request"""

    id: str
    name: str
    system_prompt: str
    provider_id: str
    model: str
    temperature: str = "0.7"
    max_tokens: str | None = None
    color: str = "#3B82F6"
    avatar: str | None = None
    is_active: bool = True
    meta: dict[str, Any] | None = Field(default=None, alias="metadata")


class AgentUpdate(BaseModel):
    """Agent update request"""

    name: str | None = None
    system_prompt: str | None = None
    provider_id: str | None = None
    model: str | None = None
    temperature: str | None = None
    max_tokens: str | None = None
    color: str | None = None
    avatar: str | None = None
    is_active: bool | None = None
    meta: dict[str, Any] | None = Field(default=None, alias="metadata")


class AgentResponse(BaseModel):
    """Agent response - consistent snake_case"""

    id: str
    name: str
    system_prompt: str
    provider_id: str
    model: str
    temperature: str
    max_tokens: str | None
    color: str
    avatar: str | None
    is_active: bool
    metadata: dict[str, Any] | None = None
    created_at: str
    updated_at: str | None

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm(cls, agent: Agent):
        """Convert Agent model to response"""
        return cls(
            id=agent.id,
            name=agent.name,
            system_prompt=agent.system_prompt,
            provider_id=agent.provider_id,
            model=agent.model,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
            color=agent.color,
            avatar=agent.avatar,
            is_active=agent.is_active,
            metadata=agent.meta,
            created_at=agent.created_at.isoformat() if agent.created_at else "",
            updated_at=agent.updated_at.isoformat() if agent.updated_at else None,
        )


@router.get("", response_model=list[AgentResponse])
async def list_agents(db: AsyncSession = Depends(get_db)):
    """List all agents"""
    result = await db.execute(select(Agent))
    agents = result.scalars().all()
    return [AgentResponse.from_orm(agent) for agent in agents]


@router.post("", response_model=AgentResponse, status_code=201)
async def create_agent(
    agent_data: AgentCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    """Create a new agent"""
    # Check if agent with this ID already exists
    result = await db.execute(select(Agent).where(Agent.id == agent_data.id))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400, detail=f"Agent with ID '{agent_data.id}' already exists"
        )

    # Map incoming `metadata` to the SQLAlchemy `meta` attribute
    payload = agent_data.model_dump()
    if "metadata" in payload:
        payload["meta"] = payload.pop("metadata")

    agent = Agent(**payload)
    db.add(agent)
    await db.commit()
    await db.refresh(agent)

    # Broadcast to all clients
    response = AgentResponse.from_orm(agent)
    background_tasks.add_task(
        broadcast_service.broadcast_agent_created,
        response.model_dump(),
    )

    return response


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific agent (with caching)"""
    # Check cache first
    cached = cache.get_agent(agent_id)
    if cached:
        return cached

    # Query database
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Cache and return as response
    response = AgentResponse.from_orm(agent)
    cache.set_agent(agent)
    return response


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Update an agent"""
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    update_data = agent_data.model_dump(exclude_unset=True)
    # map incoming `metadata` to `meta` attribute used by SQLAlchemy models
    if "metadata" in update_data:
        update_data["meta"] = update_data.pop("metadata")

    for key, value in update_data.items():
        setattr(agent, key, value)

    await db.commit()
    await db.refresh(agent)

    # Invalidate cache in background
    background_tasks.add_task(cache.invalidate_agent, agent_id)

    # Broadcast to all clients
    response = AgentResponse.from_orm(agent)
    background_tasks.add_task(
        broadcast_service.broadcast_agent_updated,
        response.model_dump(),
    )

    return response


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(
    agent_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Delete an agent"""
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    await db.delete(agent)
    await db.commit()

    # Invalidate cache in background
    background_tasks.add_task(cache.invalidate_agent, agent_id)

    # Broadcast to all clients
    background_tasks.add_task(broadcast_service.broadcast_agent_deleted, agent_id)
