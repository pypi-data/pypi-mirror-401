"""
LangGraph Orchestrator

Main orchestrator for multi-agent conversations using LangGraph's StateGraph.

Integrates all nodes and routing logic to create a sophisticated conversation flow
with quality controls, admin overrides, and system AI mediation.
"""

from typing import AsyncGenerator, Dict, List, Optional
from langgraph.graph import StateGraph, END
from sqlalchemy.ext.asyncio import AsyncSession

from aidiscuss.app.services.langgraph.state import ConversationState, create_initial_state
from aidiscuss.app.services.langgraph.nodes import (
    agent_response_node,
    check_stopping_criteria_node,
    select_next_speaker_node,
    update_participation_node,
    reflection_node,
    system_ai_mediator_node,
    check_admin_override_node,
    execute_admin_action_node
)
from aidiscuss.app.services.langgraph.nodes.agent_response_node import regenerate_response_node
from aidiscuss.app.services.langgraph.nodes.reflection_node import extract_citations_node
from aidiscuss.app.services.langgraph.edges import (
    route_after_admin_check,
    route_after_admin_execution,
    route_stopping_check,
    route_system_ai_decision,
    route_after_quality_check,
    route_after_response,
    route_speaker_selection,
    route_participation_update,
    route_consensus_check
)
from aidiscuss.app.services.langgraph.safeguards import ParticipationBalancer, NoveltyDetector
from aidiscuss.app.services.quality_service import QualityService
from aidiscuss.app.services.consensus_service import ConsensusService
from aidiscuss.app.models.chat_config import ChatConfigSchema


class LangGraphOrchestrator:
    """
    Main orchestrator for multi-agent conversations

    Builds and executes a LangGraph StateGraph with:
    - Admin override handling
    - Stopping criteria checks
    - System AI mediation
    - Speaker selection with balancing
    - Agent response generation
    - Quality reflection loops
    - Consensus detection
    - Participation tracking
    """

    def __init__(
        self,
        conversation_id: str,
        config: ChatConfigSchema,
        agent_ids: List[str],
        agents_dict: Dict,
        db: AsyncSession
    ):
        """
        Initialize orchestrator

        Args:
            conversation_id: Unique conversation identifier
            config: Chat configuration
            agent_ids: List of participating agent IDs
            agents_dict: Dictionary of agent configurations
            db: Database session
        """
        self.conversation_id = conversation_id
        self.config = config
        self.agent_ids = agent_ids
        self.agents_dict = agents_dict
        self.db = db

        # Initialize services
        self.quality_service = QualityService()
        self.consensus_service = ConsensusService()
        self.participation_balancer = ParticipationBalancer(
            max_consecutive=config.max_consecutive_turns_per_agent
        )
        self.novelty_detector = NoveltyDetector(threshold=config.novelty_threshold)

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph StateGraph with all nodes and edges

        Returns:
            Compiled StateGraph
        """
        # Create state graph
        workflow = StateGraph(ConversationState)

        # Define all nodes
        workflow.add_node("check_admin", self._wrap_check_admin)
        workflow.add_node("execute_admin_action", self._wrap_execute_admin)
        workflow.add_node("check_stopping", self._wrap_check_stopping)
        workflow.add_node("system_ai_decision", lambda state: state)  # Pass-through for routing
        workflow.add_node("system_ai_mediate", self._wrap_system_ai_mediate)
        workflow.add_node("select_speaker", self._wrap_select_speaker)
        workflow.add_node("agent_response", self._wrap_agent_response)
        workflow.add_node("regenerate_response", self._wrap_regenerate_response)
        workflow.add_node("reflection", self._wrap_reflection)
        workflow.add_node("extract_citations", self._wrap_extract_citations)
        workflow.add_node("update_participation", self._wrap_update_participation)
        workflow.add_node("check_consensus", self._wrap_check_consensus)

        # Set entry point
        workflow.set_entry_point("check_admin")

        # Add conditional edges
        workflow.add_conditional_edges(
            "check_admin",
            route_after_admin_check,
            {
                "execute_admin_action": "execute_admin_action",
                "check_stopping": "check_stopping"
            }
        )

        workflow.add_conditional_edges(
            "execute_admin_action",
            route_after_admin_execution,
            {
                END: END,
                "check_stopping": "check_stopping"
            }
        )

        workflow.add_conditional_edges(
            "check_stopping",
            route_stopping_check,
            {
                END: END,
                "system_ai_decision": "system_ai_decision"
            }
        )

        workflow.add_conditional_edges(
            "system_ai_decision",
            route_system_ai_decision,
            {
                "system_ai_mediate": "system_ai_mediate",
                "select_speaker": "select_speaker"
            }
        )

        workflow.add_edge("system_ai_mediate", "select_speaker")

        workflow.add_conditional_edges(
            "select_speaker",
            route_speaker_selection,
            {
                "agent_response": "agent_response"
            }
        )

        workflow.add_conditional_edges(
            "agent_response",
            route_after_response,
            {
                "reflection": "reflection",
                "update_participation": "update_participation"
            }
        )

        workflow.add_conditional_edges(
            "reflection",
            route_after_quality_check,
            {
                "regenerate_response": "regenerate_response",
                "extract_citations": "extract_citations",
                "update_participation": "update_participation"
            }
        )

        workflow.add_edge("regenerate_response", "reflection")  # Loop back for re-check
        workflow.add_edge("extract_citations", "update_participation")

        workflow.add_conditional_edges(
            "update_participation",
            route_participation_update,
            {
                "check_consensus": "check_consensus",
                "check_admin": "check_admin"  # Loop for next turn
            }
        )

        workflow.add_conditional_edges(
            "check_consensus",
            route_consensus_check,
            {
                END: END,
                "check_admin": "check_admin"  # Loop for next turn
            }
        )

        # Compile graph
        return workflow.compile()

    # Node wrapper methods (inject dependencies)

    async def _wrap_check_admin(self, state: ConversationState) -> ConversationState:
        return await check_admin_override_node(state)

    async def _wrap_execute_admin(self, state: ConversationState) -> ConversationState:
        return await execute_admin_action_node(state, self.db)

    async def _wrap_check_stopping(self, state: ConversationState) -> ConversationState:
        return await check_stopping_criteria_node(state)

    async def _wrap_system_ai_mediate(self, state: ConversationState) -> ConversationState:
        return await system_ai_mediator_node(state, self.db)

    async def _wrap_select_speaker(self, state: ConversationState) -> ConversationState:
        return await select_next_speaker_node(state, self.participation_balancer)

    async def _wrap_agent_response(self, state: ConversationState) -> ConversationState:
        return await agent_response_node(state, self.agents_dict, self.db)

    async def _wrap_regenerate_response(self, state: ConversationState) -> ConversationState:
        return await regenerate_response_node(state, self.agents_dict, self.db)

    async def _wrap_reflection(self, state: ConversationState) -> ConversationState:
        return await reflection_node(state, self.quality_service, self.db)

    async def _wrap_extract_citations(self, state: ConversationState) -> ConversationState:
        return await extract_citations_node(state)

    async def _wrap_update_participation(self, state: ConversationState) -> ConversationState:
        return await update_participation_node(state)

    async def _wrap_check_consensus(self, state: ConversationState) -> ConversationState:
        """Check consensus and update state"""
        if not state["stopping_criteria"].consensus_enabled:
            return state

        # Calculate consensus
        snapshot = await self.consensus_service.calculate_consensus_score(
            conversation_id=state["conversation_id"],
            turn_number=state["turn_number"],
            recent_messages=state["messages"],
            conversation_goal=state["conversation_goal"],
            agent_ids=state["agent_ids"],
            window_size=state["stopping_criteria"].consensus_window
        )

        # Update state
        state["consensus_score"] = snapshot.consensus_score
        state["consensus_trend"] = snapshot.consensus_trend

        # Check if consensus reached
        if snapshot.consensus_score >= state["stopping_criteria"].consensus_threshold:
            state["should_stop"] = True
            state["stop_reason"] = f"Consensus reached (score: {snapshot.consensus_score:.2f})"

        # Save consensus snapshot
        await self.consensus_service.save_consensus_snapshot(snapshot, self.db)

        return state

    async def stream_conversation(
        self,
        initial_message: str,
        user_id: str = "user"
    ) -> AsyncGenerator[Dict, None]:
        """
        Stream conversation execution with WebSocket events

        Yields events:
        - start: Conversation started
        - agent_start: Agent begins turn
        - token: Streaming token
        - agent_done: Agent completed turn
        - quality_check: Quality validation started
        - quality_pass/fail: Quality check results
        - admin_action: Admin override executed
        - system_mediation: System AI intervention
        - consensus_update: Consensus score changed
        - participation_warning: Imbalance detected
        - complete: Conversation ended

        Args:
            initial_message: User's initial message
            user_id: User identifier

        Yields:
            Event dictionaries for WebSocket streaming
        """
        # Create initial state
        state = create_initial_state(
            conversation_id=self.conversation_id,
            agent_ids=self.agent_ids,
            conversation_goal=self.config.conversation_goal,
            config=self.config
        )

        # Add agents_dict to state
        state["agents_dict"] = self.agents_dict

        # Add initial user message
        from langchain_core.messages import HumanMessage
        state["messages"].append(HumanMessage(content=initial_message, name=user_id))

        # Yield start event
        yield {
            "type": "start",
            "conversation_id": self.conversation_id,
            "goal": self.config.conversation_goal,
            "agent_ids": self.agent_ids
        }

        # Execute graph
        try:
            async for event in self.graph.astream(state):
                # Process events and yield appropriate WebSocket messages
                for node_name, node_output in event.items():
                    if node_name == END:
                        continue

                    # Yield node execution events
                    yield await self._process_node_event(node_name, node_output)

            # Yield completion event
            final_state = event.get(END, state) if event else state
            yield {
                "type": "complete",
                "conversation_id": self.conversation_id,
                "turn_count": final_state.get("turn_number", 0),
                "stop_reason": final_state.get("stop_reason"),
                "consensus_score": final_state.get("consensus_score", 0.0)
            }

        except Exception as e:
            yield {
                "type": "error",
                "error": str(e),
                "conversation_id": self.conversation_id
            }

    async def _process_node_event(self, node_name: str, state: ConversationState) -> Dict:
        """
        Process node execution and generate appropriate event

        Args:
            node_name: Name of executed node
            state: Updated state

        Returns:
            Event dictionary
        """
        if node_name == "agent_response":
            return {
                "type": "agent_done",
                "agent_id": state.get("current_speaker"),
                "turn_number": state.get("turn_number", 0),
                "message": state["messages"][-1].content if state["messages"] else ""
            }

        elif node_name == "reflection":
            quality_check = state.get("pending_quality_check")
            if quality_check:
                passed = not quality_check.should_regenerate
                return {
                    "type": "quality_pass" if passed else "quality_fail",
                    "scores": quality_check.scores,
                    "feedback": quality_check.feedback
                }

        elif node_name == "execute_admin_action":
            return {
                "type": "admin_action",
                "action": state["admin_action_history"][-1].model_dump() if state.get("admin_action_history") else {}
            }

        elif node_name == "system_ai_mediate":
            return {
                "type": "system_mediation",
                "turn_number": state.get("turn_number", 0)
            }

        elif node_name == "check_consensus":
            return {
                "type": "consensus_update",
                "consensus_score": state.get("consensus_score", 0.0),
                "trend": state.get("consensus_trend")
            }

        # Default node event
        return {
            "type": "node_executed",
            "node": node_name
        }

    async def inject_admin_action(self, action: 'AdminOverride'):
        """
        Inject admin action into running conversation

        This would typically be called from WebSocket endpoint
        when admin sends an override command.

        Args:
            action: Admin override action
        """
        # This is a placeholder - in practice, we'd need to modify
        # the running graph state, which requires more sophisticated
        # state management (e.g., checkpointing)
        pass
