"""
Offline router - API endpoints for offline/local model management
Phase 6: Offline Capabilities
"""

from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio
from aidiscuss.app.services.offline_service import (
    offline_service,
    LocalModel,
    OllamaModelInfo,
    ModelPullProgress
)

router = APIRouter()


# Request/Response Models

class ModelPullRequest(BaseModel):
    """Request model for pulling a model"""
    model_name: str


class ModelPullResponse(BaseModel):
    """Response model for model pull operation"""
    success: bool
    model_name: str
    message: str


class ModelDeleteResponse(BaseModel):
    """Response model for model deletion"""
    success: bool
    model_name: str
    message: str


class LocalModelResponse(BaseModel):
    """Response model for local model"""
    name: str
    size: str
    modified_at: str
    digest: str
    details: Dict[str, Any]


class OllamaModelInfoResponse(BaseModel):
    """Response model for detailed model info"""
    name: str
    model: str
    size: int
    digest: str
    modified_at: str
    format: str
    family: str
    families: Optional[List[str]]
    parameter_size: str
    quantization_level: str


class OfflineStatusResponse(BaseModel):
    """Response model for offline status"""
    ollama_available: bool
    ollama_url: str
    local_models_count: int
    local_models: List[Dict[str, str]]
    recommended_models: List[Dict[str, str]]
    can_run_offline: bool


class RecommendedModelResponse(BaseModel):
    """Response model for recommended model"""
    name: str
    size: str
    description: str
    category: str


class CompletionRequest(BaseModel):
    """Request model for local completion generation"""
    model: str
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False


class CompletionResponse(BaseModel):
    """Response model for completion"""
    response: str
    model: str
    context: List[int]
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    eval_count: int


# Endpoints

@router.get("/offline/status", response_model=OfflineStatusResponse)
async def get_offline_status():
    """
    Get comprehensive offline capabilities status

    Returns information about Ollama availability, installed models,
    and recommendations for offline use.
    """
    try:
        status = await offline_service.get_offline_status()

        return OfflineStatusResponse(**status)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving offline status: {str(e)}")


@router.get("/offline/models", response_model=List[LocalModelResponse])
async def list_local_models(force_refresh: bool = Query(False, description="Force refresh from Ollama")):
    """
    List all locally available Ollama models

    Args:
        force_refresh: Force refresh from Ollama API instead of using cache

    Returns:
        List of local models with metadata
    """
    try:
        models = await offline_service.list_local_models(force_refresh=force_refresh)

        return [
            LocalModelResponse(
                name=model.name,
                size=model.size,
                modified_at=model.modified_at.isoformat(),
                digest=model.digest,
                details=model.details
            )
            for model in models
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing local models: {str(e)}")


@router.get("/offline/models/{model_name}", response_model=OllamaModelInfoResponse)
async def get_model_info(model_name: str):
    """
    Get detailed information about a specific model

    Args:
        model_name: Name of the model

    Returns:
        Detailed model information including format, family, parameters, etc.
    """
    try:
        model_info = await offline_service.get_model_info(model_name)

        if not model_info:
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")

        return OllamaModelInfoResponse(
            name=model_info.name,
            model=model_info.model,
            size=model_info.size,
            digest=model_info.digest,
            modified_at=model_info.modified_at,
            format=model_info.format,
            family=model_info.family,
            families=model_info.families,
            parameter_size=model_info.parameter_size,
            quantization_level=model_info.quantization_level
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving model info: {str(e)}")


@router.post("/offline/models/pull", response_model=ModelPullResponse)
async def pull_model(request: ModelPullRequest):
    """
    Pull a model from Ollama registry

    This endpoint initiates a model download. For large models, this may take
    significant time. Progress tracking is not yet implemented via websockets.

    Args:
        request: Model pull request with model_name

    Returns:
        Pull operation result
    """
    try:
        # Check if Ollama is available
        if not await offline_service.check_ollama_available():
            raise HTTPException(
                status_code=503,
                detail="Ollama is not available. Please ensure Ollama is running."
            )

        success = await offline_service.pull_model(
            model_name=request.model_name,
            progress_callback=None  # TODO: Implement websocket progress tracking
        )

        if success:
            return ModelPullResponse(
                success=True,
                model_name=request.model_name,
                message=f"Successfully pulled model '{request.model_name}'"
            )
        else:
            return ModelPullResponse(
                success=False,
                model_name=request.model_name,
                message=f"Failed to pull model '{request.model_name}'"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error pulling model: {str(e)}")


@router.delete("/offline/models/{model_name}", response_model=ModelDeleteResponse)
async def delete_model(model_name: str):
    """
    Delete a local model

    Args:
        model_name: Name of model to delete

    Returns:
        Deletion result
    """
    try:
        success = await offline_service.delete_model(model_name)

        if success:
            return ModelDeleteResponse(
                success=True,
                model_name=model_name,
                message=f"Successfully deleted model '{model_name}'"
            )
        else:
            return ModelDeleteResponse(
                success=False,
                model_name=model_name,
                message=f"Failed to delete model '{model_name}'"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting model: {str(e)}")


@router.get("/offline/recommended", response_model=List[RecommendedModelResponse])
async def get_recommended_models():
    """
    Get list of recommended models for offline use

    Returns curated list of models optimized for local execution,
    with size and capability trade-offs.

    Returns:
        List of recommended models with descriptions
    """
    try:
        models = offline_service.get_recommended_models()

        return [
            RecommendedModelResponse(**model)
            for model in models
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recommendations: {str(e)}")


@router.post("/offline/generate")
async def generate_completion(request: CompletionRequest):
    """
    Generate completion using local Ollama model

    This endpoint uses locally installed Ollama models to generate completions
    without requiring internet connectivity or API keys.

    Supports both streaming and non-streaming modes.

    Args:
        request: Completion request with model, prompt, and parameters

    Returns:
        Generated completion with metadata (or StreamingResponse if stream=True)
    """
    try:
        # Check if Ollama is available
        if not await offline_service.check_ollama_available():
            raise HTTPException(
                status_code=503,
                detail="Ollama is not available. Please ensure Ollama is running."
            )

        # Handle streaming mode
        if request.stream:
            async def stream_generator():
                try:
                    async for chunk in offline_service.generate_completion_stream(
                        model=request.model,
                        prompt=request.prompt,
                        system=request.system,
                        temperature=request.temperature,
                        max_tokens=request.max_tokens
                    ):
                        # Format as server-sent events
                        yield f"data: {json.dumps(chunk)}\n\n"
                except Exception as e:
                    error_chunk = {"error": str(e)}
                    yield f"data: {json.dumps(error_chunk)}\n\n"
                finally:
                    yield "data: [DONE]\n\n"

            return StreamingResponse(
                stream_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )

        # Handle non-streaming mode
        result = await offline_service.generate_completion(
            model=request.model,
            prompt=request.prompt,
            system=request.system,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return CompletionResponse(
            response=result.get("response", ""),
            model=result.get("model", request.model),
            context=result.get("context", []),
            total_duration=result.get("total_duration", 0),
            load_duration=result.get("load_duration", 0),
            prompt_eval_count=result.get("prompt_eval_count", 0),
            eval_count=result.get("eval_count", 0)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating completion: {str(e)}")


@router.get("/offline/check")
async def check_ollama():
    """
    Quick check if Ollama is running and accessible

    Returns:
        Simple availability status
    """
    try:
        available = await offline_service.check_ollama_available()

        return {
            "available": available,
            "url": offline_service.ollama_base_url,
            "message": "Ollama is running" if available else "Ollama is not accessible"
        }

    except Exception as e:
        return {
            "available": False,
            "url": offline_service.ollama_base_url,
            "message": f"Error checking Ollama: {str(e)}"
        }


@router.websocket("/offline/pull/stream")
async def pull_model_stream(websocket: WebSocket):
    """
    WebSocket endpoint for streaming model pull progress

    Provides real-time progress updates during model download
    """
    await websocket.accept()

    try:
        # Receive model name
        data = await websocket.receive_json()
        model_name = data.get("model_name")

        if not model_name:
            await websocket.send_json({
                "type": "error",
                "error": "model_name is required"
            })
            await websocket.close()
            return

        # Check Ollama availability
        if not await offline_service.check_ollama_available():
            await websocket.send_json({
                "type": "error",
                "error": "Ollama is not available. Please ensure Ollama is running."
            })
            await websocket.close()
            return

        # Define progress callback
        async def progress_callback(progress: ModelPullProgress):
            """Send progress updates via WebSocket"""
            try:
                await websocket.send_json({
                    "type": "progress",
                    "status": progress.status,
                    "digest": progress.digest,
                    "total": progress.total,
                    "completed": progress.completed,
                    "progress_percent": (progress.completed / progress.total * 100) if progress.total > 0 else 0
                })
            except Exception as e:
                print(f"Error sending progress update: {e}")

        # Start model pull with progress callback
        await websocket.send_json({
            "type": "start",
            "model_name": model_name,
            "message": f"Starting pull for model '{model_name}'"
        })

        success = await offline_service.pull_model(
            model_name=model_name,
            progress_callback=progress_callback
        )

        # Send completion message
        if success:
            await websocket.send_json({
                "type": "complete",
                "success": True,
                "model_name": model_name,
                "message": f"Successfully pulled model '{model_name}'"
            })
        else:
            await websocket.send_json({
                "type": "complete",
                "success": False,
                "model_name": model_name,
                "message": f"Failed to pull model '{model_name}'"
            })

    except WebSocketDisconnect:
        print("WebSocket disconnected during model pull")
    except Exception as e:
        print(f"Error in model pull WebSocket: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "error": str(e)
            })
        except (WebSocketDisconnect, RuntimeError) as send_error:
            print(f"Could not send error message: {send_error}")
        try:
            await websocket.close()
        except (WebSocketDisconnect, RuntimeError) as close_error:
            print(f"Could not close websocket: {close_error}")
