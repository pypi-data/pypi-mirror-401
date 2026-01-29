"""
Admin Override Node

Handles admin override actions with highest authority:
- Check for pending admin actions
- Execute admin commands
- Log all actions for audit trail
"""

from langchain_core.messages import SystemMessage
from sqlalchemy.ext.asyncio import AsyncSession

from aidiscuss.app.services.langgraph.state import ConversationState, AgentParticipation


async def check_admin_override_node(state: ConversationState) -> ConversationState:
    """
    Check if there's a pending admin override action

    This node runs early in the graph to catch admin interventions
    before normal conversation flow continues.

    Returns:
        State (unmodified - actual execution happens in execute node)
    """
    # This node just checks - execution happens in separate node
    # This allows for conditional routing based on pending_admin_action
    return state


async def execute_admin_action_node(
    state: ConversationState,
    db: AsyncSession
) -> ConversationState:
    """
    Execute pending admin override action

    Admin actions (highest authority):
    - redirect: Change conversation goal mid-stream
    - kick_agent: Remove agent from conversation
    - add_agent: Add new agent to ongoing conversation
    - modify_goal: Update conversation goal
    - inject_context: Add information/context to conversation
    - pause: Temporarily stop conversation
    - resume: Resume paused conversation
    - toggle_system_ai_mode: Switch System AI between active/passive

    Args:
        state: Current conversation state
        db: Database session for logging actions

    Returns:
        Updated state after admin action execution
    """
    action = state.get("pending_admin_action")

    if not action:
        return state

    action_type = action.action_type
    executed_message = None

    # Execute based on action type
    if action_type == "redirect" or action_type == "modify_goal":
        # Change conversation goal
        if action.new_goal:
            old_goal = state["conversation_goal"]
            state["conversation_goal"] = action.new_goal
            executed_message = (
                f"[Admin Override]: Conversation goal changed.\n"
                f"Previous goal: {old_goal}\n"
                f"New goal: {action.new_goal}"
            )

    elif action_type == "kick_agent":
        # Remove agent from conversation
        if action.target_agent_id and action.target_agent_id in state["agent_ids"]:
            # Prevent kicking the last agent
            if len(state["agent_ids"]) <= 1:
                executed_message = (
                    f"[Admin Override]: Cannot kick last remaining agent. "
                    f"Please add another agent first."
                )
            else:
                state["agent_ids"].remove(action.target_agent_id)
                # Remove from participation tracking
                if action.target_agent_id in state["agent_participation"]:
                    del state["agent_participation"][action.target_agent_id]

                executed_message = (
                    f"[Admin Override]: Agent {action.target_agent_id} has been removed from the conversation."
                )

                # If kicked agent was next speaker, select new one
                if state.get("next_speaker") == action.target_agent_id:
                    state["next_speaker"] = None  # Will be reselected

    elif action_type == "add_agent":
        # Add new agent to conversation
        if action.target_agent_id and action.target_agent_id not in state["agent_ids"]:
            state["agent_ids"].append(action.target_agent_id)
            # Initialize participation tracking
            state["agent_participation"][action.target_agent_id] = AgentParticipation(
                agent_id=action.target_agent_id
            )

            executed_message = (
                f"[Admin Override]: Agent {action.target_agent_id} has been added to the conversation."
            )

    elif action_type == "inject_context":
        # Inject additional context or information
        if action.injected_context:
            executed_message = (
                f"[Admin Context Injection]: {action.injected_context}"
            )

    elif action_type == "pause":
        # Pause conversation
        state["should_stop"] = True
        state["stop_reason"] = "Admin paused conversation"
        executed_message = "[Admin Override]: Conversation paused by admin."

    elif action_type == "resume":
        # Resume paused conversation
        if state.get("should_stop") and state.get("stop_reason") == "Admin paused conversation":
            state["should_stop"] = False
            state["stop_reason"] = None
            executed_message = "[Admin Override]: Conversation resumed by admin."

    elif action_type == "toggle_system_ai_mode":
        # Toggle System AI mode
        if action.new_system_ai_mode:
            old_mode = state["system_ai_config"].mode
            state["system_ai_config"].mode = action.new_system_ai_mode
            state["system_ai_active"] = (action.new_system_ai_mode == "active")

            executed_message = (
                f"[Admin Override]: System AI mode changed from {old_mode} to {action.new_system_ai_mode}"
            )

    # Add executed message to conversation
    if executed_message:
        admin_message = SystemMessage(content=executed_message)
        state["messages"].append(admin_message)

    # Log action to history
    state["admin_action_history"].append(action)

    # Store action count in metadata
    state["metadata"]["admin_actions_count"] = len(state["admin_action_history"])

    # Clear pending action
    state["pending_admin_action"] = None

    # TODO: Save admin action to database for audit trail
    # This would be done via the AdminAction model

    return state


async def inject_admin_action(
    state: ConversationState,
    action: 'AdminOverride'
) -> ConversationState:
    """
    Inject admin action into running conversation

    This function can be called externally (e.g., from WebSocket endpoint)
    to inject admin actions into the conversation state.

    Args:
        state: Current conversation state
        action: Admin override action to inject

    Returns:
        Updated state with pending admin action
    """
    state["pending_admin_action"] = action
    state["admin_mode"] = True

    return state


def validate_admin_action(
    state: ConversationState,
    action: 'AdminOverride'
) -> tuple[bool, str]:
    """
    Validate admin action before execution

    Returns:
        (is_valid, error_message)
    """
    action_type = action.action_type

    # Check if admin override is allowed
    if not state.get("allow_admin_override", True):
        return False, "Admin override is disabled for this conversation"

    # Validate kick_agent
    if action_type == "kick_agent":
        if not action.target_agent_id:
            return False, "kick_agent requires target_agent_id"
        if action.target_agent_id not in state["agent_ids"]:
            return False, f"Agent {action.target_agent_id} not in conversation"
        if len(state["agent_ids"]) <= 1:
            return False, "Cannot kick the last remaining agent"

    # Validate add_agent
    if action_type == "add_agent":
        if not action.target_agent_id:
            return False, "add_agent requires target_agent_id"
        if action.target_agent_id in state["agent_ids"]:
            return False, f"Agent {action.target_agent_id} already in conversation"

    # Validate redirect/modify_goal
    if action_type in ["redirect", "modify_goal"]:
        if not action.new_goal:
            return False, f"{action_type} requires new_goal"

    # Validate inject_context
    if action_type == "inject_context":
        if not action.injected_context:
            return False, "inject_context requires injected_context"

    # Validate toggle_system_ai_mode
    if action_type == "toggle_system_ai_mode":
        if not action.new_system_ai_mode:
            return False, "toggle_system_ai_mode requires new_system_ai_mode"
        if action.new_system_ai_mode not in ["active", "passive"]:
            return False, "new_system_ai_mode must be 'active' or 'passive'"

    return True, ""
