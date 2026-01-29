"""
Decision Nodes

Implements decision-making nodes:
- Stopping criteria checks
- Speaker selection
- Participation updates
"""

from typing import Dict
from langchain_core.messages import SystemMessage
from aidiscuss.app.services.langgraph.state import ConversationState


async def check_stopping_criteria_node(state: ConversationState) -> ConversationState:
    """
    Check if conversation should stop based on configured criteria

    Checks:
    1. Turn limits (with soft warnings at 80%, 95%)
    2. Consensus threshold
    3. Keyword triggers
    4. Time limits
    5. Manual stop flag
    """
    criteria = state["stopping_criteria"]
    turn_number = state["turn_number"]

    # Already stopped
    if state.get("should_stop"):
        return state

    # Check turn limits with warnings
    if turn_number >= criteria.max_turns:
        state["should_stop"] = True
        state["stop_reason"] = "Maximum turns reached"
        return state

    # Soft warnings
    if turn_number == int(criteria.max_turns * 0.8):
        warning = SystemMessage(
            content=f"[System]: Approaching turn limit ({turn_number}/{criteria.max_turns}). Consider wrapping up."
        )
        state["messages"].append(warning)

    if turn_number == int(criteria.max_turns * 0.95):
        warning = SystemMessage(
            content=f"[System]: Final turns remaining ({criteria.max_turns - turn_number} turns left). Please conclude."
        )
        state["messages"].append(warning)

    # Check minimum turns before other stopping criteria
    if turn_number < criteria.min_turns:
        return state

    # Check consensus if enabled
    if criteria.consensus_enabled:
        consensus_score = state.get("consensus_score", 0.0)
        if consensus_score >= criteria.consensus_threshold:
            state["should_stop"] = True
            state["stop_reason"] = f"Consensus reached (score: {consensus_score:.2f})"
            return state

    # Check keyword triggers
    if criteria.keyword_triggers and state["messages"]:
        last_message = state["messages"][-1]
        content_upper = last_message.content.upper()

        for keyword in criteria.keyword_triggers:
            if keyword.upper() in content_upper:
                state["should_stop"] = True
                state["stop_reason"] = f"Keyword trigger detected: {keyword}"
                return state

    # Check time limit
    if criteria.time_limit_seconds:
        from datetime import datetime
        elapsed = (datetime.now() - state["started_at"]).total_seconds()
        if elapsed >= criteria.time_limit_seconds:
            state["should_stop"] = True
            state["stop_reason"] = "Time limit reached"
            return state

    return state


async def select_next_speaker_node(
    state: ConversationState,
    balancer: 'ParticipationBalancer' = None
) -> ConversationState:
    """
    Select next speaker based on turn-taking strategy

    Strategies:
    - round-robin: Simple rotation
    - addressed-response: Based on last message addressing
    - bidding: Agents bid for turns (future)
    - system-guided: System AI selects based on context
    """
    strategy = state["turn_strategy"]
    agent_ids = state["agent_ids"]

    if not agent_ids:
        raise ValueError("No agents available")

    # Get current speaker
    current_speaker = state.get("current_speaker")

    # Round-robin strategy (default)
    if strategy == "round-robin":
        if not current_speaker:
            # First turn - start with first agent
            next_speaker = agent_ids[0]
        else:
            # Find current index and move to next
            try:
                current_index = agent_ids.index(current_speaker)
                next_index = (current_index + 1) % len(agent_ids)
                next_speaker = agent_ids[next_index]
            except ValueError:
                # Current speaker not in list, start from beginning
                next_speaker = agent_ids[0]

        # Apply participation balancing if provided
        if balancer:
            # Check if next speaker has hit consecutive limit
            participation = state["agent_participation"][next_speaker]
            max_consecutive = state.get("max_consecutive_turns_per_agent", 3)

            if participation.consecutive_turns >= max_consecutive:
                # Force select a different speaker
                next_speaker = balancer.select_balanced_speaker(state)

    # Addressed-response strategy
    elif strategy == "addressed-response":
        # Check if last message addresses a specific agent
        if state["messages"]:
            last_message = state["messages"][-1]
            content_lower = last_message.content.lower()

            # Simple addressing detection
            addressed_agent = None
            for agent_id in agent_ids:
                if f"@{agent_id}" in content_lower or agent_id.lower() in content_lower:
                    addressed_agent = agent_id
                    break

            next_speaker = addressed_agent if addressed_agent else agent_ids[0]
        else:
            next_speaker = agent_ids[0]

    # System-guided strategy
    elif strategy == "system-guided":
        # Use participation balancer for intelligent selection
        if balancer:
            next_speaker = balancer.select_balanced_speaker(state)
        else:
            # Fallback to round-robin
            next_speaker = agent_ids[0] if not current_speaker else agent_ids[(agent_ids.index(current_speaker) + 1) % len(agent_ids)]

    # Bidding strategy (future implementation)
    else:
        # Fallback to round-robin
        next_speaker = agent_ids[0] if not current_speaker else agent_ids[(agent_ids.index(current_speaker) + 1) % len(agent_ids)]

    # Set next speaker
    state["next_speaker"] = next_speaker

    return state


async def update_participation_node(state: ConversationState) -> ConversationState:
    """
    Update participation metrics after agent response

    This is mostly handled in agent_response_node, but this node
    can be used for additional tracking or analytics
    """
    current_speaker = state.get("current_speaker")

    if not current_speaker:
        return state

    # Calculate participation balance
    participation = state["agent_participation"]
    total_turns = state["turn_number"]
    agent_count = len(state["agent_ids"])

    if agent_count == 0:
        return state

    expected_avg = total_turns / agent_count

    # Check for imbalance
    imbalanced_agents = []
    overparticipating_agents = []

    for agent_id, part in participation.items():
        if part.total_turns < expected_avg * 0.5:
            imbalanced_agents.append(agent_id)
        elif part.total_turns > expected_avg * 1.5:
            overparticipating_agents.append(agent_id)

    # Store imbalance info in metadata for System AI to use
    state["metadata"]["participation_imbalance"] = {
        "underparticipating": imbalanced_agents,
        "overparticipating": overparticipating_agents,
        "expected_avg": expected_avg
    }

    # Add participation warning if severe imbalance
    if imbalanced_agents and state.get("system_ai_active"):
        if len(imbalanced_agents) >= agent_count // 2:
            warning = SystemMessage(
                content=f"[System]: Notice - Some agents have been quiet. Encouraging balanced participation."
            )
            state["messages"].append(warning)

    return state


async def check_user_message_node(state: ConversationState) -> ConversationState:
    """
    Check if user (human) wants to contribute to conversation

    This node checks for pending human input with a timeout.
    If no response within timeout and not typing, agents continue.
    """
    import asyncio
    from datetime import datetime

    # Check if we should wait for human input
    # Only wait every N turns to avoid constant pausing
    wait_frequency = state.get("metadata", {}).get("human_input_check_frequency", 5)
    turn_number = state["turn_number"]

    if turn_number % wait_frequency != 0:
        return state

    # Configuration for waiting
    wait_timeout = state.get("metadata", {}).get("human_response_timeout", 30.0)

    # Check for pending human message
    pending_human_message = state.get("metadata", {}).get("pending_human_message")
    is_user_typing = state.get("metadata", {}).get("is_user_typing", False)

    if pending_human_message:
        # Human has responded, add their message
        from langchain_core.messages import HumanMessage
        state["messages"].append(HumanMessage(content=pending_human_message, name="user"))
        # Clear the pending message
        state["metadata"]["pending_human_message"] = None
        return state

    # If not typing and no pending message, continue without waiting
    if not is_user_typing:
        # Add a system message indicating agents are continuing
        warning = SystemMessage(
            content=f"[System]: No human response. Agents continuing discussion."
        )
        state["messages"].append(warning)

    return state
