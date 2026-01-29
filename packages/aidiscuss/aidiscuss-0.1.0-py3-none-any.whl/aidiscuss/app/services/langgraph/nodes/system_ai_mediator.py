"""
System AI Mediator Node

System AI acts as intelligent facilitator:
- Balances participation (invites quiet agents)
- Guides toward conversation goal
- Injects clarifying questions
- Detects and mediates conflicts
"""

from typing import List
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession

from aidiscuss.app.services.langgraph.state import ConversationState
from aidiscuss.app.services.llm_provider import create_llm


async def system_ai_mediator_node(
    state: ConversationState,
    db: AsyncSession
) -> ConversationState:
    """
    System AI mediation - guide conversation for better outcomes

    Actions based on mode:
    - Active: Inject messages, guide discussion, balance participation
    - Passive: Silent coordination only (handled in select_speaker_node)

    Args:
        state: Current conversation state
        db: Database session

    Returns:
        Updated state with potential System AI intervention messages
    """
    config = state["system_ai_config"]

    # Skip if passive mode
    if config.mode == "passive":
        return state

    # Skip if not time to mediate
    if not config.should_mediate(state["turn_number"]):
        return state

    # Collect mediation actions
    mediation_actions: List[str] = []

    # 1. Balance Participation
    if config.balance_participation:
        participation_data = state["metadata"].get("participation_imbalance", {})
        underparticipating = participation_data.get("underparticipating", [])

        if underparticipating:
            # Get agent names for better messaging
            quiet_agents = ", ".join(underparticipating)
            mediation_actions.append(
                f"I notice {quiet_agents} haven't contributed much yet. "
                f"I'd love to hear your perspectives on this discussion."
            )

    # 2. Guide Toward Goal
    if config.guide_toward_goal:
        # Check if conversation is drifting from goal
        alignment_score = await check_goal_alignment(state, db)

        if alignment_score < 0.6:
            mediation_actions.append(
                f"Let's refocus on our main goal: {state['conversation_goal']}. "
                f"How does our current discussion connect to this objective?"
            )

    # 3. Inject Clarifying Questions
    if config.inject_questions:
        # Detect if clarification is needed
        needs_clarification = await detect_clarification_needed(state, db)

        if needs_clarification:
            mediation_actions.append(
                "I sense we might need clarification on the last point. "
                "Could someone elaborate or provide more context?"
            )

    # 4. Detect and Mediate Conflicts
    conflict_detected = await detect_conflict(state, db)

    if conflict_detected:
        mediation_actions.append(
            "I notice different viewpoints emerging. "
            "That's valuable! Let's explore both perspectives systematically."
        )

    # 5. Check Topic Coverage
    if state.get("topics_to_cover"):
        remaining_topics = [
            topic for topic in state["topics_to_cover"]
            if topic not in state.get("current_topics", [])
        ]

        if remaining_topics and state["turn_number"] > state["stopping_criteria"].max_turns * 0.7:
            topics_str = ", ".join(remaining_topics[:2])
            mediation_actions.append(
                f"We're making good progress. We still have these topics to cover: {topics_str}. "
                f"Should we address those before concluding?"
            )

    # Inject System AI message if actions needed
    if mediation_actions:
        system_message = SystemMessage(
            content=f"[System AI Mediator]: {' '.join(mediation_actions)}"
        )
        state["messages"].append(system_message)
        state["metadata"]["system_ai_interventions"] = state["metadata"].get("system_ai_interventions", 0) + 1

    return state


async def check_goal_alignment(
    state: ConversationState,
    db: AsyncSession
) -> float:
    """
    Check if recent conversation aligns with stated goal

    Returns alignment score (0.0 - 1.0)
    """
    if not state["messages"]:
        return 1.0  # No messages yet, assume aligned

    # Get recent messages
    recent_messages = state["messages"][-3:]
    conversation_text = "\n".join([
        f"{msg.name or 'User'}: {msg.content}"
        for msg in recent_messages
    ])

    # Use LLM to assess alignment
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Assess how well the following conversation segment aligns with the stated goal.

Goal: {goal}

Recent Conversation:
{conversation}

Respond with a JSON object:
{{"alignment_score": 0.0-1.0, "reasoning": "brief explanation"}}

Where:
- 1.0 = Perfectly aligned with goal
- 0.7-0.9 = Mostly aligned
- 0.4-0.6 = Partially aligned
- 0.0-0.4 = Drifted from goal"""),
        ("human", "Assess alignment.")
    ])

    try:
        # Use a fast, cheap model for this assessment
        llm = create_llm(
            provider_name="openai",  # Or use configured default
            model="gpt-4o-mini",
            temperature=0.0
        )

        response = await llm.ainvoke(
            prompt.format_messages(
                goal=state["conversation_goal"],
                conversation=conversation_text
            )
        )

        # Parse JSON response
        import json
        result = json.loads(response.content)
        return result.get("alignment_score", 0.5)

    except Exception as e:
        # Fallback to neutral score on error
        return 0.5


async def detect_clarification_needed(
    state: ConversationState,
    db: AsyncSession
) -> bool:
    """
    Detect if clarification is needed in recent conversation

    Returns True if clarification would be helpful
    """
    if len(state["messages"]) < 2:
        return False

    # Get last few messages
    recent_messages = state["messages"][-2:]

    # Simple heuristic detection
    for msg in recent_messages:
        content_lower = msg.content.lower()

        # Look for ambiguity markers
        ambiguity_markers = [
            "not sure", "unclear", "confused", "what do you mean",
            "can you clarify", "could you explain", "??"
        ]

        for marker in ambiguity_markers:
            if marker in content_lower:
                return True

    return False


async def detect_conflict(
    state: ConversationState,
    db: AsyncSession
) -> bool:
    """
    Detect if agents are disagreeing or in conflict

    Returns True if conflict/disagreement detected
    """
    if len(state["messages"]) < 3:
        return False

    # Get recent messages from different agents
    recent_messages = state["messages"][-3:]

    # Simple disagreement detection
    disagreement_markers = [
        "disagree", "however", "but", "on the other hand",
        "i don't think", "that's not", "actually"
    ]

    disagreement_count = 0
    for msg in recent_messages:
        content_lower = msg.content.lower()
        if any(marker in content_lower for marker in disagreement_markers):
            disagreement_count += 1

    # If 2+ recent messages show disagreement markers, likely a conflict
    return disagreement_count >= 2


async def toggle_system_ai_mode_node(state: ConversationState, new_mode: str) -> ConversationState:
    """
    Toggle System AI mode mid-conversation (via admin override)

    Args:
        state: Current state
        new_mode: "active" or "passive"

    Returns:
        Updated state with new mode
    """
    old_mode = state["system_ai_config"].mode
    state["system_ai_config"].mode = new_mode
    state["system_ai_active"] = (new_mode == "active")

    # Add notification message
    notification = SystemMessage(
        content=f"[System]: System AI mode changed from {old_mode} to {new_mode}"
    )
    state["messages"].append(notification)

    return state
