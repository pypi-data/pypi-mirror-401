"""
Analytics router - API endpoints for conversation analytics and metrics
Phase 5: Analytics & Visualization
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from aidiscuss.app.services.analytics_service import (
    analytics_service,
    ConversationAnalytics,
    AgentMetrics,
    CostBreakdown,
    TokenUsage
)

router = APIRouter()


# Request/Response Models

class TrackAPICallRequest(BaseModel):
    """Request model for tracking API call"""
    conversation_id: str
    agent_id: str
    provider_id: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    success: bool = True
    error: Optional[str] = None


class ConversationAnalyticsResponse(BaseModel):
    """Response model for conversation analytics"""
    conversation_id: str
    start_time: str
    end_time: Optional[str]
    total_turns: int
    total_tokens: int
    total_cost_usd: float
    average_latency_ms: float
    agent_participation: Dict[str, int]
    provider_usage: Dict[str, int]
    token_timeline: List[Dict[str, Any]]


class AgentMetricsResponse(BaseModel):
    """Response model for agent metrics"""
    agent_id: str
    total_calls: int
    total_tokens: int
    total_cost_usd: float
    average_tokens_per_call: float
    average_latency_ms: float
    success_rate: float
    conversations: int


class CostBreakdownResponse(BaseModel):
    """Response model for cost breakdown"""
    total_cost_usd: float
    by_provider: Dict[str, float]
    by_model: Dict[str, float]
    by_conversation: Dict[str, float]


class SummaryStatsResponse(BaseModel):
    """Response model for summary statistics"""
    total_calls: int
    total_tokens: int
    total_cost_usd: float
    total_conversations: int
    total_agents: int
    average_latency_ms: float
    success_rate: float


# Endpoints

@router.post("/analytics/track")
async def track_api_call(request: TrackAPICallRequest):
    """
    Track an API call for analytics

    This should be called after each LLM API call to track costs,
    tokens, latency, and other metrics.
    """
    try:
        tokens = TokenUsage(
            prompt_tokens=request.prompt_tokens,
            completion_tokens=request.completion_tokens,
            total_tokens=request.prompt_tokens + request.completion_tokens
        )

        analytics_service.track_api_call(
            conversation_id=request.conversation_id,
            agent_id=request.agent_id,
            provider_id=request.provider_id,
            model=request.model,
            tokens=tokens,
            latency_ms=request.latency_ms,
            success=request.success,
            error=request.error
        )

        return {"status": "tracked", "conversation_id": request.conversation_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking API call: {str(e)}")


@router.get("/analytics/conversation/{conversation_id}", response_model=ConversationAnalyticsResponse)
async def get_conversation_analytics(conversation_id: str):
    """
    Get detailed analytics for a specific conversation

    Returns metrics including token usage, costs, agent participation,
    and timeline data.
    """
    try:
        analytics = analytics_service.get_conversation_analytics(conversation_id)

        if not analytics:
            raise HTTPException(status_code=404, detail=f"No analytics found for conversation {conversation_id}")

        return ConversationAnalyticsResponse(
            conversation_id=analytics.conversation_id,
            start_time=analytics.start_time.isoformat(),
            end_time=analytics.end_time.isoformat() if analytics.end_time else None,
            total_turns=analytics.total_turns,
            total_tokens=analytics.total_tokens,
            total_cost_usd=analytics.total_cost_usd,
            average_latency_ms=analytics.average_latency_ms,
            agent_participation=analytics.agent_participation,
            provider_usage=analytics.provider_usage,
            token_timeline=analytics.token_timeline
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analytics: {str(e)}")


@router.get("/analytics/agent/{agent_id}", response_model=AgentMetricsResponse)
async def get_agent_metrics(agent_id: str):
    """
    Get metrics for a specific agent

    Returns total calls, tokens, costs, and performance metrics.
    """
    try:
        metrics = analytics_service.get_agent_metrics(agent_id)

        if not metrics:
            raise HTTPException(status_code=404, detail=f"No metrics found for agent {agent_id}")

        return AgentMetricsResponse(**metrics.dict())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving agent metrics: {str(e)}")


@router.get("/analytics/costs", response_model=CostBreakdownResponse)
async def get_cost_breakdown(
    start_date: Optional[str] = Query(None, description="ISO format start date"),
    end_date: Optional[str] = Query(None, description="ISO format end date")
):
    """
    Get cost breakdown by provider, model, and conversation

    Optionally filter by date range.
    """
    try:
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        breakdown = analytics_service.get_cost_breakdown(start_dt, end_dt)

        return CostBreakdownResponse(**breakdown.dict())

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cost breakdown: {str(e)}")


@router.get("/analytics/tokens/timeline")
async def get_token_timeline(
    conversation_id: Optional[str] = Query(None, description="Filter by conversation ID"),
    granularity: str = Query("minute", description="Time granularity: minute, hour, or day")
):
    """
    Get token usage timeline

    Returns time-series data showing token usage over time.
    """
    try:
        if granularity not in ["minute", "hour", "day"]:
            raise HTTPException(status_code=400, detail="Granularity must be 'minute', 'hour', or 'day'")

        timeline = analytics_service.get_token_usage_timeline(
            conversation_id=conversation_id,
            granularity=granularity
        )

        return {
            "conversation_id": conversation_id,
            "granularity": granularity,
            "timeline": timeline
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving token timeline: {str(e)}")


@router.get("/analytics/participation")
async def get_agent_participation(
    conversation_id: Optional[str] = Query(None, description="Filter by conversation ID")
):
    """
    Get agent participation statistics

    Shows how many turns each agent took, tokens used, costs, etc.
    """
    try:
        stats = analytics_service.get_agent_participation_stats(conversation_id)

        return {
            "conversation_id": conversation_id,
            "agents": stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving participation stats: {str(e)}")


@router.get("/analytics/summary", response_model=SummaryStatsResponse)
async def get_summary_stats():
    """
    Get overall summary statistics

    Returns aggregate metrics across all conversations and agents.
    """
    try:
        stats = analytics_service.get_summary_stats()

        return SummaryStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving summary stats: {str(e)}")
