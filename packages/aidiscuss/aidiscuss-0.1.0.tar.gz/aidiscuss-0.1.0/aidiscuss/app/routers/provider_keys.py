from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.provider_key import ProviderKey
from aidiscuss.app.services.broadcast import broadcast_service

router = APIRouter()


# Pydantic schemas
class RateLimit(BaseModel):
    rpm: int = Field(..., description="Requests per minute")
    tpm: int = Field(..., description="Tokens per minute")


class Usage(BaseModel):
    tokensToday: int = 0
    requestsToday: int = 0
    totalTokens: int = 0
    totalRequests: int = 0
    estimatedCost: float = 0.0


class ProviderKeyCreate(BaseModel):
    """Provider key creation - consistent snake_case"""
    provider: str
    key: str
    label: str
    rate_limit: RateLimit
    daily_token_cap: int
    metadata: dict | None = None
    notes: str | None = None


class ProviderKeyUpdate(BaseModel):
    """Provider key update - consistent snake_case"""
    label: str | None = None
    rate_limit: RateLimit | None = None
    daily_token_cap: int | None = None
    enabled: bool | None = None
    metadata: dict | None = None
    notes: str | None = None


class UsageUpdate(BaseModel):
    tokens: int
    requests: int
    cost: float = 0.0


class ProviderKeyResponse(BaseModel):
    """Provider key response - consistent snake_case"""
    id: str
    provider: str
    key: str
    label: str
    rate_limit: dict
    daily_token_cap: int
    enabled: bool
    metadata: dict | None
    notes: str | None
    last_used: str | None
    usage: dict
    created_at: str
    updated_at: str | None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, db_obj: ProviderKey):
        return cls(
            id=db_obj.id,
            provider=db_obj.provider,
            key=db_obj.get_decrypted_key(),  # Decrypt key for API response
            label=db_obj.label,
            rate_limit=db_obj.rate_limit,
            daily_token_cap=db_obj.daily_token_cap,
            enabled=db_obj.enabled,
            metadata=db_obj.extra_metadata,
            notes=db_obj.notes,
            last_used=db_obj.last_used.isoformat() if db_obj.last_used else None,
            usage=db_obj.usage,
            created_at=db_obj.created_at.isoformat() if db_obj.created_at else "",
            updated_at=db_obj.updated_at.isoformat() if db_obj.updated_at else None,
        )


@router.get("", response_model=List[ProviderKeyResponse])
async def list_provider_keys(
    provider: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all provider keys, optionally filtered by provider.
    """
    query = select(ProviderKey)
    if provider:
        query = query.where(ProviderKey.provider == provider)

    result = await db.execute(query)
    keys = result.scalars().all()

    return [ProviderKeyResponse.from_orm(key) for key in keys]


@router.post("", response_model=ProviderKeyResponse, status_code=201)
async def create_provider_key(
    key_data: ProviderKeyCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new provider key.
    """
    import uuid

    provider_key = ProviderKey(
        id=str(uuid.uuid4()),
        provider=key_data.provider,
        key=key_data.key,
        label=key_data.label,
        rate_limit=key_data.rate_limit.model_dump(),
        daily_token_cap=key_data.daily_token_cap,
        enabled=True,
        extra_metadata=key_data.metadata,
        notes=key_data.notes,
        usage={
            "tokensToday": 0,
            "requestsToday": 0,
            "totalTokens": 0,
            "totalRequests": 0,
            "estimatedCost": 0.0
        }
    )

    db.add(provider_key)
    await db.commit()
    await db.refresh(provider_key)

    # Broadcast to all clients
    response = ProviderKeyResponse.from_orm(provider_key)
    background_tasks.add_task(
        broadcast_service.broadcast_provider_key_created,
        response.model_dump()
    )

    return response


@router.get("/{key_id}", response_model=ProviderKeyResponse)
async def get_provider_key(
    key_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific provider key by ID.
    """
    result = await db.execute(
        select(ProviderKey).where(ProviderKey.id == key_id)
    )
    provider_key = result.scalar_one_or_none()

    if not provider_key:
        raise HTTPException(status_code=404, detail="Provider key not found")

    return ProviderKeyResponse.from_orm(provider_key)


@router.patch("/{key_id}", response_model=ProviderKeyResponse)
async def update_provider_key(
    key_id: str,
    key_data: ProviderKeyUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a provider key.
    """
    result = await db.execute(
        select(ProviderKey).where(ProviderKey.id == key_id)
    )
    provider_key = result.scalar_one_or_none()

    if not provider_key:
        raise HTTPException(status_code=404, detail="Provider key not found")

    # Update fields - now using consistent snake_case
    update_data = key_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "rate_limit":
            provider_key.rate_limit = value.model_dump() if hasattr(value, 'model_dump') else value
        elif field == "daily_token_cap":
            provider_key.daily_token_cap = value
        elif field == "metadata":
            provider_key.extra_metadata = value
        else:
            setattr(provider_key, field, value)

    await db.commit()
    await db.refresh(provider_key)

    # Broadcast to all clients
    response = ProviderKeyResponse.from_orm(provider_key)
    background_tasks.add_task(
        broadcast_service.broadcast_provider_key_updated,
        response.model_dump()
    )

    return response


@router.delete("/{key_id}", status_code=204)
async def delete_provider_key(
    key_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a provider key.
    """
    result = await db.execute(
        select(ProviderKey).where(ProviderKey.id == key_id)
    )
    provider_key = result.scalar_one_or_none()

    if not provider_key:
        raise HTTPException(status_code=404, detail="Provider key not found")

    await db.delete(provider_key)
    await db.commit()

    # Broadcast to all clients
    background_tasks.add_task(
        broadcast_service.broadcast_provider_key_deleted,
        key_id
    )

    return None


@router.post("/{key_id}/toggle", response_model=ProviderKeyResponse)
async def toggle_provider_key(
    key_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Toggle the enabled status of a provider key.
    """
    result = await db.execute(
        select(ProviderKey).where(ProviderKey.id == key_id)
    )
    provider_key = result.scalar_one_or_none()

    if not provider_key:
        raise HTTPException(status_code=404, detail="Provider key not found")

    provider_key.enabled = not provider_key.enabled

    await db.commit()
    await db.refresh(provider_key)

    # Broadcast to all clients
    response = ProviderKeyResponse.from_orm(provider_key)
    background_tasks.add_task(
        broadcast_service.broadcast_provider_key_updated,
        response.model_dump()
    )

    return response


@router.post("/{key_id}/usage", response_model=ProviderKeyResponse)
async def update_key_usage(
    key_id: str,
    usage_data: UsageUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Update usage statistics for a provider key.
    """
    result = await db.execute(
        select(ProviderKey).where(ProviderKey.id == key_id)
    )
    provider_key = result.scalar_one_or_none()

    if not provider_key:
        raise HTTPException(status_code=404, detail="Provider key not found")

    # Update usage statistics
    current_usage = provider_key.usage
    current_usage["tokensToday"] += usage_data.tokens
    current_usage["requestsToday"] += usage_data.requests
    current_usage["totalTokens"] += usage_data.tokens
    current_usage["totalRequests"] += usage_data.requests
    current_usage["estimatedCost"] += usage_data.cost

    provider_key.usage = current_usage
    provider_key.last_used = datetime.now()

    await db.commit()
    await db.refresh(provider_key)

    # Broadcast to all clients
    response = ProviderKeyResponse.from_orm(provider_key)
    background_tasks.add_task(
        broadcast_service.broadcast_provider_key_updated,
        response.model_dump()
    )

    return response


@router.post("/{key_id}/reset-daily", response_model=ProviderKeyResponse)
async def reset_daily_usage(
    key_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Reset daily usage counters for a provider key.
    """
    result = await db.execute(
        select(ProviderKey).where(ProviderKey.id == key_id)
    )
    provider_key = result.scalar_one_or_none()

    if not provider_key:
        raise HTTPException(status_code=404, detail="Provider key not found")

    # Reset daily counters
    current_usage = provider_key.usage
    current_usage["tokensToday"] = 0
    current_usage["requestsToday"] = 0
    provider_key.usage = current_usage

    await db.commit()
    await db.refresh(provider_key)

    # Broadcast to all clients
    response = ProviderKeyResponse.from_orm(provider_key)
    background_tasks.add_task(
        broadcast_service.broadcast_provider_key_updated,
        response.model_dump()
    )

    return response
