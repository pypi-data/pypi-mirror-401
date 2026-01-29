"""
Reflection Node

Implements quality control through reflection pattern:
- RAG grounding validation
- LLM-as-Judge scoring
- Novelty detection
- Aggregate quality scoring
"""

from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from aidiscuss.app.services.langgraph.state import ConversationState


async def reflection_node(
    state: ConversationState,
    quality_service: 'QualityService',
    db: AsyncSession
) -> ConversationState:
    """
    Perform quality checks on pending agent response

    Quality checks:
    1. RAG Grounding - Validate response uses provided documents
    2. LLM-as-Judge - Score response quality and relevance
    3. Novelty Detection - Prevent repetitive responses
    4. Aggregate Scoring - Combine scores and make decision

    Args:
        state: Current conversation state
        quality_service: Quality assessment service
        db: Database session

    Returns:
        Updated state with quality check results
    """
    # Check if there's a pending quality check
    quality_check = state.get("pending_quality_check")

    if not quality_check:
        # No quality check needed
        return state

    config = state["quality_config"]
    response_content = quality_check.response
    agent_id = quality_check.agent_id

    # Initialize results
    scores = {}
    feedback = []
    passed = True

    # 1. RAG Grounding Check (if enabled and RAG context available)
    if config.enable_rag_grounding and state.get("rag_context"):
        try:
            grounding_score = await quality_service.rag_grounding_check(
                response=response_content,
                rag_context=state["rag_context"],
                require_citations=config.require_citations
            )
            scores["rag_grounding"] = grounding_score

            if grounding_score < 0.5:
                passed = False
                feedback.append("Response not well-grounded in provided knowledge base")

            if config.require_citations and "[Source:" not in response_content:
                passed = False
                feedback.append("Response missing required citations")

        except Exception as e:
            # Log error but don't fail
            feedback.append(f"RAG grounding check error: {str(e)}")

    # 2. LLM-as-Judge Validation (if enabled)
    if config.enable_llm_judge:
        try:
            judge_score = await quality_service.llm_judge_evaluate(
                agent_id=agent_id,
                response=response_content,
                conversation_context=state["messages"][-5:] if state["messages"] else [],
                goal=state["conversation_goal"]
            )
            scores["llm_judge"] = judge_score

            if not config.passes_threshold(judge_score):
                passed = False
                feedback.append(f"Quality score {judge_score:.2f} below threshold {config.min_quality_threshold}")

        except Exception as e:
            feedback.append(f"LLM judge error: {str(e)}")

    # 3. Novelty Detection (if enabled)
    if config.enable_novelty_detection and state.get("recent_response_embeddings"):
        try:
            novelty_score = await quality_service.check_novelty(
                response=response_content,
                recent_embeddings=state["recent_response_embeddings"]
            )
            scores["novelty"] = novelty_score

            if novelty_score < config.novelty_threshold:
                passed = False
                feedback.append(f"Response too similar to recent messages (novelty: {novelty_score:.2f})")

            # Update embeddings history
            new_embedding = await quality_service.get_embedding(response_content)
            if "recent_response_embeddings" not in state:
                state["recent_response_embeddings"] = []
            state["recent_response_embeddings"].append(new_embedding)

            # Keep only last 20 embeddings
            if len(state["recent_response_embeddings"]) > 20:
                state["recent_response_embeddings"] = state["recent_response_embeddings"][-20:]

        except Exception as e:
            feedback.append(f"Novelty check error: {str(e)}")

    # 4. Calculate aggregate score
    if scores:
        aggregate_score = sum(scores.values()) / len(scores)
        scores["aggregate"] = aggregate_score
    else:
        aggregate_score = 0.5  # Neutral score if no checks performed

    # Update quality check with results
    quality_check.scores = scores
    quality_check.feedback = feedback

    # Decide on regeneration
    max_attempts = config.max_regeneration_attempts
    current_attempt = quality_check.regeneration_attempt

    if not passed and current_attempt < max_attempts:
        # Mark for regeneration
        quality_check.should_regenerate = True
        state["pending_quality_check"] = quality_check
    else:
        # Accept response (either passed or max attempts reached)
        if not passed and current_attempt >= max_attempts:
            # Log that we're accepting a low-quality response
            state["metadata"]["quality_warnings"] = state["metadata"].get("quality_warnings", [])
            state["metadata"]["quality_warnings"].append({
                "turn": state["turn_number"],
                "agent": agent_id,
                "feedback": feedback,
                "scores": scores
            })

        # Update agent participation with quality score
        if aggregate_score and agent_id in state["agent_participation"]:
            state["agent_participation"][agent_id].response_quality_scores.append(aggregate_score)
            if "novelty" in scores:
                state["agent_participation"][agent_id].novelty_scores.append(scores["novelty"])

        # Clear pending quality check
        state["pending_quality_check"] = None
        state["regeneration_count"] = 0

    return state


async def extract_citations_node(state: ConversationState) -> ConversationState:
    """
    Extract citations from agent response (if RAG enabled)

    This is a helper node that can run after quality check to extract
    and validate citations for analytics purposes
    """
    if not state.get("rag_enabled"):
        return state

    # Get last message
    if not state["messages"]:
        return state

    last_message = state["messages"][-1]
    content = last_message.content

    # Simple citation extraction (look for [Source: ...] patterns)
    import re
    citation_pattern = r'\[Source:\s*([^\]]+)\]'
    citations = re.findall(citation_pattern, content)

    if citations:
        # Store citations in metadata
        if "citations" not in state["metadata"]:
            state["metadata"]["citations"] = {}

        state["metadata"]["citations"][last_message.name] = citations

    return state
