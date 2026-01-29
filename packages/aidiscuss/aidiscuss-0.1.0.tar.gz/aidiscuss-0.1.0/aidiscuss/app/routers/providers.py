"""
Provider management router with caching
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.provider import Provider
from aidiscuss.app.services.cache import cache
from aidiscuss.app.services.broadcast import broadcast_service

router = APIRouter()


class ModelPricing(BaseModel):
    """Per-model pricing (per 1M tokens)"""

    input: float
    output: float


class ModelMetadata(BaseModel):
    """Model metadata"""

    id: str
    name: str
    contextLength: int = Field(alias="context_length")
    supportsTools: bool = Field(alias="supports_tools")
    costTier: str = Field(alias="cost_tier")
    isDefault: bool = Field(default=False, alias="is_default")
    pricing: ModelPricing


class ProviderCapabilities(BaseModel):
    """Provider capabilities"""

    supportsStreaming: bool = Field(alias="supports_streaming")
    supportsTools: bool = Field(alias="supports_tools")
    supportsVision: bool = Field(default=False, alias="supports_vision")
    corsOk: bool = Field(default=False, alias="cors_ok")


class ProviderMetadata(BaseModel):
    """Provider metadata structure"""

    models: List[ModelMetadata]
    capabilities: ProviderCapabilities


class ProviderUpdate(BaseModel):
    """Provider update request - for API key and metadata changes only"""

    api_key: str | None = None
    is_active: bool | None = None
    meta: ProviderMetadata | None = Field(default=None, alias="metadata")


class ProviderResponse(BaseModel):
    """Provider response (without API key)"""

    id: str
    name: str
    base_url: str | None
    is_active: bool
    has_api_key: bool  # Whether an API key is set (don't expose the key itself)
    metadata: Dict[str, Any] | None = None
    created_at: str
    updated_at: str | None

    @classmethod
    def from_orm(cls, provider: Provider):
        """Convert Provider model to response"""
        return cls(
            id=provider.id,
            name=provider.name,
            base_url=provider.base_url,
            is_active=provider.is_active,
            has_api_key=provider.api_key_encrypted is not None,
            metadata=provider.meta,
            created_at=provider.created_at.isoformat() if provider.created_at else "",
            updated_at=provider.updated_at.isoformat() if provider.updated_at else None,
        )


@router.get("", response_model=list[ProviderResponse])
async def list_providers(db: AsyncSession = Depends(get_db)):
    """List all providers"""
    result = await db.execute(select(Provider))
    providers = result.scalars().all()

    return [ProviderResponse.from_orm(p) for p in providers]


@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(provider_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific provider (with caching)"""
    # Check cache first
    cached = cache.get_provider(provider_id)
    if cached:
        provider = cached
    else:
        # Query database
        result = await db.execute(select(Provider).where(Provider.id == provider_id))
        provider = result.scalar_one_or_none()

        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")

        # Cache the result
        cache.set_provider(provider)

    return ProviderResponse.from_orm(provider)


@router.patch("/{provider_id}", response_model=ProviderResponse)
async def update_provider(
    provider_id: str,
    provider_data: ProviderUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Update provider - can update API key, activation status, and models list.
    Note: Cannot delete/modify default models (isDefault=True), only add custom models.
    """
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # Update API key if provided
    if provider_data.api_key is not None:
        provider.set_api_key(provider_data.api_key)

    # Update activation status if provided
    if provider_data.is_active is not None:
        provider.is_active = provider_data.is_active

    # Update metadata (models list) if provided
    if provider_data.meta is not None:
        new_meta = provider_data.meta.model_dump(by_alias=True)

        # Validate that default models are not deleted/modified
        if provider.meta and "models" in provider.meta:
            existing_models = provider.meta.get("models", [])
            new_models = new_meta.get("models", [])

            # Check all default models are still present and unmodified
            for existing_model in existing_models:
                if existing_model.get("isDefault", False):
                    # Find this model in new models list
                    found = next((m for m in new_models if m["id"] == existing_model["id"]), None)
                    if not found:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Cannot delete default model: {existing_model['id']}"
                        )
                    # Ensure default model properties are not modified
                    for key in ["name", "contextLength", "supportsTools", "costTier", "pricing", "isDefault"]:
                        if found.get(key) != existing_model.get(key):
                            raise HTTPException(
                                status_code=400,
                                detail=f"Cannot modify default model properties: {existing_model['id']}"
                            )

        provider.meta = new_meta

    await db.commit()
    await db.refresh(provider)

    # Invalidate cache in background
    background_tasks.add_task(cache.invalidate_provider, provider_id)

    response = ProviderResponse.from_orm(provider)

    # Broadcast to all clients
    background_tasks.add_task(broadcast_service.broadcast_provider_updated, response.model_dump())

    return response


@router.post("/{provider_id}/validate-model")
async def validate_model(provider_id: str, model_id: str, db: AsyncSession = Depends(get_db)):
    """
    Validate if model is listed for provider.
    Returns warning but allows creation (hybrid validation).
    """
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    if not provider.meta or "models" not in provider.meta:
        return {"listed": False, "warning": "Provider has no model metadata", "available_models": []}

    models = provider.meta.get("models", [])
    is_listed = any(m.get("id") == model_id for m in models)

    return {
        "listed": is_listed,
        "warning": f"Model '{model_id}' not in provider's list" if not is_listed else None,
        "available_models": [m.get("id") for m in models],
    }
