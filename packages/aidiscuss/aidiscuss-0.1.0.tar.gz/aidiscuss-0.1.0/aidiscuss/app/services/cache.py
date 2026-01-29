"""
Caching service for providers and agents to reduce database queries
"""

from typing import Optional
from datetime import datetime, timedelta
from aidiscuss.app.models.provider import Provider
from aidiscuss.app.models.agent import Agent


class CacheEntry:
    """Cache entry with expiration"""

    def __init__(self, value: any, ttl_seconds: int = 300):
        self.value = value
        self.expires_at = datetime.now() + timedelta(seconds=ttl_seconds)

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at


class CacheService:
    """
    Simple in-memory cache for providers and agents
    Reduces database queries for frequently accessed data
    """

    def __init__(self, default_ttl: int = 300):
        """
        Initialize cache

        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self._providers: dict[str, CacheEntry] = {}
        self._agents: dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl

    def get_provider(self, provider_id: str) -> Optional[Provider]:
        """Get cached provider"""
        if provider_id in self._providers:
            entry = self._providers[provider_id]
            if not entry.is_expired():
                return entry.value
            else:
                # Remove expired entry
                del self._providers[provider_id]
        return None

    def set_provider(self, provider: Provider, ttl: Optional[int] = None):
        """Cache provider"""
        self._providers[provider.id] = CacheEntry(
            provider, ttl or self._default_ttl
        )

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get cached agent"""
        if agent_id in self._agents:
            entry = self._agents[agent_id]
            if not entry.is_expired():
                return entry.value
            else:
                del self._agents[agent_id]
        return None

    def set_agent(self, agent: Agent, ttl: Optional[int] = None):
        """Cache agent"""
        self._agents[agent.id] = CacheEntry(agent, ttl or self._default_ttl)

    def invalidate_provider(self, provider_id: str):
        """Invalidate cached provider"""
        if provider_id in self._providers:
            del self._providers[provider_id]

    def invalidate_agent(self, agent_id: str):
        """Invalidate cached agent"""
        if agent_id in self._agents:
            del self._agents[agent_id]

    def clear_all(self):
        """Clear all cached data"""
        self._providers.clear()
        self._agents.clear()

    def cleanup_expired(self):
        """Remove all expired entries"""
        # Cleanup providers
        expired_providers = [
            pid for pid, entry in self._providers.items() if entry.is_expired()
        ]
        for pid in expired_providers:
            del self._providers[pid]

        # Cleanup agents
        expired_agents = [
            aid for aid, entry in self._agents.items() if entry.is_expired()
        ]
        for aid in expired_agents:
            del self._agents[aid]


# Global cache instance
cache = CacheService(default_ttl=300)  # 5-minute cache
