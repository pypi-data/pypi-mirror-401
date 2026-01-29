"""
Provider model - stores LLM provider configurations with metadata
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class Provider(Base):
    """LLM Provider model"""

    __tablename__ = "providers"

    id = Column(String, primary_key=True)  # e.g., "openai", "anthropic", "google"
    name = Column(String, nullable=False)  # Display name
    api_key_encrypted = Column(Text, nullable=True)  # Encrypted API key
    base_url = Column(String, nullable=True)  # Custom base URL (optional)
    is_active = Column(Boolean, default=True)  # Whether this provider is enabled
    meta = Column("metadata", JSON, nullable=True)  # Provider metadata (models, pricing, capabilities)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_api_key(self, api_key: str):
        """Encrypt and store API key"""
        if api_key:
            self.api_key_encrypted = api_key
        else:
            self.api_key_encrypted = None

    def get_api_key(self) -> str | None:
        """Decrypt and return API key"""
        if self.api_key_encrypted:
            try:
                return self.api_key_encrypted
            except Exception:
                return None
        return None
