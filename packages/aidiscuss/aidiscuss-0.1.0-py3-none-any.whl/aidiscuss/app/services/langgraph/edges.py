"""
Conditional Edge Routing Logic

Defines routing functions that determine which node to execute next
based on the current conversation state.
"""

from typing import Literal
from aidiscuss.app.services.langgraph.state import ConversationState


# Route destination constants
END = "__end__"


def route_after_admin_check(state: ConversationState) -> Literal["execute_admin_action", "check_stopping"]:
    """
    Route after checking for admin overrides

    Decision:
    - If pending admin action exists → execute it
    - Otherwise → proceed to stopping criteria check

    Args:
        state: Current conversation state

    Returns:
        Next node name
    """
    if state.get("pending_admin_action"):
        return "execute_admin_action"
    return "check_stopping"


def route_after_admin_execution(state: ConversationState) -> Literal["__end__", "check_stopping"]:
    """
    Route after executing admin action

    Decision:
    - If admin paused conversation → END
    - Otherwise → continue to stopping check

    Args:
        state: Current conversation state

    Returns:
        Next node name or END
    """
    if state.get("should_stop"):
        return END
    return "check_stopping"


def route_stopping_check(state: ConversationState) -> Literal["__end__", "system_ai_decision"]:
    """
    Route after checking stopping criteria

    Decision:
    - If should_stop is True → END conversation
    - Otherwise → continue to System AI decision

    Args:
        state: Current conversation state

    Returns:
        Next node name or END
    """
    if state.get("should_stop"):
        return END
    return "system_ai_decision"


def route_system_ai_decision(state: ConversationState) -> Literal["system_ai_mediate", "select_speaker"]:
    """
    Route System AI decision

    Decision:
    - If System AI should mediate (active mode + right turn) → mediate
    - Otherwise → proceed to speaker selection

    Args:
        state: Current conversation state

    Returns:
        Next node name
    """
    config = state.get("system_ai_config")
    turn_number = state.get("turn_number", 0)

    if config and config.should_mediate(turn_number):
        return "system_ai_mediate"

    return "select_speaker"


def route_after_quality_check(state: ConversationState) -> Literal["regenerate_response", "update_participation", "extract_citations"]:
    """
    Route after quality reflection check

    Decision:
    - If quality check failed and should regenerate → regenerate_response
    - If citations should be extracted (RAG enabled) → extract_citations
    - Otherwise → update_participation

    Args:
        state: Current conversation state

    Returns:
        Next node name
    """
    quality_check = state.get("pending_quality_check")

    if quality_check and quality_check.should_regenerate:
        return "regenerate_response"

    # Check if we should extract citations
    if state.get("rag_enabled") and state.get("quality_config", {}).require_citations:
        return "extract_citations"

    return "update_participation"


def route_after_response(state: ConversationState) -> Literal["reflection", "update_participation"]:
    """
    Route after agent generates response

    Decision:
    - If quality check is pending → go to reflection node
    - Otherwise → skip to participation update

    Args:
        state: Current conversation state

    Returns:
        Next node name
    """
    if state.get("pending_quality_check"):
        return "reflection"

    return "update_participation"


def route_speaker_selection(state: ConversationState) -> Literal["agent_response", "check_user_message"]:
    """
    Route after speaker selection

    Decision:
    - If human-in-the-loop enabled → check for user message
    - Otherwise → proceed to agent response

    Args:
        state: Current conversation state

    Returns:
        Next node name
    """
    # For now, always go to agent response
    # In future, this could check for human participant flag
    return "agent_response"


def route_participation_update(state: ConversationState) -> Literal["check_consensus", "check_admin"]:
    """
    Route after updating participation

    Decision:
    - If consensus checking enabled → check consensus
    - Otherwise → loop back to admin check (start of next turn)

    Args:
        state: Current conversation state

    Returns:
        Next node name
    """
    if state.get("stopping_criteria", {}).consensus_enabled:
        return "check_consensus"

    # Loop back to admin check for next turn
    return "check_admin"


def route_consensus_check(state: ConversationState) -> Literal["__end__", "check_admin"]:
    """
    Route after consensus check

    Decision:
    - If consensus reached → END
    - Otherwise → continue (loop back to admin check)

    Args:
        state: Current conversation state

    Returns:
        Next node name or END
    """
    if state.get("should_stop"):
        return END

    return "check_admin"


def create_conditional_edges_map():
    """
    Create a mapping of node names to their routing functions

    This is used by the LangGraph orchestrator to define conditional edges.

    Returns:
        Dictionary mapping node names to routing functions
    """
    return {
        "check_admin": route_after_admin_check,
        "execute_admin_action": route_after_admin_execution,
        "check_stopping": route_stopping_check,
        "system_ai_decision": route_system_ai_decision,
        "agent_response": route_after_response,
        "reflection": route_after_quality_check,
        "select_speaker": route_speaker_selection,
        "update_participation": route_participation_update,
        "check_consensus": route_consensus_check
    }


def get_start_node() -> str:
    """Get the starting node for the conversation graph"""
    return "check_admin"


def get_end_node() -> str:
    """Get the end marker for the conversation graph"""
    return END
