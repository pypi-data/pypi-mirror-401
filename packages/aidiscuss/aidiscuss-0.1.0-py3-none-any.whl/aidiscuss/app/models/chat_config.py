"""
Chat Configuration Model and Schema

Stores configuration for multi-agent conversations including:
- Agenda and goals
- Stopping criteria
- Turn-taking strategy
- Quality control settings
- System AI configuration
"""

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class ChatConfigSchema(BaseModel):
    """Pydantic schema for chat configuration validation"""

    # ===== Agenda & Goals Section =====
    conversation_goal: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Primary goal or agenda for the conversation"
    )
    topics_to_cover: List[str] = Field(
        default_factory=list,
        max_length=10,
        description="Optional list of topics to cover during discussion"
    )

    # ===== Stopping Criteria Section =====
    max_turns: int = Field(
        default=20,
        ge=3,
        le=100,
        description="Maximum number of turns before conversation stops"
    )
    min_turns: int = Field(
        default=3,
        ge=1,
        le=50,
        description="Minimum turns before stopping criteria can trigger"
    )
    consensus_enabled: bool = Field(
        default=False,
        description="Enable automatic consensus detection"
    )
    consensus_threshold: float = Field(
        default=0.8,
        ge=0.5,
        le=1.0,
        description="Consensus score threshold (0.5-1.0) to stop conversation"
    )
    consensus_window: int = Field(
        default=5,
        ge=3,
        le=10,
        description="Number of recent messages to analyze for consensus"
    )
    keyword_triggers: List[str] = Field(
        default_factory=list,
        max_length=10,
        description="Keywords that trigger conversation end (e.g., 'DONE', 'CONSENSUS')"
    )
    time_limit_minutes: Optional[int] = Field(
        default=None,
        ge=1,
        le=180,
        description="Optional time limit in minutes"
    )

    # ===== Turn-Taking & Balance Section =====
    turn_strategy: Literal[
        "round-robin",
        "addressed-response",
        "bidding",
        "system-guided"
    ] = Field(
        default="round-robin",
        description="Turn-taking strategy for speaker selection"
    )
    max_consecutive_turns_per_agent: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum consecutive turns allowed per agent"
    )

    # ===== Persona Consistency Section =====
    enable_persona_reminders: bool = Field(
        default=True,
        description="Inject persona reminders to maintain character consistency"
    )
    persona_reminder_frequency: int = Field(
        default=5,
        ge=3,
        le=10,
        description="Inject persona reminder every N turns"
    )
    enable_consistency_scoring: bool = Field(
        default=True,
        description="Score agent responses for persona consistency"
    )
    consistency_check_frequency: int = Field(
        default=10,
        ge=5,
        le=20,
        description="Check persona consistency every N turns"
    )

    # ===== Quality Control Section =====
    enable_reflection: bool = Field(
        default=True,
        description="Enable reflection loops for quality validation"
    )
    reflection_frequency: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Perform quality reflection every N agent responses"
    )
    enable_rag_grounding: bool = Field(
        default=True,
        description="Validate responses against RAG knowledge base"
    )
    require_citations: bool = Field(
        default=False,
        description="Require agents to cite sources from RAG context"
    )
    enable_llm_judge: bool = Field(
        default=True,
        description="Use LLM-as-Judge to score response quality"
    )
    min_quality_threshold: float = Field(
        default=0.6,
        ge=0.4,
        le=1.0,
        description="Minimum quality score to accept response (0.4-1.0)"
    )
    max_regeneration_attempts: int = Field(
        default=2,
        ge=1,
        le=5,
        description="Maximum attempts to regenerate low-quality responses"
    )

    # ===== System AI Configuration Section =====
    system_ai_mode: Literal["active", "passive"] = Field(
        default="passive",
        description="System AI mediation mode (active=intervene, passive=coordinate)"
    )
    system_ai_inject_questions: bool = Field(
        default=True,
        description="Allow System AI to inject clarifying questions"
    )
    system_ai_balance_participation: bool = Field(
        default=True,
        description="System AI balances agent participation"
    )
    system_ai_guide_toward_goal: bool = Field(
        default=True,
        description="System AI redirects conversation if drifting from goal"
    )
    system_ai_mediation_frequency: int = Field(
        default=5,
        ge=3,
        le=15,
        description="System AI mediates every N turns (active mode only)"
    )

    # ===== Novelty & Diversity Section =====
    enable_novelty_detection: bool = Field(
        default=True,
        description="Detect and prevent repetitive responses"
    )
    novelty_threshold: float = Field(
        default=0.3,
        ge=0.1,
        le=0.8,
        description="Minimum novelty score (1.0 - similarity) to accept response"
    )
    enforce_diversity: bool = Field(
        default=True,
        description="Enforce diverse perspectives across agents"
    )
    min_diversity_score: float = Field(
        default=0.5,
        ge=0.3,
        le=0.9,
        description="Minimum diversity score across agent responses"
    )

    # ===== Admin Control Section =====
    allow_admin_override: bool = Field(
        default=True,
        description="Allow admin to override conversation mid-stream"
    )

    # ===== Memory Configuration Section =====
    enable_memory: bool = Field(
        default=True,
        description="Enable conversation memory (facts, summaries, checkpoints)"
    )
    memory_summary_frequency: int = Field(
        default=10,
        ge=5,
        le=20,
        description="Generate memory summary every N turns"
    )

    # ===== RAG Configuration Section =====
    enable_rag: bool = Field(
        default=False,
        description="Enable RAG knowledge grounding"
    )
    rag_namespace: str = Field(
        default="default",
        description="RAG namespace for document retrieval"
    )
    rag_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of RAG documents to retrieve (top-k)"
    )
    rag_min_score: float = Field(
        default=0.7,
        ge=0.5,
        le=1.0,
        description="Minimum similarity score for RAG retrieval"
    )

    # ===== Advanced Settings Section =====
    context_window_messages: int = Field(
        default=20,
        ge=5,
        le=50,
        description="Number of recent messages to keep in context window"
    )
    enable_tools: bool = Field(
        default=True,
        description="Enable agent tool use"
    )
    enable_analytics: bool = Field(
        default=True,
        description="Track analytics (token usage, quality metrics, etc.)"
    )

    # ===== Emotional Tone Settings (Future Enhancement) =====
    target_tone: Optional[Literal["formal", "friendly", "empathetic", "neutral"]] = Field(
        default=None,
        description="Target emotional tone for conversation"
    )

    # ===== Debate Mode Settings (Future Enhancement) =====
    debate_mode: bool = Field(
        default=False,
        description="Enable structured debate format"
    )
    debate_rounds: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Number of debate rounds (if debate_mode enabled)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_goal": "Discuss the implications of AI on future job markets",
                "topics_to_cover": ["automation", "new job creation", "education needs"],
                "max_turns": 20,
                "min_turns": 5,
                "turn_strategy": "round-robin",
                "enable_reflection": True,
                "system_ai_mode": "active",
                "enable_rag": True,
                "rag_namespace": "economics"
            }
        }


class ChatConfig(Base):
    """Database model for chat configuration"""
    __tablename__ = "chat_configs"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, unique=True, nullable=False, index=True)
    config_json = Column(JSON, nullable=False)  # Stores ChatConfigSchema as JSON
    is_locked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_schema(self) -> ChatConfigSchema:
        """Convert database model to Pydantic schema"""
        return ChatConfigSchema(**self.config_json)

    @staticmethod
    def from_schema(conversation_id: str, schema: ChatConfigSchema, config_id: str) -> "ChatConfig":
        """Create database model from Pydantic schema"""
        return ChatConfig(
            id=config_id,
            conversation_id=conversation_id,
            config_json=schema.model_dump(),
            is_locked=False
        )

    def __repr__(self) -> str:
        return f"<ChatConfig(id={self.id}, conversation_id={self.conversation_id}, locked={self.is_locked})>"
