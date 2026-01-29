"""
LangGraph State Schema

Defines the comprehensive state structure for multi-agent conversations including:
- Core conversation state (messages, turn tracking)
- Agent participation tracking
- Stopping criteria configuration
- System AI mediation config
- Quality control settings
- Admin override actions
- Consensus and novelty tracking
"""

from datetime import datetime
from typing import Dict, List, Literal, Optional, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class AgentParticipation(BaseModel):
    """Track individual agent participation metrics"""

    agent_id: str
    consecutive_turns: int = 0
    total_turns: int = 0
    last_turn_number: int = 0
    response_quality_scores: List[float] = Field(default_factory=list)
    novelty_scores: List[float] = Field(default_factory=list)
    consistency_scores: List[float] = Field(default_factory=list)

    def reset_consecutive(self):
        """Reset consecutive turn counter"""
        self.consecutive_turns = 0

    def add_turn(self, turn_number: int, quality_score: Optional[float] = None):
        """Record a new turn for this agent"""
        self.consecutive_turns += 1
        self.total_turns += 1
        self.last_turn_number = turn_number
        if quality_score is not None:
            self.response_quality_scores.append(quality_score)

    def average_quality(self) -> float:
        """Calculate average quality score"""
        if not self.response_quality_scores:
            return 0.5  # Default neutral score
        return sum(self.response_quality_scores) / len(self.response_quality_scores)


class StoppingCriteria(BaseModel):
    """Configuration for conversation stopping conditions"""

    max_turns: int = 20
    min_turns: int = 3
    consensus_enabled: bool = False
    consensus_threshold: float = 0.8
    consensus_window: int = 5
    keyword_triggers: List[str] = Field(default_factory=list)
    time_limit_seconds: Optional[int] = None

    def should_check_consensus(self, turn_number: int) -> bool:
        """Check if we should evaluate consensus at this turn"""
        return self.consensus_enabled and turn_number >= self.min_turns

    def check_turn_limit(self, turn_number: int) -> tuple[bool, Optional[str]]:
        """
        Check if turn limit reached
        Returns: (should_stop, stop_reason)
        """
        if turn_number >= self.max_turns:
            return True, "Maximum turns reached"
        return False, None

    def check_keyword_trigger(self, message_content: str) -> tuple[bool, Optional[str]]:
        """
        Check if message contains stopping keyword
        Returns: (should_stop, stop_reason)
        """
        content_upper = message_content.upper()
        for keyword in self.keyword_triggers:
            if keyword.upper() in content_upper:
                return True, f"Keyword trigger detected: {keyword}"
        return False, None


class SystemAIConfig(BaseModel):
    """System AI orchestrator configuration"""

    mode: Literal["active", "passive"] = "passive"
    inject_questions: bool = True
    balance_participation: bool = True
    guide_toward_goal: bool = True
    mediation_frequency: int = 5

    def should_mediate(self, turn_number: int) -> bool:
        """Check if System AI should mediate at this turn"""
        return self.mode == "active" and (turn_number % self.mediation_frequency == 0)


class QualityConfig(BaseModel):
    """Quality control configuration"""

    enable_reflection: bool = True
    enable_rag_grounding: bool = True
    enable_llm_judge: bool = True
    reflection_frequency: int = 3
    min_quality_threshold: float = 0.6
    require_citations: bool = False
    max_regeneration_attempts: int = 2
    enable_novelty_detection: bool = True
    novelty_threshold: float = 0.3

    def should_check_quality(self, turn_number: int) -> bool:
        """Check if quality check should run at this turn"""
        return self.enable_reflection and (turn_number % self.reflection_frequency == 0)

    def passes_threshold(self, score: float) -> bool:
        """Check if quality score passes minimum threshold"""
        return score >= self.min_quality_threshold


class AdminOverride(BaseModel):
    """Admin override action"""

    action_type: Literal[
        "redirect",
        "kick_agent",
        "add_agent",
        "modify_goal",
        "inject_context",
        "pause",
        "resume",
        "toggle_system_ai_mode"
    ]
    target_agent_id: Optional[str] = None
    new_goal: Optional[str] = None
    injected_context: Optional[str] = None
    new_system_ai_mode: Optional[Literal["active", "passive"]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: str = "admin"


class PendingQualityCheck(BaseModel):
    """Pending quality check for a response"""

    agent_id: str
    response: str
    turn_number: int
    should_regenerate: bool = False
    regeneration_attempt: int = 0
    scores: Dict[str, float] = Field(default_factory=dict)
    feedback: List[str] = Field(default_factory=list)


class ConversationState(TypedDict, total=False):
    """
    LangGraph state for multi-agent conversation

    This TypedDict defines the complete state maintained throughout the conversation.
    All fields are optional (total=False) to allow partial state updates.
    """

    # ===== Core Conversation State =====
    messages: List[BaseMessage]
    conversation_id: str
    turn_number: int
    started_at: datetime

    # ===== Agent Management =====
    agent_ids: List[str]
    agents_dict: Dict[str, Dict]  # Agent ID -> Agent configuration
    agent_participation: Dict[str, AgentParticipation]
    current_speaker: Optional[str]
    next_speaker: Optional[str]

    # ===== Orchestration Strategy =====
    turn_strategy: Literal[
        "round-robin",
        "addressed-response",
        "bidding",
        "system-guided"
    ]

    # ===== Goal and Agenda =====
    conversation_goal: str
    topics_to_cover: List[str]
    current_topics: List[str]

    # ===== Stopping Criteria =====
    stopping_criteria: StoppingCriteria
    should_stop: bool
    stop_reason: Optional[str]

    # ===== System AI =====
    system_ai_config: SystemAIConfig
    system_ai_active: bool

    # ===== Quality Control =====
    quality_config: QualityConfig
    pending_quality_check: Optional[PendingQualityCheck]
    regeneration_count: int

    # ===== Admin Control =====
    admin_mode: bool
    allow_admin_override: bool
    pending_admin_action: Optional[AdminOverride]
    admin_action_history: List[AdminOverride]

    # ===== RAG and Memory =====
    rag_context: Optional[str]
    rag_enabled: bool
    memory_context: Optional[Dict]
    enable_memory: bool

    # ===== Consensus Tracking =====
    consensus_score: float
    consensus_trend: Optional[str]
    recent_agreements: List[Dict]

    # ===== Novelty Tracking =====
    recent_response_embeddings: List[List[float]]
    novelty_threshold: float

    # ===== Metadata =====
    metadata: Dict


def create_initial_state(
    conversation_id: str,
    agent_ids: List[str],
    conversation_goal: str,
    config: 'ChatConfigSchema'  # Type hint for ChatConfigSchema from models
) -> ConversationState:
    """
    Create initial conversation state from configuration

    Args:
        conversation_id: Unique conversation identifier
        agent_ids: List of agent IDs participating in conversation
        conversation_goal: Primary goal/agenda for conversation
        config: ChatConfigSchema with all configuration settings

    Returns:
        Initialized ConversationState ready for LangGraph execution
    """
    from aidiscuss.app.models.chat_config import ChatConfigSchema

    # Initialize agent participation tracking
    participation = {
        agent_id: AgentParticipation(agent_id=agent_id)
        for agent_id in agent_ids
    }

    # Create state
    state: ConversationState = {
        # Core state
        "messages": [],
        "conversation_id": conversation_id,
        "turn_number": 0,
        "started_at": datetime.now(),

        # Agents
        "agent_ids": agent_ids,
        "agent_participation": participation,
        "current_speaker": None,
        "next_speaker": None,

        # Orchestration
        "turn_strategy": config.turn_strategy,

        # Goal
        "conversation_goal": conversation_goal,
        "topics_to_cover": config.topics_to_cover,
        "current_topics": [],

        # Stopping criteria
        "stopping_criteria": StoppingCriteria(
            max_turns=config.max_turns,
            min_turns=config.min_turns,
            consensus_enabled=config.consensus_enabled,
            consensus_threshold=config.consensus_threshold,
            consensus_window=config.consensus_window,
            keyword_triggers=config.keyword_triggers,
            time_limit_seconds=config.time_limit_minutes * 60 if config.time_limit_minutes else None
        ),
        "should_stop": False,
        "stop_reason": None,

        # System AI
        "system_ai_config": SystemAIConfig(
            mode=config.system_ai_mode,
            inject_questions=config.system_ai_inject_questions,
            balance_participation=config.system_ai_balance_participation,
            guide_toward_goal=config.system_ai_guide_toward_goal,
            mediation_frequency=config.system_ai_mediation_frequency
        ),
        "system_ai_active": config.system_ai_mode == "active",

        # Quality
        "quality_config": QualityConfig(
            enable_reflection=config.enable_reflection,
            enable_rag_grounding=config.enable_rag_grounding,
            enable_llm_judge=config.enable_llm_judge,
            reflection_frequency=config.reflection_frequency,
            min_quality_threshold=config.min_quality_threshold,
            require_citations=config.require_citations,
            max_regeneration_attempts=config.max_regeneration_attempts,
            enable_novelty_detection=config.enable_novelty_detection,
            novelty_threshold=config.novelty_threshold
        ),
        "pending_quality_check": None,
        "regeneration_count": 0,

        # Admin
        "admin_mode": False,
        "allow_admin_override": config.allow_admin_override,
        "pending_admin_action": None,
        "admin_action_history": [],

        # RAG and Memory
        "rag_context": None,
        "rag_enabled": config.enable_rag,
        "memory_context": None,
        "enable_memory": config.enable_memory,

        # Consensus
        "consensus_score": 0.0,
        "consensus_trend": None,
        "recent_agreements": [],

        # Novelty
        "recent_response_embeddings": [],
        "novelty_threshold": config.novelty_threshold,

        # Metadata
        "metadata": {}
    }

    return state


def state_to_dict(state: ConversationState) -> Dict:
    """
    Convert ConversationState to dict for database storage

    Note: Excludes messages (stored separately) and embeddings (too large)
    """
    return {
        "conversation_id": state.get("conversation_id"),
        "turn_number": state.get("turn_number"),
        "agent_ids": state.get("agent_ids"),
        "agent_participation": {
            k: v.model_dump() for k, v in state.get("agent_participation", {}).items()
        },
        "current_speaker": state.get("current_speaker"),
        "turn_strategy": state.get("turn_strategy"),
        "conversation_goal": state.get("conversation_goal"),
        "should_stop": state.get("should_stop"),
        "stop_reason": state.get("stop_reason"),
        "consensus_score": state.get("consensus_score"),
        "consensus_trend": state.get("consensus_trend"),
        "metadata": state.get("metadata", {})
    }
