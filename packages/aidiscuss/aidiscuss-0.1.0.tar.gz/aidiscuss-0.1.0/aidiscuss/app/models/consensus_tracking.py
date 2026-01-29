"""
Consensus Tracking Model

Tracks consensus scores and agreement/disagreement patterns throughout conversation.
Used for automatic stopping when consensus is reached.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class ConsensusSnapshot(BaseModel):
    """Pydantic schema for consensus snapshot at a given turn"""

    conversation_id: str
    turn_number: int

    # Consensus score (0.0 - 1.0)
    consensus_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Consensus score based on recent messages (1.0 = full agreement)"
    )

    # Topic analysis
    agreement_topics: List[str] = Field(
        default_factory=list,
        description="Topics where agents agree"
    )
    disagreement_topics: List[str] = Field(
        default_factory=list,
        description="Topics where agents disagree"
    )

    # Agent alignment
    agent_alignments: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="Which agents align with which viewpoints"
    )

    # Analysis metadata
    analysis_method: Optional[str] = Field(
        default="llm_judge",
        description="Method used for consensus detection (llm_judge, embedding_similarity, etc.)"
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence in consensus score"
    )

    # Trend information
    consensus_trend: Optional[str] = Field(
        default=None,
        description="Trend direction: increasing, decreasing, stable"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "turn_number": 15,
                "consensus_score": 0.82,
                "agreement_topics": [
                    "AI will impact job market",
                    "Education needs reform"
                ],
                "disagreement_topics": [
                    "Timeline for changes",
                    "Government regulation approach"
                ],
                "agent_alignments": {
                    "optimistic_view": ["agent_1", "agent_3"],
                    "cautious_view": ["agent_2"]
                },
                "analysis_method": "llm_judge",
                "confidence": 0.85,
                "consensus_trend": "increasing"
            }
        }


class ConsensusTracking(Base):
    """Database model for consensus tracking"""
    __tablename__ = "consensus_tracking"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False, index=True)
    turn_number = Column(Integer, nullable=False)

    # Consensus metrics
    consensus_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=True)

    # Topic analysis (stored as JSON)
    agreement_topics = Column(JSON, nullable=True)
    disagreement_topics = Column(JSON, nullable=True)
    agent_alignments = Column(JSON, nullable=True)

    # Metadata
    analysis_method = Column(String, default="llm_judge", nullable=True)
    consensus_trend = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def to_schema(self) -> ConsensusSnapshot:
        """Convert database model to Pydantic schema"""
        return ConsensusSnapshot(
            conversation_id=self.conversation_id,
            turn_number=self.turn_number,
            consensus_score=self.consensus_score,
            agreement_topics=self.agreement_topics or [],
            disagreement_topics=self.disagreement_topics or [],
            agent_alignments=self.agent_alignments,
            analysis_method=self.analysis_method,
            confidence=self.confidence,
            consensus_trend=self.consensus_trend
        )

    @staticmethod
    def from_schema(schema: ConsensusSnapshot, tracking_id: str) -> "ConsensusTracking":
        """Create database model from Pydantic schema"""
        return ConsensusTracking(
            id=tracking_id,
            conversation_id=schema.conversation_id,
            turn_number=schema.turn_number,
            consensus_score=schema.consensus_score,
            agreement_topics=schema.agreement_topics,
            disagreement_topics=schema.disagreement_topics,
            agent_alignments=schema.agent_alignments,
            analysis_method=schema.analysis_method,
            confidence=schema.confidence,
            consensus_trend=schema.consensus_trend
        )

    def __repr__(self) -> str:
        return (
            f"<ConsensusTracking(id={self.id}, turn={self.turn_number}, "
            f"score={self.consensus_score:.2f}, trend={self.consensus_trend})>"
        )
