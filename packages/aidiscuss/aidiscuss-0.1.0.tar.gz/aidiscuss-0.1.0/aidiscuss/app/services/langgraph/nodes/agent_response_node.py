"""
Agent Response Node

Generates responses from the selected agent with:
- Memory context injection
- RAG context grounding
- Persona reminders
- Participation tracking
"""

from typing import Dict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession

from aidiscuss.app.services.langgraph.state import ConversationState, PendingQualityCheck
from aidiscuss.app.services.llm_provider import create_llm


async def build_agent_prompt(
    state: ConversationState,
    agent: Dict,
    db: AsyncSession
) -> list:
    """
    Build comprehensive prompt for agent including:
    - System prompt with persona
    - Memory context
    - RAG context
    - Conversation history
    - Goal reminder
    """
    messages = []

    # 1. Base system prompt
    system_content = agent.get("system_prompt", "You are a helpful AI assistant.")

    # 2. Add multi-agent conversation context
    agent_names = [state["agents_dict"].get(aid, {}).get("name", aid) for aid in state["agent_ids"]]
    system_content += f"\n\n# Multi-Agent Conversation Context"
    system_content += f"\nYou are {agent.get('name', 'Agent')}, participating in a multi-agent conversation."
    system_content += f"\n\nOther AI agents in this conversation: {', '.join([n for n in agent_names if n != agent.get('name', 'Agent')])}"
    system_content += f"\n\n**CRITICAL**: The human user is NOT an agent. When you see messages from 'user' or 'human', that is the HUMAN USER observing the conversation."
    system_content += f"\nThe agents discuss topics among themselves. If the human contributes, acknowledge them briefly, then continue discussing with the OTHER AGENTS."
    system_content += f"\n\nStay in character. Your responses must reflect your unique personality, perspective, and behavior."
    system_content += f"\nAddress other AGENTS by their names. Build upon, challenge, or respond to their points with your perspective."
    system_content += f"\n\n**DO NOT** confuse the human with any agent. Only the agents listed above are AI agents."

    # 3. Add persona reminder if enabled
    config = state["quality_config"]
    turn_number = state["turn_number"]

    if state.get("enable_memory") and turn_number > 0:
        persona_frequency = state["quality_config"].reflection_frequency
        if turn_number % persona_frequency == 0:
            system_content += f"\n\nReminder: Stay true to your persona and role. You are: {agent.get('name', 'Agent')}"

    # 4. Add conversation goal
    system_content += f"\n\nConversation Goal: {state['conversation_goal']}"

    # 5. Add RAG context if available
    if state.get("rag_context") and state.get("rag_enabled"):
        rag_context = state["rag_context"]
        system_content += f"\n\nKnowledge Base Context:\n{rag_context}"

        if config.require_citations:
            system_content += "\n\nIMPORTANT: When using information from the knowledge base, cite your sources using [Source: ...] format."

    # 6. Add memory context if available
    if state.get("memory_context") and state.get("enable_memory"):
        memory_summary = state["memory_context"].get("summary", "")
        if memory_summary:
            system_content += f"\n\nConversation Summary So Far:\n{memory_summary}"

        # Add extracted facts
        facts = state["memory_context"].get("facts", [])
        if facts:
            facts_text = "\n".join([f"- {fact['content']}" for fact in facts[:5]])
            system_content += f"\n\nKey Facts:\n{facts_text}"

    # Create system message
    messages.append(SystemMessage(content=system_content))

    # 7. Add conversation history (context window)
    context_window = state.get("context_window_messages", 20)
    recent_messages = state["messages"][-context_window:] if state["messages"] else []
    messages.extend(recent_messages)

    return messages


async def agent_response_node(
    state: ConversationState,
    agents_dict: Dict,
    db: AsyncSession
) -> ConversationState:
    """
    Generate response from selected agent

    Args:
        state: Current conversation state
        agents_dict: Dictionary of agent configurations by ID
        db: Database session for loading agent data

    Returns:
        Updated state with new message and participation tracking
    """
    agent_id = state.get("next_speaker")

    if not agent_id:
        raise ValueError("No next speaker selected")

    # Get agent configuration
    agent = agents_dict.get(agent_id)
    if not agent:
        raise ValueError(f"Agent {agent_id} not found")

    # Build prompt with all context
    prompt_messages = await build_agent_prompt(state, agent, db)

    # Create LLM for this agent
    llm = create_llm(
        provider_name=agent.get("provider_name"),
        model=agent.get("model"),
        temperature=agent.get("temperature", 0.7),
        max_tokens=agent.get("max_tokens", 1000),
        api_key=agent.get("api_key")
    )

    # Generate response
    try:
        response = await llm.ainvoke(prompt_messages)
        response_content = response.content
    except Exception as e:
        # Fallback error message
        response_content = f"[Error generating response: {str(e)}]"

    # Create AI message
    ai_message = AIMessage(
        content=response_content,
        name=agent_id,
        additional_kwargs={
            "agent_name": agent.get("name", agent_id),
            "turn_number": state["turn_number"],
            "model": agent.get("model")
        }
    )

    # Update state
    state["messages"].append(ai_message)
    state["current_speaker"] = agent_id

    # Update participation tracking
    participation = state["agent_participation"][agent_id]
    participation.consecutive_turns += 1
    participation.total_turns += 1
    participation.last_turn_number = state["turn_number"]

    # Reset consecutive counts for other agents
    for other_agent_id in state["agent_ids"]:
        if other_agent_id != agent_id:
            state["agent_participation"][other_agent_id].consecutive_turns = 0

    # Set up pending quality check if enabled
    if state["quality_config"].enable_reflection:
        should_check = state["quality_config"].should_check_quality(state["turn_number"])
        if should_check:
            state["pending_quality_check"] = PendingQualityCheck(
                agent_id=agent_id,
                response=response_content,
                turn_number=state["turn_number"],
                should_regenerate=False,
                regeneration_attempt=state.get("regeneration_count", 0)
            )

    # Increment turn number
    state["turn_number"] += 1

    return state


async def regenerate_response_node(
    state: ConversationState,
    agents_dict: Dict,
    db: AsyncSession
) -> ConversationState:
    """
    Regenerate response after quality check failure

    Similar to agent_response_node but:
    - Removes the last (failed) message
    - Increments regeneration count
    - Adds feedback to prompt
    """
    # Get pending quality check
    quality_check = state.get("pending_quality_check")
    if not quality_check:
        return state

    agent_id = quality_check.agent_id
    agent = agents_dict.get(agent_id)

    if not agent:
        return state

    # Remove failed message
    if state["messages"] and state["messages"][-1].name == agent_id:
        state["messages"].pop()

    # Increment regeneration count
    state["regeneration_count"] += 1

    # Build prompt with feedback
    prompt_messages = await build_agent_prompt(state, agent, db)

    # Add feedback as additional system message
    feedback_text = "\n".join(quality_check.feedback)
    feedback_message = SystemMessage(
        content=f"Previous response had quality issues. Please address:\n{feedback_text}"
    )
    prompt_messages.append(feedback_message)

    # Create LLM
    llm = create_llm(
        provider_name=agent.get("provider_name"),
        model=agent.get("model"),
        temperature=agent.get("temperature", 0.7) + 0.1,  # Slightly increase creativity
        max_tokens=agent.get("max_tokens", 1000),
        api_key=agent.get("api_key")
    )

    # Generate new response
    try:
        response = await llm.ainvoke(prompt_messages)
        response_content = response.content
    except Exception as e:
        response_content = f"[Error generating response: {str(e)}]"

    # Create new message
    ai_message = AIMessage(
        content=response_content,
        name=agent_id,
        additional_kwargs={
            "agent_name": agent.get("name", agent_id),
            "turn_number": state["turn_number"],
            "regeneration_attempt": state["regeneration_count"],
            "model": agent.get("model")
        }
    )

    # Update state
    state["messages"].append(ai_message)

    # Update pending quality check for re-evaluation
    quality_check.response = response_content
    quality_check.regeneration_attempt = state["regeneration_count"]
    state["pending_quality_check"] = quality_check

    return state
