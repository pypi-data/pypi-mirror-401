"""
Analytics Service - Phase 5
Tracks costs, token usage, agent participation, and conversation quality metrics
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from collections import defaultdict
import json


class TokenUsage(BaseModel):
    """Token usage for a single API call"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class APICallMetrics(BaseModel):
    """Metrics for a single API call"""
    timestamp: datetime
    conversation_id: str
    agent_id: str
    provider_id: str
    model: str
    tokens: TokenUsage
    cost_usd: float
    latency_ms: float
    success: bool
    error: Optional[str] = None


class ConversationAnalytics(BaseModel):
    """Aggregated analytics for a conversation"""
    conversation_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_turns: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    average_latency_ms: float = 0.0
    agent_participation: Dict[str, int] = Field(default_factory=dict)
    provider_usage: Dict[str, int] = Field(default_factory=dict)
    token_timeline: List[Dict[str, Any]] = Field(default_factory=list)


class AgentMetrics(BaseModel):
    """Metrics for a specific agent"""
    agent_id: str
    total_calls: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    average_tokens_per_call: float = 0.0
    average_latency_ms: float = 0.0
    success_rate: float = 1.0
    conversations: int = 0


class CostBreakdown(BaseModel):
    """Cost breakdown by provider/model"""
    total_cost_usd: float
    by_provider: Dict[str, float] = Field(default_factory=dict)
    by_model: Dict[str, float] = Field(default_factory=dict)
    by_conversation: Dict[str, float] = Field(default_factory=dict)


# Pricing data (approximate costs per 1M tokens as of 2026)
MODEL_PRICING = {
    # OpenAI
    "gpt-4": {"prompt": 30.0, "completion": 60.0},
    "gpt-4-turbo": {"prompt": 10.0, "completion": 30.0},
    "gpt-3.5-turbo": {"prompt": 0.5, "completion": 1.5},
    "gpt-4o": {"prompt": 5.0, "completion": 15.0},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.6},

    # Anthropic
    "claude-3-opus": {"prompt": 15.0, "completion": 75.0},
    "claude-3-sonnet": {"prompt": 3.0, "completion": 15.0},
    "claude-3-haiku": {"prompt": 0.25, "completion": 1.25},
    "claude-3.5-sonnet": {"prompt": 3.0, "completion": 15.0},
    "claude-3.5-haiku": {"prompt": 0.8, "completion": 4.0},

    # Google
    "gemini-pro": {"prompt": 0.5, "completion": 1.5},
    "gemini-1.5-pro": {"prompt": 3.5, "completion": 10.5},
    "gemini-1.5-flash": {"prompt": 0.075, "completion": 0.3},

    # Local models (free)
    "ollama": {"prompt": 0.0, "completion": 0.0},
}


class AnalyticsService:
    """
    Service for tracking and analyzing conversation metrics

    Features:
    - Real-time cost tracking
    - Token usage analytics
    - Agent participation metrics
    - Provider usage statistics
    - Conversation quality tracking
    """

    def __init__(self):
        self.api_calls: List[APICallMetrics] = []
        self.conversations: Dict[str, ConversationAnalytics] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}

    def calculate_cost(self, model: str, tokens: TokenUsage) -> float:
        """
        Calculate cost in USD for API call

        Args:
            model: Model name
            tokens: Token usage

        Returns:
            Cost in USD
        """
        # Normalize model name (handle variations)
        model_key = model.lower()

        # Try exact match first
        if model_key in MODEL_PRICING:
            pricing = MODEL_PRICING[model_key]
        else:
            # Try to find partial match
            for key in MODEL_PRICING:
                if key in model_key:
                    pricing = MODEL_PRICING[key]
                    break
            else:
                # Default to gpt-3.5-turbo pricing if unknown
                pricing = MODEL_PRICING["gpt-3.5-turbo"]

        prompt_cost = (tokens.prompt_tokens / 1_000_000) * pricing["prompt"]
        completion_cost = (tokens.completion_tokens / 1_000_000) * pricing["completion"]

        return prompt_cost + completion_cost

    def track_api_call(
        self,
        conversation_id: str,
        agent_id: str,
        provider_id: str,
        model: str,
        tokens: TokenUsage,
        latency_ms: float,
        success: bool = True,
        error: Optional[str] = None
    ):
        """
        Track a single API call

        Args:
            conversation_id: Conversation ID
            agent_id: Agent ID
            provider_id: Provider ID
            model: Model name
            tokens: Token usage
            latency_ms: Request latency in milliseconds
            success: Whether call succeeded
            error: Error message if failed
        """
        # Calculate cost
        cost = self.calculate_cost(model, tokens)

        # Create metrics record
        metrics = APICallMetrics(
            timestamp=datetime.now(),
            conversation_id=conversation_id,
            agent_id=agent_id,
            provider_id=provider_id,
            model=model,
            tokens=tokens,
            cost_usd=cost,
            latency_ms=latency_ms,
            success=success,
            error=error
        )

        self.api_calls.append(metrics)

        # Update conversation analytics
        self._update_conversation_analytics(metrics)

        # Update agent metrics
        self._update_agent_metrics(metrics)

    def _update_conversation_analytics(self, call: APICallMetrics):
        """Update conversation-level analytics"""
        conv_id = call.conversation_id

        if conv_id not in self.conversations:
            self.conversations[conv_id] = ConversationAnalytics(
                conversation_id=conv_id,
                start_time=call.timestamp
            )

        conv = self.conversations[conv_id]
        conv.end_time = call.timestamp
        conv.total_turns += 1
        conv.total_tokens += call.tokens.total_tokens
        conv.total_cost_usd += call.cost_usd

        # Update average latency
        total_latency = conv.average_latency_ms * (conv.total_turns - 1) + call.latency_ms
        conv.average_latency_ms = total_latency / conv.total_turns

        # Agent participation
        if call.agent_id not in conv.agent_participation:
            conv.agent_participation[call.agent_id] = 0
        conv.agent_participation[call.agent_id] += 1

        # Provider usage
        if call.provider_id not in conv.provider_usage:
            conv.provider_usage[call.provider_id] = 0
        conv.provider_usage[call.provider_id] += 1

        # Token timeline
        conv.token_timeline.append({
            "timestamp": call.timestamp.isoformat(),
            "tokens": call.tokens.total_tokens,
            "cumulative_tokens": conv.total_tokens,
            "agent_id": call.agent_id
        })

    def _update_agent_metrics(self, call: APICallMetrics):
        """Update agent-level metrics"""
        agent_id = call.agent_id

        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id)

        agent = self.agent_metrics[agent_id]
        agent.total_calls += 1
        agent.total_tokens += call.tokens.total_tokens
        agent.total_cost_usd += call.cost_usd

        # Update averages
        agent.average_tokens_per_call = agent.total_tokens / agent.total_calls
        total_latency = agent.average_latency_ms * (agent.total_calls - 1) + call.latency_ms
        agent.average_latency_ms = total_latency / agent.total_calls

        # Update success rate
        successes = sum(1 for c in self.api_calls if c.agent_id == agent_id and c.success)
        agent.success_rate = successes / agent.total_calls

        # Count unique conversations
        unique_convs = set(c.conversation_id for c in self.api_calls if c.agent_id == agent_id)
        agent.conversations = len(unique_convs)

    def get_conversation_analytics(self, conversation_id: str) -> Optional[ConversationAnalytics]:
        """Get analytics for specific conversation"""
        return self.conversations.get(conversation_id)

    def get_agent_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """Get metrics for specific agent"""
        return self.agent_metrics.get(agent_id)

    def get_cost_breakdown(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> CostBreakdown:
        """
        Get cost breakdown by provider, model, and conversation

        Args:
            start_date: Filter calls after this date
            end_date: Filter calls before this date

        Returns:
            Cost breakdown
        """
        # Filter calls by date range
        calls = self.api_calls
        if start_date:
            calls = [c for c in calls if c.timestamp >= start_date]
        if end_date:
            calls = [c for c in calls if c.timestamp <= end_date]

        breakdown = CostBreakdown(total_cost_usd=0.0)

        for call in calls:
            breakdown.total_cost_usd += call.cost_usd

            # By provider
            if call.provider_id not in breakdown.by_provider:
                breakdown.by_provider[call.provider_id] = 0.0
            breakdown.by_provider[call.provider_id] += call.cost_usd

            # By model
            if call.model not in breakdown.by_model:
                breakdown.by_model[call.model] = 0.0
            breakdown.by_model[call.model] += call.cost_usd

            # By conversation
            if call.conversation_id not in breakdown.by_conversation:
                breakdown.by_conversation[call.conversation_id] = 0.0
            breakdown.by_conversation[call.conversation_id] += call.cost_usd

        return breakdown

    def get_token_usage_timeline(
        self,
        conversation_id: Optional[str] = None,
        granularity: str = "minute"  # "minute", "hour", "day"
    ) -> List[Dict[str, Any]]:
        """
        Get token usage over time

        Args:
            conversation_id: Filter by conversation (optional)
            granularity: Time granularity

        Returns:
            Timeline data points
        """
        calls = self.api_calls
        if conversation_id:
            calls = [c for c in calls if c.conversation_id == conversation_id]

        if not calls:
            return []

        # Group by time bucket
        buckets: Dict[str, Dict[str, int]] = defaultdict(lambda: {"tokens": 0, "calls": 0})

        for call in calls:
            # Round timestamp to granularity
            if granularity == "minute":
                bucket_time = call.timestamp.replace(second=0, microsecond=0)
            elif granularity == "hour":
                bucket_time = call.timestamp.replace(minute=0, second=0, microsecond=0)
            else:  # day
                bucket_time = call.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

            bucket_key = bucket_time.isoformat()
            buckets[bucket_key]["tokens"] += call.tokens.total_tokens
            buckets[bucket_key]["calls"] += 1

        # Convert to timeline
        timeline = [
            {
                "timestamp": bucket_key,
                "tokens": data["tokens"],
                "calls": data["calls"]
            }
            for bucket_key, data in sorted(buckets.items())
        ]

        return timeline

    def get_agent_participation_stats(
        self,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get agent participation statistics

        Args:
            conversation_id: Filter by conversation (optional)

        Returns:
            Agent participation data
        """
        calls = self.api_calls
        if conversation_id:
            calls = [c for c in calls if c.conversation_id == conversation_id]

        stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "turns": 0,
            "tokens": 0,
            "cost_usd": 0.0,
            "avg_latency_ms": 0.0,
            "total_latency": 0.0
        })

        for call in calls:
            agent = stats[call.agent_id]
            agent["turns"] += 1
            agent["tokens"] += call.tokens.total_tokens
            agent["cost_usd"] += call.cost_usd
            agent["total_latency"] += call.latency_ms

        # Calculate averages
        for agent_id, data in stats.items():
            if data["turns"] > 0:
                data["avg_latency_ms"] = data["total_latency"] / data["turns"]
            del data["total_latency"]  # Remove intermediate value

        return dict(stats)

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get overall summary statistics"""
        total_calls = len(self.api_calls)
        if total_calls == 0:
            return {
                "total_calls": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "total_conversations": 0,
                "total_agents": 0,
                "average_latency_ms": 0.0
            }

        total_tokens = sum(call.tokens.total_tokens for call in self.api_calls)
        total_cost = sum(call.cost_usd for call in self.api_calls)
        avg_latency = sum(call.latency_ms for call in self.api_calls) / total_calls

        return {
            "total_calls": total_calls,
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost,
            "total_conversations": len(self.conversations),
            "total_agents": len(self.agent_metrics),
            "average_latency_ms": avg_latency,
            "success_rate": sum(1 for c in self.api_calls if c.success) / total_calls
        }


# Singleton instance
analytics_service = AnalyticsService()
