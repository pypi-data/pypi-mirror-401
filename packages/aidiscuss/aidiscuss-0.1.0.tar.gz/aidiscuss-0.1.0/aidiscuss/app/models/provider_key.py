from sqlalchemy import Column, String, Integer, Boolean, JSON, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from aidiscuss.app.db.base import Base
from aidiscuss.app.core.encryption import encryption_service


class ProviderKey(Base):
    """
    Stores API keys for LLM providers with usage tracking and rate limits.
    API keys are automatically encrypted at rest using Fernet (AES-128).
    """
    __tablename__ = "provider_keys"

    id = Column(String, primary_key=True)
    provider = Column(String, nullable=False, index=True)  # Provider ID reference
    key = Column(String, nullable=False)  # API key (encrypted at rest)
    label = Column(String, nullable=False)  # User-friendly name for the key

    # Rate limiting configuration
    rate_limit = Column(
        JSON,
        nullable=False,
        default={"rpm": 60, "tpm": 10000}
    )  # {"rpm": requests per minute, "tpm": tokens per minute}

    daily_token_cap = Column(Integer, nullable=False, default=1000000)
    enabled = Column(Boolean, nullable=False, default=True)

    # Additional metadata
    extra_metadata = Column(JSON, nullable=True)  # Arbitrary key-value pairs
    notes = Column(Text, nullable=True)  # User notes about this key
    last_used = Column(DateTime(timezone=True), nullable=True)

    # Usage statistics
    usage = Column(
        JSON,
        nullable=False,
        default={
            "tokensToday": 0,
            "requestsToday": 0,
            "totalTokens": 0,
            "totalRequests": 0,
            "estimatedCost": 0.0
        }
    )

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    @validates("key")
    def encrypt_key(self, key_name, plaintext_key):
        """Automatically encrypt API key before storing"""
        if not plaintext_key:
            return plaintext_key
        # Encrypt the key
        return encryption_service.encrypt(plaintext_key)

    def get_decrypted_key(self) -> str:
        """Get the decrypted API key"""
        if not self.key:
            return ""
        return encryption_service.decrypt(self.key)

    def __repr__(self):
        return f"<ProviderKey(id={self.id}, provider={self.provider}, label={self.label})>"
