"""
RAG Control Router
Endpoints for managing RAG model loading/unloading and status
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Dict

from aidiscuss.app.db.base import get_db
from aidiscuss.app.models.settings import Settings
from aidiscuss.app.services.rag_service import rag_service

router = APIRouter()


class RAGStatusResponse(BaseModel):
    """RAG service status"""

    model_loaded: bool
    is_loading: bool
    load_progress: int
    enabled_in_settings: bool
    namespaces: list[str]


class RAGToggleRequest(BaseModel):
    """Toggle RAG on/off"""

    enabled: bool


class RAGActionResponse(BaseModel):
    """Response from load/unload actions"""

    success: bool
    message: str
    status: Dict


@router.get("/status", response_model=RAGStatusResponse)
async def get_rag_status(db: AsyncSession = Depends(get_db)):
    """Get current RAG service status"""

    # Get RAG status from service
    service_status = rag_service.get_status()

    # Get enabled setting from database
    result = await db.execute(select(Settings).where(Settings.id == 1))
    settings = result.scalar_one_or_none()

    enabled_in_settings = False
    if settings and settings.rag:
        enabled_in_settings = settings.rag.get("enabled", False)

    return RAGStatusResponse(
        model_loaded=service_status["model_loaded"],
        is_loading=service_status["is_loading"],
        load_progress=service_status["load_progress"],
        enabled_in_settings=enabled_in_settings,
        namespaces=service_status["namespaces"],
    )


@router.post("/toggle", response_model=RAGActionResponse)
async def toggle_rag(request: RAGToggleRequest, db: AsyncSession = Depends(get_db)):
    """
    Toggle RAG on/off
    - When enabled=True: loads model and updates settings
    - When enabled=False: unloads model and updates settings
    """

    # Get settings
    result = await db.execute(select(Settings).where(Settings.id == 1))
    settings = result.scalar_one_or_none()

    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")

    # Perform action based on toggle
    if request.enabled:
        # Load model
        load_result = rag_service.load_model()

        if not load_result["success"]:
            return RAGActionResponse(
                success=False,
                message=load_result["message"],
                status=rag_service.get_status(),
            )

        # Update settings
        settings.rag["enabled"] = True
        await db.commit()

        return RAGActionResponse(
            success=True,
            message="RAG enabled and model loaded",
            status=rag_service.get_status(),
        )

    else:
        # Unload model
        unload_result = rag_service.unload_model()

        # Update settings
        settings.rag["enabled"] = False
        await db.commit()

        return RAGActionResponse(
            success=True,
            message="RAG disabled and model unloaded",
            status=rag_service.get_status(),
        )


@router.post("/load", response_model=RAGActionResponse)
async def load_rag_model():
    """Manually load RAG model without changing settings"""

    result = rag_service.load_model()

    return RAGActionResponse(
        success=result["success"],
        message=result["message"],
        status=rag_service.get_status(),
    )


@router.post("/unload", response_model=RAGActionResponse)
async def unload_rag_model():
    """Manually unload RAG model without changing settings"""

    result = rag_service.unload_model()

    return RAGActionResponse(
        success=result["success"],
        message=result["message"],
        status=rag_service.get_status(),
    )


@router.get("/progress")
async def get_load_progress():
    """Get current loading progress (for polling during load)"""
    return {
        "is_loading": rag_service.is_loading(),
        "progress": rag_service.get_load_progress(),
        "model_loaded": rag_service.is_model_loaded(),
    }
