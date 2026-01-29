"""
LangGraph-based Multi-Agent Orchestration

This package contains the LangGraph implementation for sophisticated multi-agent
conversation orchestration with quality controls, admin overrides, and system AI mediation.
"""

from .state import (
    ConversationState,
    AgentParticipation,
    StoppingCriteria,
    SystemAIConfig,
    QualityConfig,
    AdminOverride
)

__all__ = [
    "ConversationState",
    "AgentParticipation",
    "StoppingCriteria",
    "SystemAIConfig",
    "QualityConfig",
    "AdminOverride"
]
