"""
Settings management router with real-time sync
Manages application-wide settings as a singleton
"""

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Any
from datetime import datetime

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.settings import Settings
from aidiscuss.app.services.broadcast import broadcast_service

router = APIRouter()


# Pydantic models
class AppearanceSettings(BaseModel):
    """Appearance settings"""

    theme: str = "system"
    density: str = "comfortable"
    fontSize: str = "medium"


class SafetySettings(BaseModel):
    """Safety settings"""

    enabled: bool = True
    strictness: str = "medium"
    toxicityDetection: bool = False


class ModelsSettings(BaseModel):
    """Models settings"""

    preset: str = "standard"
    primaryProvider: str = "openai"
    apiKeys: dict[str, str] = {}


class StorageSettings(BaseModel):
    """Storage settings"""

    encrypted: bool = True


class RAGSettings(BaseModel):
    """RAG settings"""

    chunkSize: int = 1000
    chunkOverlap: int = 200
    maxResults: int = 5
    minRelevance: float = 0.7


class SettingsUpdate(BaseModel):
    """Request model for updating settings (partial)"""

    appearance: AppearanceSettings | None = None
    safety: SafetySettings | None = None
    models: ModelsSettings | None = None
    storage: StorageSettings | None = None
    rag: RAGSettings | None = None


class SettingsResponse(BaseModel):
    """Response model for settings"""

    id: int
    appearance: dict[str, Any]
    safety: dict[str, Any]
    models: dict[str, Any]
    storage: dict[str, Any]
    rag: dict[str, Any]
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


async def get_or_create_settings(db: AsyncSession) -> Settings:
    """Get settings or create default if not exists (singleton pattern)"""
    result = await db.execute(select(Settings).where(Settings.id == 1))
    settings = result.scalar_one_or_none()

    if not settings:
        # Create default settings
        settings = Settings(
            id=1,
            appearance={"theme": "system", "density": "comfortable", "fontSize": "medium"},
            safety={"enabled": True, "strictness": "medium", "toxicityDetection": False},
            models={"preset": "standard", "primaryProvider": "openai", "apiKeys": {}},
            storage={"encrypted": True},
            rag={"chunkSize": 1000, "chunkOverlap": 200, "maxResults": 5, "minRelevance": 0.7},
        )
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    return settings


@router.get("", response_model=SettingsResponse)
async def get_settings(db: AsyncSession = Depends(get_db)):
    """Get application settings (singleton)"""
    settings = await get_or_create_settings(db)
    return settings


@router.patch("", response_model=SettingsResponse)
async def update_settings(
    data: SettingsUpdate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    """Update application settings (partial update)"""
    settings = await get_or_create_settings(db)

    # Update only provided fields
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if value is not None:
            # Merge with existing data for nested updates
            current_value = getattr(settings, key)
            if isinstance(current_value, dict) and isinstance(value, dict):
                # Merge dictionaries
                merged = {**current_value, **value}
                setattr(settings, key, merged)
            else:
                setattr(settings, key, value)

    await db.commit()
    await db.refresh(settings)

    # Broadcast to all clients
    background_tasks.add_task(
        broadcast_service.broadcast_settings_updated,
        {
            "id": settings.id,
            "appearance": settings.appearance,
            "safety": settings.safety,
            "models": settings.models,
            "storage": settings.storage,
            "rag": settings.rag,
            "created_at": settings.created_at.isoformat(),
            "updated_at": settings.updated_at.isoformat() if settings.updated_at else None,
        },
    )

    return settings


@router.post("/reset", response_model=SettingsResponse)
async def reset_settings(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Reset settings to defaults"""
    result = await db.execute(select(Settings).where(Settings.id == 1))
    settings = result.scalar_one_or_none()

    if settings:
        await db.delete(settings)
        await db.commit()

    # Create new default settings
    settings = await get_or_create_settings(db)

    # Broadcast to all clients
    background_tasks.add_task(
        broadcast_service.broadcast_settings_updated,
        {
            "id": settings.id,
            "appearance": settings.appearance,
            "safety": settings.safety,
            "models": settings.models,
            "storage": settings.storage,
            "rag": settings.rag,
            "created_at": settings.created_at.isoformat(),
            "updated_at": settings.updated_at.isoformat() if settings.updated_at else None,
        },
    )

    return settings
