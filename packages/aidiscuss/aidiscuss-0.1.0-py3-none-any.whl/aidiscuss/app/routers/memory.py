"""
Memory router - API endpoints for conversation memory management
Phase 2: Memory Enhancement
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from aidiscuss.app.services.memory_service import memory_service
from datetime import datetime

router = APIRouter()


# Request/Response Models

class FactCreate(BaseModel):
    """Request model for creating a fact"""
    text: str
    importance: float = Field(ge=0, le=1, default=0.5)
    source_turn: int


class FactResponse(BaseModel):
    """Response model for fact"""
    id: str
    text: str
    importance: float
    source_turn: int
    timestamp: datetime


class CheckpointResponse(BaseModel):
    """Response model for checkpoint"""
    id: str
    turn_number: int
    topic: str
    summary: str
    timestamp: datetime


class MemoryResponse(BaseModel):
    """Response model for conversation memory"""
    conversation_id: str
    rolling_summary: str
    facts: List[FactResponse]
    checkpoints: List[CheckpointResponse]
    last_summary_turn: int
    last_checkpoint_turn: int
    total_tokens: int


class MemoryStatsResponse(BaseModel):
    """Response model for memory statistics"""
    conversation_id: str
    facts_count: int
    checkpoints_count: int
    has_summary: bool
    last_summary_turn: int
    last_checkpoint_turn: int
    total_tokens: int


class ContextRequest(BaseModel):
    """Request model for building context"""
    conversation_id: str
    messages: List[Dict]
    max_tokens: int = 4000


class ContextResponse(BaseModel):
    """Response model for context"""
    system_context: str
    relevant_history: List[Dict]
    facts: List[FactResponse]
    total_tokens: int


# Endpoints

@router.get("/memory/{conversation_id}", response_model=MemoryResponse)
async def get_memory(conversation_id: str):
    """
    Get full memory for a conversation

    Returns all facts, checkpoints, and rolling summary
    """
    try:
        memory = memory_service.get_or_create_memory(conversation_id)

        return MemoryResponse(
            conversation_id=memory.conversation_id,
            rolling_summary=memory.rolling_summary,
            facts=[
                FactResponse(
                    id=f.id,
                    text=f.text,
                    importance=f.importance,
                    source_turn=f.source_turn,
                    timestamp=f.timestamp
                )
                for f in memory.facts
            ],
            checkpoints=[
                CheckpointResponse(
                    id=c.id,
                    turn_number=c.turn_number,
                    topic=c.topic,
                    summary=c.summary,
                    timestamp=c.timestamp
                )
                for c in memory.checkpoints
            ],
            last_summary_turn=memory.last_summary_turn,
            last_checkpoint_turn=memory.last_checkpoint_turn,
            total_tokens=memory.total_tokens
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {str(e)}")


@router.get("/memory/{conversation_id}/stats", response_model=MemoryStatsResponse)
async def get_memory_stats(conversation_id: str):
    """
    Get memory statistics for a conversation

    Returns counts and metadata without full content
    """
    try:
        stats = memory_service.get_memory_stats(conversation_id)
        return MemoryStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")


@router.get("/memory/{conversation_id}/facts", response_model=List[FactResponse])
async def get_facts(conversation_id: str, min_importance: float = 0.0):
    """
    Get facts for a conversation

    Args:
        conversation_id: Conversation ID
        min_importance: Minimum importance threshold (0-1)
    """
    try:
        memory = memory_service.get_or_create_memory(conversation_id)

        facts = [
            f for f in memory.facts
            if f.importance >= min_importance
        ]

        return [
            FactResponse(
                id=f.id,
                text=f.text,
                importance=f.importance,
                source_turn=f.source_turn,
                timestamp=f.timestamp
            )
            for f in facts
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving facts: {str(e)}")


@router.get("/memory/{conversation_id}/summary")
async def get_summary(conversation_id: str):
    """
    Get rolling summary for a conversation
    """
    try:
        memory = memory_service.get_or_create_memory(conversation_id)

        return {
            "conversation_id": conversation_id,
            "summary": memory.rolling_summary,
            "last_updated_turn": memory.last_summary_turn
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving summary: {str(e)}")


@router.get("/memory/{conversation_id}/checkpoints", response_model=List[CheckpointResponse])
async def get_checkpoints(conversation_id: str):
    """
    Get all checkpoints for a conversation

    Returns checkpoints in reverse chronological order (newest first)
    """
    try:
        memory = memory_service.get_or_create_memory(conversation_id)

        # Return in reverse order (newest first)
        checkpoints = sorted(
            memory.checkpoints,
            key=lambda c: c.timestamp,
            reverse=True
        )

        return [
            CheckpointResponse(
                id=c.id,
                turn_number=c.turn_number,
                topic=c.topic,
                summary=c.summary,
                timestamp=c.timestamp
            )
            for c in checkpoints
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving checkpoints: {str(e)}")


@router.post("/memory/{conversation_id}/context", response_model=ContextResponse)
async def build_context(request: ContextRequest):
    """
    Build memory-aware context for agent prompts

    This is used by the frontend to build context before sending messages
    """
    try:
        context = memory_service.build_context(
            request.conversation_id,
            request.messages,
            request.max_tokens
        )

        return ContextResponse(
            system_context=context["system_context"],
            relevant_history=context["relevant_history"],
            facts=[
                FactResponse(
                    id=f.id,
                    text=f.text,
                    importance=f.importance,
                    source_turn=f.source_turn,
                    timestamp=f.timestamp
                )
                for f in context["facts"]
            ],
            total_tokens=context["total_tokens"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building context: {str(e)}")


@router.post("/memory/{conversation_id}/facts", response_model=FactResponse)
async def add_fact(conversation_id: str, fact: FactCreate):
    """
    Manually add a fact to conversation memory

    Useful for user-specified facts or important information
    """
    try:
        import uuid
        from app.services.memory_service import Fact

        memory = memory_service.get_or_create_memory(conversation_id)

        new_fact = Fact(
            id=str(uuid.uuid4()),
            text=fact.text,
            importance=fact.importance,
            source_turn=fact.source_turn,
            timestamp=datetime.now()
        )

        memory.facts.append(new_fact)

        # Prune if needed
        memory_service._prune_facts(memory)

        return FactResponse(
            id=new_fact.id,
            text=new_fact.text,
            importance=new_fact.importance,
            source_turn=new_fact.source_turn,
            timestamp=new_fact.timestamp
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding fact: {str(e)}")


@router.delete("/memory/{conversation_id}/facts/{fact_id}")
async def delete_fact(conversation_id: str, fact_id: str):
    """
    Delete a specific fact from memory
    """
    try:
        memory = memory_service.get_or_create_memory(conversation_id)

        original_count = len(memory.facts)
        memory.facts = [f for f in memory.facts if f.id != fact_id]

        if len(memory.facts) == original_count:
            raise HTTPException(status_code=404, detail="Fact not found")

        return {"message": "Fact deleted successfully", "fact_id": fact_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting fact: {str(e)}")


@router.post("/memory/{conversation_id}/summary/regenerate")
async def regenerate_summary(
    conversation_id: str,
    messages: List[Dict],
    turn_number: int
):
    """
    Manually regenerate rolling summary

    Useful for forcing a summary update
    """
    try:
        summary = await memory_service.generate_summary(
            conversation_id,
            messages,
            turn_number
        )

        return {
            "conversation_id": conversation_id,
            "summary": summary,
            "turn_number": turn_number
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error regenerating summary: {str(e)}")


@router.post("/memory/{conversation_id}/checkpoints/create")
async def create_checkpoint(
    conversation_id: str,
    messages: List[Dict],
    turn_number: int,
    force: bool = False
):
    """
    Manually create a checkpoint

    Args:
        conversation_id: Conversation ID
        messages: All messages
        turn_number: Current turn
        force: Force checkpoint creation even if topic hasn't changed
    """
    try:
        checkpoint = await memory_service.create_checkpoint(
            conversation_id,
            messages,
            turn_number,
            force=force
        )

        if not checkpoint:
            return {
                "message": "No checkpoint created (topic unchanged)",
                "conversation_id": conversation_id
            }

        return CheckpointResponse(
            id=checkpoint.id,
            turn_number=checkpoint.turn_number,
            topic=checkpoint.topic,
            summary=checkpoint.summary,
            timestamp=checkpoint.timestamp
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating checkpoint: {str(e)}")


@router.delete("/memory/{conversation_id}")
async def clear_memory(conversation_id: str):
    """
    Clear all memory for a conversation

    WARNING: This deletes all facts, checkpoints, and summaries
    """
    try:
        if conversation_id in memory_service.memories:
            del memory_service.memories[conversation_id]

        return {
            "message": "Memory cleared successfully",
            "conversation_id": conversation_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")
