"""
Quality/Persona router - API endpoints for conversation quality metrics
Phase 3: Persona Consistency
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from aidiscuss.app.services.persona_service import persona_service

router = APIRouter()


# Response Models

class ConsistencyScoreResponse(BaseModel):
    """Response model for consistency score"""
    score: float
    prompt_to_line_score: float
    line_to_line_score: float
    feedback: str
    violations: List[str]


class DiversityMetricsResponse(BaseModel):
    """Response model for diversity metrics"""
    response_similarity: float
    topic_diversity: float
    opinion_diversity: float
    suggestions: List[str]


class QualityMetricsResponse(BaseModel):
    """Response model for overall quality metrics"""
    conversation_id: str
    consistency: Dict
    diversity: Dict
    overall_quality: float


# Endpoints

@router.get("/quality/{conversation_id}", response_model=QualityMetricsResponse)
async def get_quality_metrics(conversation_id: str, agent_id: Optional[str] = None):
    """
    Get comprehensive quality metrics for a conversation

    Returns consistency scores, diversity metrics, and overall quality
    """
    try:
        metrics = await persona_service.get_conversation_quality_metrics(
            conversation_id,
            agent_id
        )

        return QualityMetricsResponse(**metrics)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quality metrics: {str(e)}")


@router.get("/quality/{conversation_id}/consistency", response_model=Dict[str, ConsistencyScoreResponse])
async def get_consistency_scores(conversation_id: str):
    """
    Get persona consistency scores for all agents in a conversation
    """
    try:
        if conversation_id not in persona_service.consistency_history:
            return {}

        # Get latest scores for each agent
        results = {}
        for agent_id in persona_service.consistency_history.keys():
            scores = persona_service.consistency_history[agent_id]
            if scores:
                latest = scores[-1]
                results[agent_id] = ConsistencyScoreResponse(
                    score=latest.score,
                    prompt_to_line_score=latest.prompt_to_line_score,
                    line_to_line_score=latest.line_to_line_score,
                    feedback=latest.feedback,
                    violations=latest.violations
                )

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving consistency scores: {str(e)}")


@router.get("/quality/{conversation_id}/diversity", response_model=DiversityMetricsResponse)
async def get_diversity_metrics(conversation_id: str):
    """
    Get diversity metrics for a conversation
    """
    try:
        if conversation_id not in persona_service.diversity_history:
            raise HTTPException(status_code=404, detail="No diversity metrics found for this conversation")

        # Get latest diversity metrics
        latest = persona_service.diversity_history[conversation_id][-1]

        return DiversityMetricsResponse(
            response_similarity=latest.response_similarity,
            topic_diversity=latest.topic_diversity,
            opinion_diversity=latest.opinion_diversity,
            suggestions=latest.suggestions
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving diversity metrics: {str(e)}")


@router.get("/quality/{conversation_id}/suggestions")
async def get_improvement_suggestions(conversation_id: str, agent_id: Optional[str] = None):
    """
    Get actionable suggestions for improving conversation quality

    Args:
        conversation_id: Conversation ID
        agent_id: Specific agent (optional)
    """
    try:
        suggestions = persona_service.get_improvement_suggestions(
            conversation_id,
            agent_id
        )

        return {
            "conversation_id": conversation_id,
            "agent_id": agent_id,
            "suggestions": suggestions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving suggestions: {str(e)}")


@router.get("/quality/{conversation_id}/history")
async def get_quality_history(conversation_id: str, agent_id: Optional[str] = None):
    """
    Get historical quality metrics showing trends over time

    Returns consistency and diversity scores across multiple evaluations
    """
    try:
        history = {
            "conversation_id": conversation_id,
            "consistency_history": {},
            "diversity_history": []
        }

        # Get consistency history
        if agent_id:
            if agent_id in persona_service.consistency_history:
                history["consistency_history"][agent_id] = [
                    {
                        "score": s.score,
                        "prompt_to_line": s.prompt_to_line_score,
                        "line_to_line": s.line_to_line_score,
                        "feedback": s.feedback
                    }
                    for s in persona_service.consistency_history[agent_id]
                ]
        else:
            # All agents
            for aid, scores in persona_service.consistency_history.items():
                history["consistency_history"][aid] = [
                    {
                        "score": s.score,
                        "prompt_to_line": s.prompt_to_line_score,
                        "line_to_line": s.line_to_line_score
                    }
                    for s in scores
                ]

        # Get diversity history
        if conversation_id in persona_service.diversity_history:
            history["diversity_history"] = [
                {
                    "response_similarity": d.response_similarity,
                    "topic_diversity": d.topic_diversity,
                    "opinion_diversity": d.opinion_diversity
                }
                for d in persona_service.diversity_history[conversation_id]
            ]

        return history

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quality history: {str(e)}")
